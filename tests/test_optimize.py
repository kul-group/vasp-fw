import subprocess
from unittest import TestCase
from vaspfw.optimize import OptimizeWithVaps
import os
from ase.db import connect
from ase.io import read
from fireworks import ScriptTask
import yaml

with open(os.path.join('data', 'aws.yaml')) as f:
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)

db_url = db_yaml['db']
launchpad_path = os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml')

calc_spec = {"encut": 400}
spec = {"database_path": db_url,
        "input_id": 1,
        "calculation_type": "dry_run",
        "calc_spec": calc_spec,
        "structure_type": "zeo"}


class TestOptimizeWithVaps(TestCase):
    def assert_atoms_equal(self, atoms1, atoms2):
        for a1, a2 in zip(atoms1, atoms2):
            self.assertEqual(a1.symbol, a2.symbol)
            for p1, p2 in zip(a1.position, a2.position):
                self.assertEqual(p1, p2)

    def test_init(self):
        folder_path = str(os.path.join(os.getcwd(), 'data', 't29_tmpo'))
        lpad_path = str(os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml'))
        opt_vasp = OptimizeWithVaps(folder_path=folder_path,
                                    file_format="traj",
                                    db_path=db_url,
                                    specs=[spec],
                                    launchpad_path=launchpad_path,
                                    reset_launchpad=True)

        self.assertEqual(opt_vasp.folder_path, folder_path)
        self.assertEqual(opt_vasp.file_format, 'traj')
        self.assertEqual(opt_vasp.launchpad_path, lpad_path)
        self.assertEqual(opt_vasp.db_path, db_url)
        self.assertTrue(opt_vasp.db)
        self.assertEqual(opt_vasp.fireworks_dict_path, 'fireworks_dict.json')
        self.assertDictEqual(opt_vasp.specs[0], spec)
        self.assertEqual(opt_vasp.reset_launchpad, True)

    def test_get_atom_file_list(self):
        folder_path = str(os.path.join(os.getcwd(), 'data', 't29_tmpo'))
        opt_vasp = OptimizeWithVaps(folder_path=folder_path,
                                    file_format="traj",
                                    db_path=db_url,
                                    specs=[spec],
                                    launchpad_path=launchpad_path,
                                    reset_launchpad=True)
        cmd = f'find "$(pwd)" -maxdepth 6 -path "*{folder_path}*" -name "*.traj" > output/test.txt'
        subprocess.run(cmd, shell=True, universal_newlines=True, check=True)
        with open('output/test.txt') as f:
            file_list = [line.strip() for line in f.readlines()]

        program_filelist = opt_vasp.get_atom_file_list()
        self.assertCountEqual(file_list, program_filelist)

    def test_add_atom_files_to_db(self):
        output_db = "output/test.db"
        if os.path.isfile(output_db):
            os.remove(output_db)

        folder_path = str(os.path.join(os.getcwd(), 'data', 't29_tmpo'))
        lpad_path = str(os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml'))
        opt_vasp = OptimizeWithVaps(folder_path=folder_path,
                                    file_format="traj",
                                    db_path=output_db,
                                    specs=[spec],
                                    launchpad_path=launchpad_path,
                                    reset_launchpad=True)

        output = opt_vasp.add_atom_files_to_db(opt_vasp.get_atom_file_list())
        output_dict = {}
        db = connect(output_db)
        with self.subTest('test db atoms added'):
            for index, file_path in enumerate(opt_vasp.get_atom_file_list()):
                db_atoms = db.get_atoms(index + 1)
                read_atoms = read(file_path)
                output_dict[index + 1] = file_path
                self.assert_atoms_equal(db_atoms, read_atoms)

        with self.subTest('test correct output dict'):
            self.assertDictEqual(output_dict, output)

    def test_create_simple_workflow(self):
        spec_list = []
        for i in range(10):
            my_dict = {'script': 'echo hello!'}
            spec_list.append(my_dict)
        output = OptimizeWithVaps.create_simple_workflow(spec_list, ScriptTask)
        print(output.as_dict())

    def test_run(self):
        # TODO: Find a way to test this fun currently running it works
        folder_path = str(os.path.join(os.getcwd(), 'data', 't29_tmpo'))

        opt_vasp = OptimizeWithVaps(folder_path=folder_path,
                                    file_format="traj",
                                    db_path=db_url,
                                    specs=[spec],
                                    launchpad_path=launchpad_path,
                                    reset_launchpad=True)

        opt_vasp.submit()

    def test_run(self):
        # TODO: Find a way to test this fun currently running it works
        folder_path = str(os.path.join(os.getcwd(), 'data', 'water'))

        opt_vasp = OptimizeWithVaps(folder_path=folder_path,
                                    file_format="traj",
                                    db_path=db_url,
                                    specs=[spec],
                                    launchpad_path=launchpad_path,
                                    reset_launchpad=True)

        opt_vasp.submit()
