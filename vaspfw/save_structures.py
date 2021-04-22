import json
from pathlib import Path

import yaml
from ase.db import connect
from ase.io import read, write
from fireworks import LaunchPad


class SaveStructures:
    """
    Fireworks added optimized structures to a database. This class then loads the optimized structures
    from that database and saves them in the original file structure from which they originated.
    """
    def __init__(self, db_path: str, launchpad_path: str, output_filename='optimized.traj', fireworks_dict_path=None):
        """
        This initializes the save structures class
        :param db_path: path to the database (can be an AWS connection string)
        :type db_path: str
        :param launchpad_path: path to fireworks launchpad
        :type launchpad_path: str
        :param output_filename: the name of the filename in which to save the output (default 'optimized.traj')
        :type output_filename: str
        :param fireworks_dict_path: path to dictionary mapping indices to structures
        :type fireworks_dict_path: str
        """
        self.new_filename = output_filename
        self.db = connect(db_path)
        if not fireworks_dict_path:
            self.fireworks_dict_path = 'fireworks_dict.json'
        else:
            self.fireworks_dict_path = fireworks_dict_path

        with open(self.fireworks_dict_path) as f:
            self.fireworks_dict = json.load(f,
                                            object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v
                                                                   in d.items()})

        with open(launchpad_path) as file:
            con_params = yaml.load(file, Loader=yaml.FullLoader)
        self.launchpad = LaunchPad(**con_params)

    def save(self) -> None:
        """
        Attempts to save the optimized structures to the folder structure.
        Errors are not thrown, but instead printed.
        :return: None
        :rtype: None
        """
        for filename, fireworks in self.fireworks_dict.values():
            new_filename = Path(filename).parents[0] / self.new_filename
            final_structure_id = \
            fw_dict = self.launchpad.get_fw_by_id(fireworks[-1]).as_dict()
            try:
                final_structure_id = fw_dict['launches'][0]['action']['stored_data']['output_index']
                atoms = self.db.get_atoms(final_structure_id)
                write(new_filename, atoms)
                print(f"wrote {new_filename}")
            except Exception as e:
                print(f'failed to write {new_filename}')
                print(repr(e))
