from unittest import TestCase
import os
from src.save_structures import SaveStructures
import yaml

with open(os.path.join('data', 'aws.yaml')) as f:
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)

db_url = db_yaml['db']
launchpad_path = os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml')


class TestSaveStructures(TestCase):
    def test_save(self):
        save_structures = SaveStructures(db_path=db_url, launchpad_path=launchpad_path)
        save_structures.save()

