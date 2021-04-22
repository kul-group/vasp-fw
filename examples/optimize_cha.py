"""
This file optimizes a CHA structure by submitting the job to fireworks
"""
import os

import yaml
from ase.io import read, write

from vaspfw.optimize import OptimizeWithVaps

if __name__ == "__main__":
    with open(os.path.join('data', 'aws.yaml')) as f:
        db_yaml = yaml.load(f, Loader=yaml.FullLoader)

    db_url = db_yaml['db']
    launchpad_path = os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml')

    cha = read(os.path.join(os.getcwd(), 'tests','data','CHA.cif'))
    write(os.path.join('data', 'cha','cha.traj'), cha)
    folder_path = str(os.path.join(os.getcwd(), 'data', 'cha'))
    spec = {"is_zeolite": True,
            "database_path": db_url,
            "input_id": 1,
            "nsw": 1,
            "my_nsw": 1,
            "encut": 520.0,
            "kpts": (1, 1, 1),
            "ivdw": 12,
            "isif": 2}

    opt_vasp = OptimizeWithVaps(folder_path=folder_path,
                                file_format="traj",
                                db_path=db_url,
                                specs=[spec],
                                launchpad_path=launchpad_path,
                                reset_launchpad=True)

    opt_vasp.submit()
