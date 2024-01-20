import numpy as np
import matplotlib.pyplot as plt

from typing import Literal, List
from copy import deepcopy
from time import mktime, strptime, struct_time

from . import model


class Histogram:

    def __init__(self, times: List[str], powers: List[float], mode: Literal['constpower', 'constflux'] = 'constpower', model: model.Model = None):
        self.times = times
        self.powers = np.array(powers)
        self.model = model
        self.mode = mode

    def __add__(self, histogram):
        return Histogram(self.times + histogram.times, np.concatenate([self.powers, histogram.powers]))

    def __mul__(self, ratio):
        return Histogram(self.times, self.powers * ratio)

    def __truediv__(self, ratio):
        return Histogram(self.times, self.powers / ratio)

    @property
    def stamps(self):
        return np.array([mktime(strptime(time, "%Y-%m-%d %H:%M")) for time in self.times])

    @property
    def time_lengths(self):
        return self.stamps[1:] - self.stamps[:-1]

    @property
    def average_powers(self):
        return (self.powers[:-1, 1] + self.powers[1:, 0]) / 2

    @property
    def burnup(self):
        return sum(self.time_lengths * self.average_powers)

    @burnup.setter
    def burnup(self, burnup):
        self.powers *= burnup / self.burnup

    def copy(self):
        return deepcopy(self)

    def get_power(self, time) -> float:
        if isinstance(time, struct_time):
            time = mktime(time)
        if (time <= self.stamps[0]) or (time >= self.stamps[-1]):
            return 0
        else:
            index = np.argwhere(self.stamps < time)[-1][0]
            init_time = self.stamps[index]
            final_time = self.stamps[index+1]
            init_power = self.powers[index][1]
            final_power = self.powers[index+1][0]
            power = (time - init_time) / (final_time - init_time) * (final_power - init_power) + init_power  # linear interpolation
            return power

    def plot_power(self, time_length=10, axes: plt.Axes = None) -> plt.Axes:
        if axes is None:
            _, axes = plt.subplots(figsize=(20, 3))
        times = np.linspace(self.stamps[0], self.stamps[-1], int((self.stamps[-1] - self.stamps[0])/(86400*time_length)))
        powers = [self.get_power(time) for time in times]
        axes.plot(times, powers, ".-", markersize=10)
        axes.set_xticks(self.stamps, self.times, rotation=90)
        axes.set_ylim(0, )
        return axes

    def to_model(self, step_length: float = 10 * 86400):

        self.model.remove_node("burnup")
        for i in range(len(self.stamps)-1):
            repeat = int((self.stamps[i+1]-self.stamps[i]) / step_length) + 1
            step_length_exact = (self.stamps[i+1]-self.stamps[i]) / repeat
            if self.powers[i][1] != 0 or self.powers[i+1][0] != 0:
                if self.powers[i][1] == self.powers[i+1][0]:
                    self.model.add_burnup(mode=self.mode,
                                          time=step_length_exact,
                                          val=self.powers[i][1],
                                          repeat=repeat,
                                          unit='second')
                else:
                    for j in range(repeat):
                        self.model.add_burnup(mode=self.mode,
                                              time=step_length_exact,
                                              val=self.get_power(self.stamps[i]+step_length_exact*(j+1/2)),
                                              unit='second')
            else:
                self.model.add_burnup(mode='decay',
                                      time=step_length_exact,
                                      val=0,
                                      repeat=repeat,
                                      unit='second')
        return self.model
