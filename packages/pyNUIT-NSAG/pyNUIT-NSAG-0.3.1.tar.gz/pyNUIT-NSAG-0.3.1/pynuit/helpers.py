from typing import List, Literal
from re import match
from .constants import time_convert_units, Atomic_dict, Atomic_list

def parse_filelines(filelines: List[str], target: str, start_index: int = 0):
    index = start_index
    filelen = len(filelines)
    while target not in filelines[index]:
        index += 1
        if index == filelen:
            return None
    return index

def convert_time(time, unit1, unit2):
    return time * time_convert_units[unit1] / time_convert_units[unit2]


def decompose_nucname(nucname, style: Literal['NUIT', 'OpenMC'] = 'NUIT'):
    if style == 'NUIT':
        pattern = r'^([a-zA-Z]+)(\d+)_?(m[123])?$'
    elif style == 'OpenMC':
        pattern = r'^([a-zA-Z]+)(\d+)?(m)?$'
    match_results = match(pattern, nucname)

    if match_results is None:
        return None
    else:
        match_results = match_results.groups()

    symbol = match_results[0]
    mass = int(match_results[1])
    state = 0 if match_results[2] is None else int(match_results[2][1])
    atomic = Atomic_dict[symbol]
    nucid = atomic * 10000 + mass * 10 + state

    nuc_info = {'symbol': symbol, 'mass': mass, 'state': state, 'atomic': atomic, 'nucid': nucid}
    return nuc_info

def convert_nucid_to_name(nucid: int):
    atomic = nucid // 10000
    mass = nucid // 10 % 1000
    state = nucid % 10
    symbol = Atomic_list[atomic]
    name = f'{symbol}{mass}'
    if state != 0:
        name += f'm{state}'
    return name
