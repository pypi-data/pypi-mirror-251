# -*- coding: utf-8 -*-

# Copyright 2024 Jean-Baptiste Delisle
#
# This file is part of p2esm.
#
# p2esm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# p2esm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with p2esm.  If not, see <http://www.gnu.org/licenses/>.


import os
import tkinter as tk

import numpy as np
import p2api
import tomllib
from astropy import units as u
from astropy.coordinates import (
  AltAz,
  EarthLocation,
  SkyCoord,
  get_body,
)
from astropy.time import Time
from matplotlib import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure


class P2ESM(tk.Tk):
  def __init__(self, config):
    super().__init__()
    self.iconphoto(
      True,
      tk.PhotoImage(file=f'{os.path.dirname(os.path.realpath(__file__))}/p2esm.png'),
    )
    self.config = config
    self.inst = self.config['telescope']['instruments']
    self.ninst = len(self.inst)
    self.wm_title('P2 Execution Sequence Merger')
    self.init_widgets()
    self.init_astropy()
    self.init_p2api()
    self.refresh_p2()
    self.redraw()

  def init_widgets(self):
    rcParams.update({'font.size': self.config['plot']['fontsize']})
    self.fig = Figure(
      figsize=self.config['plot']['figsize'], dpi=self.config['plot']['dpi']
    )
    self.ax = self.fig.add_subplot()
    self.canvas = FigureCanvasTkAgg(self.fig, master=self)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    self.canvas.mpl_connect('button_press_event', self.on_click)

  def on_click(self, event):
    if event.xdata is None:
      return
    ut = Time(event.xdata, format='plot_date')
    ut.format = 'datetime'
    if event.button == 1:
      starts = np.array([ob['start'] for ob in self.sequence])
      k = np.searchsorted(starts, ut) - 1
      if k == -1:
        self.current_inst = (self.current_inst + 1) % self.ninst
        self.next_inst = self.current_inst
      elif k < len(self.sequence) - 1:
        obId = self.sequence[k]['obId']
        inst = self.sequence[k]['inst']
        if obId in self.switch:
          inst = self.switch[obId]
        self.switch[obId] = (inst + 1) % self.ninst
        if self.switch[obId] == self.sequence[k]['inst']:
          self.switch.pop(obId)
    else:
      self.start = ut
      self.custom_start = True

  def init_astropy(self):
    self.obs_site = EarthLocation.of_site(self.config['telescope']['site'])
    self.now = Time.now()
    tshift = self.obs_site.lon / (360 * u.deg) * 24 * u.h
    self.night = (
      self.now + tshift - self.config['telescope']['latest_localtime_sunrise_h'] * u.h
    ).strftime('%Y-%m-%d')
    tstart = Time(self.night) - tshift + 12 * u.h
    tstep = self.config['plot']['tstep_min'] * u.min
    nt = int(1 * u.d / tstep) + 1
    dt_night = np.arange(nt) / (nt - 1) * u.d
    t = tstart + dt_night
    # ESO seems to define the horizon at 0 deg in P2, etc.
    horizon = 0 * u.deg
    # R = 1.0 * u.Rearth
    # H = obs_site.to_geodetic().height
    # horizon = np.arccos(R / (R + H))

    sun = get_body('sun', t, location=self.obs_site)
    sun_altaz = sun.transform_to(AltAz(obstime=t, location=self.obs_site))
    to_plot = sun_altaz.alt < horizon + 6 * u.deg
    self.t = t[to_plot]
    sun_altaz = sun_altaz[to_plot]
    night_def = dict(
      sunset=0 * u.deg, civil=-6 * u.deg, nautic=-12 * u.deg, astro=-18 * u.deg
    )
    self.night_label = dict(
      sunset='civil twilight',
      civil='nautical twilight',
      nautic='astronomical twilight',
      astro=None,
    )
    self.night_color = dict(
      sunset='whitesmoke', civil='lightgray', nautic='darkgray', astro='white'
    )
    self.night_t = {
      key: self.t[sun_altaz.alt < night_def[key] - horizon] for key in night_def
    }

    self.moon = get_body('moon', self.t, location=self.obs_site)
    self.moon_alt = self.moon.transform_to(
      AltAz(obstime=self.t, location=self.obs_site)
    ).alt

  def init_p2api(self):
    self.p2api = p2api.ApiConnection(
      self.config['p2api']['env'],
      self.config['p2api']['user'],
      self.config['p2api']['password'],
    )
    self.current_ob = None
    self.current_inst = 0
    self.next_inst = 0
    self.switch = {}
    self.custom_start = False
    self.start = self.t[0]
    self.sequence = []
    self.known_obs = {}

  def calc_ob(self, ob):
    if ob['obId'] in self.known_obs:
      hem, alt, airmass, moon_sep = self.known_obs[ob['obId']]
    else:
      coord = SkyCoord(
        ob['target']['ra'], ob['target']['dec'], unit=(u.hourangle, u.deg), frame='icrs'
      )
      hem = 'North' if coord.dec.to_value() > self.obs_site.lat.to_value() else 'South'
      altaz = coord.transform_to(AltAz(obstime=self.t, location=self.obs_site))
      alt = altaz.alt
      airmass = altaz.secz
      airmass[airmass < 0] = np.inf
      moon_sep = self.moon.separation(coord)
      self.known_obs[ob['obId']] = hem, alt, airmass, moon_sep
    return (hem, alt, airmass, moon_sep)

  def add_ob(self, ob, inst):
    ob_start = self.end
    self.end = ob_start + ob['executionTime'] * u.s
    trange = (self.t >= ob_start) & (self.t < self.end)
    hem, alt, airmass, moon_sep = self.calc_ob(ob)

    max_airmass = np.max(airmass[trange]) if np.any(trange) else np.inf
    min_moon_sep = np.min(moon_sep[trange]).to_value() if np.any(trange) else 0

    err = ['']
    if max_airmass > ob['constraints']['airmass']:
      err.append(f"airmass {max_airmass:.2f} > { ob['constraints']['airmass']} ")
    if min_moon_sep < ob['constraints']['moonDistance']:
      err.append(f"moon {min_moon_sep:.2f} < { ob['constraints']['moonDistance']} ")
    err = '⚠ '.join(err)
    lbl = f"{err}{hem} - {self.inst[inst]} - {ob['target']['name']}"
    self.sequence.append(
      {
        'label': lbl,
        'ok': err == '',
        'start': ob_start,
        'end': self.end,
        'trange': trange,
        'alt': alt,
        'switch': None,
        'obId': ob['obId'],
        'inst': inst,
      }
    )

  def refresh_p2(self):
    self.new_ess = [
      self.p2api.getExecutionSequence(self.inst[k])[0] for k in range(self.ninst)
    ]
    nes = sum(
      [
        [
          (ex, self.p2api.getOB(ex['obId'])[0])
          for ex in self.p2api.getNightExecutions(self.inst[k], self.night)[0]
          if ex['obStatus'] == 'X'
        ]
        for k in range(self.ninst)
      ],
      [],
    )
    self.new_nes = sorted(
      [
        (
          ob['target']['name'],
          (self.t >= Time(ex['from'])) & (self.t < Time(ex['to'])),
        )
        + self.calc_ob(ob)
        for ex, ob in nes
        if ob['itemType'] == 'OB'
      ],
      key=lambda x: x[1][0],
    )

    self.after(self.config['p2api']['update_interval_ms'], self.refresh_p2)

  def refresh_sequence(self):
    self.now = Time.now()
    if self.new_ess is not None:
      self.ess = self.new_ess
      self.nes = self.new_nes
      self.new_ess = None
      self.new_nes = None

    lens = [len(self.ess[k]) for k in range(self.ninst)]
    is_observing = False
    for k in range(self.ninst):
      if lens[k] > 0:
        if self.ess[k][0]['obStatus'] == 'S':
          if self.current_ob != self.ess[k][0]['obId'] or self.custom_start:
            self.current_ob = self.ess[k][0]['obId']
            execs, _ = self.p2api.getOBExecutions(
              self.current_ob, self.now.strftime('%Y-%m-%d')
            )
            if execs:
              self.start = Time(execs[-1]['from'])
              self.start.format = 'datetime'
            else:
              self.start = self.now
          is_observing = True
          self.custom_start = False
          self.current_inst = k
          self.next_inst = self.switch.get(self.current_ob, k)

    if self.now > self.start:
      self.custom_start = False

    if not is_observing and not self.custom_start:
      self.start = min(max(self.now, self.t[0]), self.t[-1])
      self.current_inst = self.next_inst
    inds = [0 for k in range(self.ninst)]
    inst = self.current_inst
    self.sequence = []
    self.end = self.start
    nobs = np.sum(lens)
    while len(self.sequence) < nobs:
      if lens[inst] > inds[inst]:
        if self.sequence:
          self.sequence[-1]['switch'] = (
            inst if self.sequence[-1]['inst'] != inst else None
          )
        ob = self.ess[inst][inds[inst]]
        inds[inst] += 1
        self.add_ob(ob, inst)
        if ob['obId'] in self.switch:
          inst = self.switch[ob['obId']]
      else:
        inst = (inst + 1) % self.ninst

  def redraw(self):
    self.refresh_sequence()
    self.ax.cla()
    self.ax.set_xlim(self.t[0].datetime, self.t[-1].datetime)
    self.ax.set_ylim(0, 90)
    self.ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    self.ax.set_xlabel('UT')
    self.ax.set_ylabel('Elevation (⁰)')
    for key in self.night_t:
      self.ax.fill_between(
        [self.night_t[key][0].datetime, self.night_t[key][-1].datetime],
        2 * [0],
        2 * [90],
        color=self.night_color[key],
        label=self.night_label[key],
      )
    self.ax.plot(
      self.t.datetime,
      self.moon_alt,
      '-.',
      c='blue',
      lw=2,
      label='Moon',
      rasterized=True,
    )
    self.ax.axvline(x=self.now.datetime, c='r', lw=1.5)
    for name, trange, _, alt, _, _ in self.nes:
      self.ax.plot(
        self.t.datetime,
        alt,
        '--',
        c='gray',
        lw=0.5,
        alpha=0.35,
        rasterized=True,
      )
      self.ax.plot(
        self.t.datetime[trange],
        alt[trange],
        '-',
        lw=1.5,
        alpha=0.35,
        label=f'✓ {name}',
        rasterized=True,
      )

    self.ax.text(
      (self.start + 5 * u.min).datetime,
      89,
      self.inst[self.current_inst],
      rotation='vertical',
      horizontalalignment='left',
      verticalalignment='top',
    )

    for ob in self.sequence:
      self.ax.plot(
        self.t.datetime,
        ob['alt'],
        '--',
        c='gray',
        lw=0.5,
        rasterized=True,
      )
      self.ax.plot(
        self.t.datetime[ob['trange']],
        ob['alt'][ob['trange']],
        '-' if ob['ok'] else ':',
        lw=1.5 if ob['ok'] else 3,
        label=ob['label'],
        rasterized=True,
      )
      if ob['switch'] is not None and np.any(ob['trange']):
        self.ax.axvline(x=self.t.datetime[ob['trange']][-1], c='k')
        self.ax.text(
          (self.t[ob['trange']][-1] + 5 * u.min).datetime,
          89,
          self.inst[ob['switch']],
          rotation='vertical',
          horizontalalignment='left',
          verticalalignment='top',
        )
    self.ax.legend(bbox_to_anchor=(1, 0.5), loc='center left')
    self.ax.set_title(
      f'Current time (UT): {self.now.strftime("%Y-%m-%d %H:%M:%S")}'
      + self.config['plot']['title_space'] * ' '
      + f'Start (UT): {self.start.strftime("%Y-%m-%d %H:%M:%S")}'
      + self.config['plot']['title_space'] * ' '
      + f'End (UT): {self.end.strftime("%Y-%m-%d %H:%M:%S")}'
    )
    self.fig.tight_layout()
    self.canvas.draw()
    self.after(self.config['plot']['update_interval_ms'], self.redraw)


def main():
  config = None

  paths = ['p2esm.toml', os.path.expanduser('~/.config/p2esm.toml')]
  for path in paths:
    if os.path.exists(path):
      config = tomllib.load(open(path, 'rb'))
      break

  if config is None:
    raise Exception(f'Could not find any config file in {paths}')

  P2ESM(config).mainloop()
