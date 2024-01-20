'''
Author: albertzhang albert.zhangweij@outlook.com
Date: 2023-12-22 11:20:00
Description: 

Copyright (c) 2024 by THU-RSAG, All Rights Reserved. 
'''
from pickle import load
from collections import namedtuple
from typing import Union

from ..helpers import decompose_nucname, convert_nucid_to_name
from ..constants import MT_dict

ISOclause = namedtuple("ISOclause", ["nucid", "MT", "fracm"])
def __repr__(self):
    return f"{convert_nucid_to_name(self.nucid)} {self.MT}: {self.fracm}"
ISOclause.__repr__ = __repr__

class ISOlib(list):

    def __init__(self, clauses: list[ISOclause] = []):
        super().__init__(clauses)

    def __call__(self, nuclide: Union[str, int], reaction: Union[str, int]):
        if isinstance(reaction, str):
            reaction = MT_dict[reaction]
        if isinstance(nuclide, str):
            nuclide = decompose_nucname(nuclide)['nucid']
        clause = next((clause for clause in self if getattr(clause, 'nucid') == nuclide and getattr(clause, 'MT') == reaction))
        return clause

    @classmethod
    def from_pickle(cls, filepath: str):
        
        with open(filepath, 'rb') as fileopen:
            isomerics = load(fileopen)
        isolib = ISOlib([ISOclause(iso['nucid'], iso["MT"], iso["fracm"]) for iso in isomerics])
        return isolib
