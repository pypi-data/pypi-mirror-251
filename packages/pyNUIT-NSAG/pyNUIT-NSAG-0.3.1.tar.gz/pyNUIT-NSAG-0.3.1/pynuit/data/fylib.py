'''
Author: albertzhang albert.zhangweij@outlook.com
Date: 2023-12-27 16:20:50
Description: 

Copyright (c) 2023 by THU-RSAG, All Rights Reserved. 
'''
from re import match
from collections import namedtuple
from typing import Union
from functools import cached_property

from .classes import Nuclib
from ..helpers import parse_filelines, decompose_nucname, convert_nucid_to_name

FYclause = namedtuple("FYclause", ["nuclide", "target", "group", "energy", "fyield"])
def __repr__(self):
    return f"{convert_nucid_to_name(self.nuclide)}->{convert_nucid_to_name(self.target)} {self.fyield}"
FYclause.__repr__ = __repr__


class FYlib(list):
    
    def __init__(self, clauses: list[FYclause] = []):
        super().__init__(clauses)

    def __call__(self, target: Union[int, str], nuclide: Union[int, str]="U235"):
        if isinstance(target, str):
            target = decompose_nucname(target)['nucid']
        if isinstance(nuclide, str):
            nuclide = decompose_nucname(nuclide)['nucid']
            
        clause = next((clause for clause in self if clause.nuclide == nuclide and clause.target == target), None)
        return clause

    @classmethod
    def from_datfile(cls, filepath: str):
        fylib = cls([])
        with open(filepath, 'r') as fileopen:
            filelines = fileopen.readlines()
        index = parse_filelines(filelines, "NUIT fission product yield data") + 4
        for i in range(index, len(filelines)):
            if (results := match(r"^(\d+)\s+([A-z0-9]+)\s+(\d+)\s+(\d)\s+$", filelines[i])):
                nuclide = decompose_nucname(results.group(2))['nucid']
                group = int(results.group(4))
                energy = [float(val) for val in filelines[i+1].split()]
            elif (results := match(r"^\s+(\d+)\s+([A-z0-9\.\+\-]+)\s+", filelines[i])):
                target = int(results.group(1))
                fyield = [float(val) for val in filelines[i].split()[1:]]
                fylib.append(FYclause(nuclide, target, group, energy, fyield))
        return fylib
