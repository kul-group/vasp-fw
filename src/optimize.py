import copy
import json
from pathlib import Path
from typing import List, Dict

import yaml
from ase.db import connect
from ase.io import read
from fireworks import Firework, LaunchPad, Workflow
from vasp_fw.vasp_db import VASPDB


class OptimizeWithVaps:
    """
    This class manages submitting a folder of traj (or other VASP compatible files) to a fireworks
    so that they can be run on a remote server.
    """
    def __init__(self, folder_path: str, file_format: str, db_path: str, specs: List[Dict], launchpad_path: str, reset_launchpad=True, fireworks_dict_path=None):
        """
        Initilize a OptimizeWithVASP object
        :param folder_path: path to folder containing specified files
        :type folder_path: str
        :param file_format: extension (not containing '.')
        :type file_format: str
        :param db_path: database path or connection string
        :type db_path: str
        :param specs: dictionary of specs for vasp optimization
        :type specs: Dict
        :param launchpad_path: path to launchpad
        :type launchpad_path: str
        :param reset_launchpad: reset the launchpad and clear existing rockets? (default True)
        :type reset_launchpad: bool
        :param fireworks_dict_path: path to fireworks dictionary mapping file paths to json
        :type fireworks_dict_path: str
        """

        self.folder_path = folder_path
        assert '.' not in file_format, 'do not include "." in file_format arg'
        self.file_format = file_format
        self.db_path = db_path
        self.db = connect(db_path)
        self.specs = specs
        self.launchpad_path = launchpad_path
        self.reset_launchpad = reset_launchpad
        
        if not fireworks_dict_path:
            self.fireworks_dict_path = 'fireworks_dict.json'
        else:
            self.fireworks_dict_path = fireworks_dict_path 
 
    def get_atom_file_list(self) -> List[str]:
        """
        Get list of all of the files with the specified traj in the specified directory
        :return: list of filepaths of atoms-like searilizations (e.g. .traj files)
        :rtype: List[str]
        """
        paths = Path(self.folder_path).rglob('*' + '.' + self.file_format)
        return [str(p) for p in paths]
    
    def add_atom_files_to_db(self, filelist: List[str]) -> Dict:
        """
        Add all of the atom files to the db
        :param filelist: filelist of atoms to add to database
        :type filelist: mapping between db ids and filelist
        :return: mapping between db ids and filelist
        :rtype:
        """
        filelist_dict = {}
        for file in filelist:
            atoms = read(file)
            index = self.db.write(atoms)
            filelist_dict[index] = file

        return filelist_dict


    @staticmethod
    def create_simple_workflow(spec_list, firework_class, name=None):
        if name is None:
            name = "vasp_opt"
        fw_list = []
        for spec in spec_list:
            fw_list.append(Firework(firework_class(**spec), spec=spec))
        workflow_dict = {}
        for i in range(len(fw_list)):
            if i + 1 < len(fw_list):
                workflow_dict[fw_list[i]] = fw_list[i+1]
        
        return Workflow(fw_list, workflow_dict, name=name)

    
    def run(self, workflow_fun=None):
        filelist = self.get_atom_file_list()
        filelist_dict = self.add_atom_files_to_db(filelist)

        with open(self.launchpad_path) as file:
            con_params = yaml.load(file, Loader=yaml.FullLoader)
        launchpad = LaunchPad(**con_params)
        if self.reset_launchpad:
            launchpad.reset('', require_password=False)
        if workflow_fun is None: 
            workflow_fun = self.create_simple_workflow
        
        fireworks_dict = {}
        for id in filelist_dict.keys():
            specs_copy = copy.deepcopy(self.specs)
            for spec in specs_copy:
                print(id)
                spec['input_id'] = id
                spec['database_path'] = self.db_path

            wf = workflow_fun(specs_copy, VASPDB, name='vasp_opt' + str(id))
            launchpad.add_wf(wf)
            fireworks_dict[id] = [filelist_dict[id], [fw.fw_id for fw in wf.fws]]

        with open(self.fireworks_dict_path, 'w') as f:
            json.dump(fireworks_dict, f)