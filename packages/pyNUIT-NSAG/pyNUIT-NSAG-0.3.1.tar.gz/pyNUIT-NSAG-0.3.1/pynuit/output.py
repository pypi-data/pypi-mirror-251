import numpy as np

from typing import Any, List, Union

from .helpers import parse_filelines


class Output():
    """
    container for NUIT Output file.

    Attributes:
        filelines (list): List of strings representing the lines of the output file.
        nuclide_masses (list): List of dictionaries containing nuclide information, including nuclide ID, name, and data.
        burnups (ndarray): Array of burnup values.
        powers (ndarray): Array of power values.
        timesteps (ndarray): Array of timestep values.
        fluxes (ndarray): Array of flux values.

    Methods:
        __init__(filepath): Initializes the Output object by reading the file and parsing the data.
        _read_isotopes(): Parses the nuclide density data from the file.
        _read_burnups(): Parses the burnup data from the file.
        _read_powers(): Parses the power data from the file.
        _read_timesteps(): Parses the timestep data from the file.
        _read_fluxes(): Parses the flux data from the file.
        match(key, value, type): Matches an element from the stored tables using a key-value pair.
        get_nuclide_mass(nuclide, burnup): Gets the nuclide mass at a certain burnup depth.
        output_nuclide_mass(nuclide_list, burnup): Gets the nuclide mass in batch.
    """

    def __init__(self, filepath) -> None:
        """
        Initialize the Output object.

        Args:
            filepath (str): The path to the file to be read.
        """
        with open(filepath) as fileopen:
            self.filelines = fileopen.readlines()
        
        # to avoid format diffenrence when print_all_steps=0/1
        try:
            self._read_burnups()
            self._read_powers()
            self._read_timesteps()
            self._read_fluxes()
        except:
            self._read_info_two_steps()
            pass
        self._read_isotopes()

    def _read_info_two_steps(self) -> None:
        index = parse_filelines(self.filelines, 'Nuclide Density(n*1.0E+24) Table, Instantaneous', 0) + 3
        self.timesteps = [float(t) for t in self.filelines[index].split()[2::3]]
        self.fluxes = [float(t) for t in self.filelines[index+1].split()[2::3]]
        self.powers = [float(t) for t in self.filelines[index+2].split()[2::3]]
        self.burnups = [float(t) for t in self.filelines[index+3].split()[2::3]]

    def _read_isotopes(self) -> None:
        """
        Extracts the nuclide information, including nuclide ID, name, and data, from the filelines and stores them in the `nuclide_masses` attribute.
        
        Returns:
            None
        """
        self.nuclide_masses = []
        index = parse_filelines(self.filelines, 'Nuclide Density', 0) + 1
        index = parse_filelines(self.filelines, 'NucID', index) + 2
        while "Non-Actinide" not in self.filelines[index]:
            line = self.filelines[index].split()
            nuc_id, nuc_name = int(line[0]), line[1]
            nuc_den = np.asarray([float(item) for item in line[2:]])
            self.nuclide_masses.append({'nucid': nuc_id,
                                        'name': nuc_name,
                                        'data': nuc_den})
            index += 1

    def _read_burnups(self) -> None:
        """
        Extracts the burnup values from the filelines and stores them in the `burnups` attribute.

        Returns:
            None
        """
        self.burnups = []
        ind = parse_filelines(self.filelines, 'BU(MWd/kgHM):', 0)
        line = self.filelines[ind].split()
        for bu in line[1:]:
            self.burnups.append(float(bu))
        self.burnups = np.asarray(self.burnups)

    def _read_powers(self) -> None:
        """
        Reads the power values from the filelines and stores them in the powers attribute.

        Returns:
            None
        """
        self.powers = []
        ind = parse_filelines(self.filelines, 'Power(MW):', 0)
        line = self.filelines[ind].split()
        for pw in line[1:]:
            self.powers.append(float(pw))
        self.powers = np.asarray(self.powers)

    def _read_timesteps(self) -> None:
        """
        Reads the timesteps from the filelines and stores them in the `timesteps` attribute.

        Returns:
            None
        """
        self.timesteps = []
        ind = parse_filelines(self.filelines, 'TotalTime(s):', 0)
        line = self.filelines[ind].split()
        for ts in line[1:]:
            self.timesteps.append(float(ts))
        self.timesteps = np.asarray(self.timesteps)

    def _read_fluxes(self) -> None:
        """
        Reads the fluxes from the filelines and stores them in the 'fluxes' attribute.
        
        Returns:
            None
        """
        self.fluxes = []
        ind = parse_filelines(self.filelines, 'Flux(n/cm^2/s):', 0)
        line = self.filelines[ind].split()
        for fl in line[1:]:
            self.fluxes.append(float(fl))
        self.fluxes = np.asarray(self.fluxes)

    def match(self, key='name', value='Cs137', type='nuclide') -> Any:
        """
        Match an element from stored tables using key-value pair.
        
        Returns:
            Any: Depends on the type of the table.
        """
        if type == 'nuclide':
            table = self.nuclide_masses
        elif type == 'burnup':
            table = self.burnups
        val = next((item for item in table if item[key] == value), None)
        return val

    def get_nuclide_mass(self, nuclide: str, burnup: float = None) -> Union[float, List[float]]:
        """"
        Get nuclide mass at a certain burnup depth.
        
        Returns:
            mass (Union(float, List[float])): Nuclide mass at a certain burnup depth.
        """
        if burnup:
            return self.match('name', nuclide, 'nuclide')[abs(self.burnups-burnup).argmin()]
        else:
            return self.match('name', nuclide)['data']

    def output_nuclide_mass(self, nuclide_list, burnup=None) -> List[float]:
        """
        Get nuclide mass in batch.
        
        Returns:
            mass (List[float]): Nuclide mass in batch.
        """
        return [self.get_nuclide_mass(nuclide, burnup) for nuclide in nuclide_list]
