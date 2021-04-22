"""
This file loads optimization results from the atoms database and saves them in the original folder structure
from which the unoptimized structures were taken
"""
import os
from vaspfw.save_structures import SaveStructures
import yaml

if __name__ == "__main__":
    with open(os.path.join('data', 'aws.yaml')) as f:
        db_yaml = yaml.load(f, Loader=yaml.FullLoader)

    db_url = db_yaml['db']
    launchpad_path = os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml')

    save_structures = SaveStructures(db_path=db_url, launchpad_path=launchpad_path)
    save_structures.save()
