 ## Tutorial  
### Submitting a folder of .traj files for optimization 

Create a folder of folders containing the .traj files that you wish to optimize. For example 

    tree 
    sn_bea_tmpo_structures
    ├── 00_closed
    │   ├── 01SnBea
    │   │   └── bea_structure_unopt.traj
    │   ├── 02SnBea
    │   │   └── bea_structure_unopt.traj
    │   ├── 03SnBea
    │   │   └── bea_structure_unopt.traj
    │   ├── 04SnBea
    │   │   └── bea_structure_unopt.traj
    │   ├── 07SnBea
    │   │   └── bea_structure_unopt.traj
    │   ├── 08SnBea
    │   │   └── bea_structure_unopt.traj
    │   └── 09SnBea
    │       └── bea_structure_unopt.traj
    └── 02_open2
        ├── 01_Sn
        │   └── bea_structure_unopt.traj
        ├── 02_Sn
        │   └── bea_structure_unopt.traj
        ├── 03_Sn
        │   └── bea_structure_unopt.traj
        ├── 04_Sn
        │   └── bea_structure_unopt.traj
        ├── 07_Sn
        │   └── bea_structure_unopt.traj
        ├── 08_Sn
        │   └── bea_structure_unopt.traj
        ├── 09_Sn
        │   └── bea_structure_unopt.traj
        └── bea_structure_unopt.traj

### Next determine the workflow for the optimization 

Here is an example workflow 
1. Pre-opt bare zeolite – Single point for each ENCUT iterations, ENCUT (300, 400, …., 700)  
2. 1Al, 2Al zeolites – unconstrained opt, 50~100 steps for each ENCUT iterations, ENCUT (x, x, 700)  
3. EF/BronstedH/Defect zeolites – constrained opt, pre-opt with FF, 30~50 steps for each ENCUT iterations, ENCUT (x, x, 700)

### Create a spec dictionary for each step of this process  

Here is an example spec 
```python
spec1 = {"is_zeolite": True,  
        "database_path": db_url,  
        "input_id": 1,  
        "nsw": 1,  
        "my_nsw": 1,  
        "encut": 520.0,  
        "kpts": (1, 1, 1),  
        "ivdw": 12,  
        "isif": 2}
```

### Use vasp-fw to submit all files for the same optimization 
This is an example script makes the same workflow for all of the traj files in the folder, and submits the workflow to the fireworks launchpad. 
```python
import os  
import yaml  
from ase.io import read, write  
from vaspfw.optimize import OptimizeWithVaps  

with open(os.path.join('data', 'aws.yaml')) as f:  
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)  

db_url = db_yaml['db']  
launchpad_path = os.path.join(os.getcwd(), 'data', 'my_launchpad.yaml')  
folder_path = "sn_bea_tmpo_structures" 

spec1 = {"is_zeolite": True,  
        "database_path": db_url,  
        "input_id": 1,  
        "nsw": 1,  
        "my_nsw": 1,  
        "encut": 400.0,  
        "kpts": (1, 1, 1),  
        "ivdw": 12,  
        "isif": 2}  

spec2 = {"is_zeolite": True,  
        "database_path": db_url,  
        "input_id": 1,  
        "nsw": 1,  
        "my_nsw": 1,  
        "encut": 600.0,  
        "kpts": (1, 1, 1),  
        "ivdw": 12,  
        "isif": 2}  

spec3 = {"is_zeolite": True, 
        "database_path": db_url,  
        "input_id": 1,  
        "nsw": 1,  
        "my_nsw": 1,  
        "encut": 800.0,  
        "kpts": (1, 1, 1),  
        "ivdw": 12,  
        "isif": 2}  

specs = [spec1, spec2, spec3]
opt_vasp = OptimizeWithVaps(folder_path=folder_path,  
                            file_format="traj",  
                            db_path=db_url,  
                            specs=specs,  
                            launchpad_path=launchpad_path,  
                            reset_launchpad=True)  

opt_vasp.submit()
```

The jobs have now been submitted to fireworks. Now you can go to your remote computer and use `qlaunch` to submit all of your jobs. 

Once these jobs are done, you can now put the optimized structures into your original folder structure. To do this use the `SaveStructures` class in the `save_results` file. 

```python
import os  
from vaspfw.save_structures import SaveStructures  
import yaml  

with open(os.path.join('data', 'aws.yaml')) as f:  
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)  

db_url = db_yaml['db']  
launchpad_path = os.path.join(os.getcwd(), 'data', 'my_launchpad_backup.yaml')  

save_structures = SaveStructures(db_path=db_url, launchpad_path=launchpad_path)  
save_structures.save()
```

This function prints out confirmations for each successful save and failure, but does not throw exceptions. After running this file check out your original folder structure. You should see an additional, optimized file in each folder. 
```
├── sn_bea_tmpo_structures
│   ├── 00_closed
│   │   ├── 01SnBea
│   │   │   ├── opt_from_vasp.traj
│   │   │   └── optimized.traj
│   │   ├── 02SnBea
│   │   │   ├── opt_from_vasp.traj
│   │   │   └── optimized.traj
│   │   ├── 03SnBea
│   │   │   ├── opt_from_vasp.traj
│   │   │   └── optimized.traj
│   │   ├── 04SnBea
│   │   │   ├── opt_from_vasp.traj
│   │   │   └── optimized.traj
│   │   ├── 07SnBea
│   │   │   ├── opt_from_vasp.traj
│   │   │   └── optimized.traj
│   │   ├── 08SnBea
│   │   │   ├── opt_from_vasp.traj
│   │   │   └── optimized.traj
│   │   └── 09SnBea
│   │       ├── opt_from_vasp.traj
│   │       └── optimized.traj
│   └── 02_open2
│       ├── 01_Sn
│       │   ├── opt_from_vasp.traj
│       │   └── optimized.traj
│       ├── 02_Sn
│       │   ├── opt_from_vasp.traj
│       │   └── optimized.traj
│       ├── 03_Sn
│       │   └── opt_from_vasp.traj
│       ├── 04_Sn
│       │   ├── opt_from_vasp.traj
│       │   └── optimized.traj
│       ├── 07_Sn
│       │   ├── opt_from_vasp.traj
│       │   └── optimized.traj
│       ├── 08_Sn
│       │   ├── opt_from_vasp.traj
│       │   └── optimized.traj
│       ├── 09_Sn
│       │   ├── opt_from_vasp.traj
│       │   └── optimized.traj
│       ├── opt_from_vasp.traj
│       └── optimized.traj
```
