'''
Author: albertzhang albert.zhangweij@outlook.com
Date: 2023-12-22 11:20:00
Description: 

Copyright (c) 2023 by THU-RSAG, All Rights Reserved. 
'''

from typing import List, Union, Any
from functools import cached_property
from ..constants import MT_dict, Atomic_list, MT_to_nucid_dict, particle_dict
from ..helpers import decompose_nucname


class Reaction():

    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data

    @cached_property
    def fullMT(self):
        return MT_dict[self.name]
    
    @cached_property
    def MT(self):
        if 'm1' in self.name:
            return MT_dict[self.name[:-2]]
        return MT_dict[self.name]

    @cached_property
    def status(self):
        return int(self.name[:-2] == 'm1')

    @cached_property
    def varid(self):
        return (MT_to_nucid_dict[self.MT], self.status)

    def __repr__(self):
        return self.name

    def __getattr__(self, attr: str):
        if attr in self.data:
            return self.data[attr]
        else:
            return None


class DecayReaction:
    
    def __init__(self, decayMT: int, data: dict):
        self.decayMT = decayMT
        self.data = data

    @staticmethod
    def help():
        return "DecayReaction(decayMT, data={'ratio':float})"
        
    @cached_property
    def name(self):
        name = '(' + '|'.join([particle_dict[int(char)][0] for char in str(self.decayMT)[:-1] if char != '0']) + ')'
        name += f'm{self.decayMT%10}' if self.decayMT%10 != 0 else ''
        return name

    @cached_property
    def status(self):
        return self.decayMT % 10

    @cached_property
    def varid(self):
        varid = sum([particle_dict[int(char)][1] for char in str(self.decayMT)[:-1] if char != '0'])
        return (varid, self.status)

    def __repr__(self):
        return self.name

    def __getattr__(self, attr: str):
        if attr in self.data:
            return self.data[attr]
        else:
            return None


class Nuclide(list):

    def __init__(self, name: str, reaction: List[Union[Reaction, DecayReaction]] = [], data: dict = None):
        self.name = name
        self.data = data
        super().__init__(reaction)

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name + super().__repr__()

    def __getattr__(self, attr: str):
        if attr in self.data:
            return self.data[attr]
        else:
            return None

    @staticmethod
    def help():
        return "Nuclide(name, reaction=[Reaction, DecayReaction], data={'rate':float, 'Qalpha':float, 'Qbeta':float, 'Qgamma':float}"

    @cached_property
    def nucid(self):
        return decompose_nucname(self.name)["nucid"]

    @cached_property
    def mass(self):
        return decompose_nucname(self.name)["mass"]
    
    @cached_property
    def atomic(self):
        return decompose_nucname(self.name)["atomic"]

    @property
    def num_rec(self):
        return len(self)

    def __call__(self, reaction: Union[str, int]) -> Union[Reaction, DecayReaction]:
        rec_index = 'name' if isinstance(reaction, str) else 'MT'
        return next(reactioni for reactioni in self if getattr(reactioni, rec_index) == reaction)

    def sort_reactions(self):
        self.sort(key=lambda reaction: reaction.MT)

    def transmute_by_reaction(self, reaction: Union[Reaction, DecayReaction]):
        target = self.nucid + reaction.varid[0] * 10
        target = target // 10 * 10 + reaction.varid[1]
        return target
    
    def transmute_by_varid(self, varid: tuple):
        target = self.nucid + varid[0] * 10
        target = target // 10 * 10 + varid[1]
        return target

    def transmute(self):
        return [self.transmute_by_reaction(reaction) for reaction in self]

    def decay(self):
        return [self.transmute_by_reaction(decayreaction) for decayreaction in self]
    
class Nuclib(list):

    def __init__(self, type: str, nuclides: List[Nuclide] = []):
        self.type = type
        super().__init__(nuclides)

    def __call__(self, nuclide: Union[str, int]) -> Nuclide:
        """
        Returns the first instance of a nuclide in the class that matches the given nuclide name or ID.

        Parameters:
        - nuclide: A string representing the name of the nuclide or an integer representing the nuclide ID.

        Returns:
        - The first instance of the nuclide found in the class.

        Raises:
        - StopIteration: If no matching nuclide is found in the class.
        """
        nuc_index = 'name' if isinstance(nuclide, str) else 'nucid'
        return next(nuclidei for nuclidei in self if getattr(nuclidei, nuc_index) == nuclide)

    def sort_nuclides(self):
        self.sort(key=lambda nuclide: nuclide.nucid)
