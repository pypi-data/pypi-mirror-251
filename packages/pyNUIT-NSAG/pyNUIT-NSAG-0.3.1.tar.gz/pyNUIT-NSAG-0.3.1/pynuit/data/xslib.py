'''
Author: albertzhang albert.zhangweij@outlook.com
Date: 2023-12-22 11:20:00
Description: 

Copyright (c) 2023 by THU-RSAG, All Rights Reserved. 
'''
import numpy as np

from re import match
from typing import List

from .classes import Reaction, Nuclide, Nuclib
from ..constants import MT_dict
from ..helpers import parse_filelines


class XSlib(Nuclib):

    def __init__(self, nuclides: List[Nuclide] = [], with_burnup: bool = False):
        self.with_burnups = with_burnup
        super().__init__('xses', nuclides)

    @classmethod
    def from_datfile(cls, filepath: str):

        xslib = cls()
        with open(filepath, 'r') as fileopen:
            filelines = fileopen.readlines()

        # read burnup table
        if (index := parse_filelines(filelines, 'BU(MWd/kgHM)')):
            xslib.with_burnups = True
            xslib.burnups = [float(bu) for bu in filelines[index+1].split()]
        else:
            xslib.with_burnups = False
            index = 0

        # count index until the xs table
        index = parse_filelines(filelines, 'NucId', index) + 1
        index_final = parse_filelines(filelines, 'NUIT fission product yield data', index) - 1 if not xslib.with_burnups else len(filelines)
        for fileline in filelines[index: index_final]:
            if (results := match(r'^(\d+)\s+([A-Za-z0-9_]+)\s+(\d+)\s*\n$', fileline)):  # nuclide line
                xslib.append(Nuclide(name=results.group(2)))
            elif results := match(r'^\s+(\d+)\s+([0-9E\-\.\+]+)\s+([0-9E\-\.\+]+)', fileline):  # reaction line
                fullMT = int(results.group(1))  # fullMT = MT + status
                Qvalue = float(results.group(2))
                if xslib.with_burnups:
                    xses = [float(xs) for xs in fileline.split()[1:]]
                else:
                    xses = float(results.group(3))
                xslib[-1].append(Reaction(MT_dict[fullMT], data={"Qvalue": Qvalue, "xses": xses}))
        xslib.nucids = [nuclide.nucid for nuclide in xslib]
        return xslib

    def to_datfile(self, filepath: str):

        fileopen = open(filepath, 'w')
        fileopen.write('*************************** NUIT one-group neutron cross-section data ***************************\n')
        fileopen.write(f'Number of isotopes with neutron data: \n\t{len(self)}\n')
        if self.with_burnups:
            fileopen.write(f'Number of burnup steps:\n\t{len(self.burnups)}\n\n')
        else:
            fileopen.write('Number of energy groups:\n\t361\n\n')

        if self.with_burnups:
            fileopen.write('BU(MWd/kgHM)\n')
            fileopen.write('   '.join([f'{burnup:<12.8E}' for burnup in self.burnups]) + '\n\n')

        if self.with_burnups:
            fileopen.write('NucId    NucName  MT\n')
            for nuclide in self:
                fileopen.write(f'{nuclide.nucid:<8d} {nuclide.name:<8s} {nuclide.num_rec:<8d}' + '\n')
                for reaction in nuclide:
                    fileopen.write(f'                  {reaction.MT:<6d}' + '   '.join([f"{xs:<12.6E}" for xs in reaction.xses]) + '\n')
        else:
            fileopen.write('NucId    NucName  MT     Qvalue         Cross section\n')
            for nuclide in self:
                fileopen.write(f'{nuclide.nucid:<8d} {nuclide.name:<8s} {nuclide.num_rec:<8d}' + '\n')
                for reaction in nuclide:
                    fileopen.write(f'                  {reaction.MT:<6d}{reaction.Qvalue:>13.6E}   {reaction.xses:<12.6E}' + '\n')

