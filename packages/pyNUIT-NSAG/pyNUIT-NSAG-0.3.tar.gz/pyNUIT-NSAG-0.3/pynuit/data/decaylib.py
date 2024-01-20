'''
Author: albertzhang albert.zhangweij@outlook.com
Date: 2023-12-20 11:56:37
Description: 

Copyright (c) 2023 by THU-RSAG, All Rights Reserved. 
'''
from re import match
from typing import List

from .classes import Nuclide, Nuclib, DecayReaction
from .xslib import XSlib
from ..helpers import parse_filelines


class DECAYlib(Nuclib):
    
    def __init__(self, nuclides: List[Nuclide] = []):
        super().__init__("decay", nuclides)

    @classmethod
    def from_datfile(cls, filepath: str):

        decaylib = cls()
        with open(filepath, 'r') as fileopen:
            filelines = fileopen.readlines()

        index = parse_filelines(filelines, 'NUIT decay library') + 1
        for fileline in filelines[index:]:
            if results := match(r"^(\d+)\s+([A-z0-9]+)\s+(\d+)\s+([0-9E\+\-\.]+)\s+([0-9E\+\-\.]+)\s+([0-9E\+\-\.]+)\s+([0-9E\+\-\.]+)", fileline):
                name = results.group(2)
                decaylib.append(Nuclide(name, data={"rate":float(results.group(4)), "Qalpha":float(results.group(5)),
                                                     "Qbeta":float(results.group(6)), "Qgamma":float(results.group(7))}))
            elif results := match(r"^\s+(\d+)\s+([0-9E\+\-\.]+)", fileline):
                decayMT = int(results.group(1))
                ratio = float(results.group(2))
                # decaylib[-1].append({'decayMT': decayMT, 'ratio': ratio})
                decaylib[-1].append(DecayReaction(decayMT, data={'ratio': ratio}))
        return decaylib