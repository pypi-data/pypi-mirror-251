import numpy as np

from re import match
from typing import List

from .classes import Reaction, Nuclide, Nuclib
from .xslib import XSlib
from ..constants import MT_dict
from ..helpers import parse_filelines


class MGXSlib(Nuclib):

    def __init__(self, nuclides: List[Nuclide] = []):
        super().__init__("mgxs", nuclides)

    def to_basic_xslib(self, fluxes: List[float], original_xslib: XSlib = None):
        xslib = XSlib()
        for nuclide in self:
            xslib.append(Nuclide(nuclide.name))
            for reaction in nuclide:
                xses = (reaction.mgxs * fluxes[reaction.start_group-1:]).sum() / fluxes.sum()
                Qvalue = original_xslib(nuclide.name)(reaction.name).Qvalue if original_xslib else 0
                xslib[-1].append(Reaction(reaction.name, data={"xses": xses, "Qvalue": Qvalue}))
        return xslib

    def to_fixed_xslib(self, flux: List[float]):
        xslib = XSlib(with_burnup=True)
        xslib.burnups = [0, 100]
        for nuclide in self:
            xslib.append(Nuclide(nuclide.name))
            for reaction in nuclide:
                xses = (reaction.mgxs * flux[reaction.start_group-1:]).sum() / flux.sum()
                xslib[-1].append(Reaction(reaction.name, data={"xses": [xses, xses]}))
        return xslib

    def to_unfixed_xslib(self, fluxes: List[List[float]], burnups: List[float]):
        xslib = XSlib(with_burnup=True)
        xslib.burnups = burnups
        for nuclide in self:
            xslib.append(Nuclide(nuclide.name))
            for reaction in nuclide:
                xses = (reaction.mgxs[np.newaxis, :] * fluxes[:, reaction.start_group-1:]).sum(axis=1) / fluxes.sum(axis=1)
                xslib[-1].append(Reaction(reaction.name, data={"xses": xses}))
        return xslib

    @classmethod
    def from_datfile(cls, filepath: str):

        mgxslib = cls()
        with open(filepath, 'r') as fileopen:
            filelines = fileopen.readlines()

        index = parse_filelines(filelines, 'NucId') + 1
        for fileline in filelines[index:]:
            if results := match(r"^(\d+)\s+([A-z0-9]+)\s+(\d+)$", fileline):
                name = results.group(2)
                mgxslib.append(Nuclide(name))
            elif results := match(r"^\s+(\d+)\s+(\d+)\s+([0-9E\-\.]+)", fileline):
                MT = int(results.group(1))
                start_group = int(results.group(2))
                xses = [float(xs) for xs in fileline.split()[2:]]
                mgxslib[-1].append(Reaction(MT_dict[MT], data={"start_group": start_group, "mgxs": np.array(xses)}))
        return mgxslib
