
# VASP-FW 
### Bridging the gap between VASP and fireworks    
This package bridges fireworks and ASE/VASP/MAZE-sim so that jobs can easily be submitted.   
 ## Installation
1. Activate your fireworks conda environment ``source activate fw37``
2. Clone the repo, navigate into it, and install the package in developer/editible mode 
```bash
git clone https://github.com/kul-group/vasp-fw.git
cd vasp-fw
pip install -e . 
```
 
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

calc_spec = {"encut": 400}
spec = {"database_path": db_url,
        "input_id": 1,
        "calculation_type": "alchemy",
        "calc_spec": calc_spec,
        "structure_type": "zeo"}
```

### Use vasp-fw to submit all files for the same optimization 
This is an example script makes the same workflow for all of the traj files in the folder, and submits the workflow to the fireworks launchpad. The test run case alchemy is used, which converts all of the structures to gold. 
```python
import os  
import yaml  
from ase.io import read, write  
from vaspfw.optimize import OptimizeWithVaps  

with open(os.path.join('aws.yaml')) as f:  
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)  

db_url = db_yaml['db']  
launchpad_path = os.path.join(os.getcwd(), 'my_launchpad.yaml')  
folder_path = "structures" 

calc_spec = {"encut": 400}
spec = {"database_path": db_url,
        "input_id": 1,
        "calculation_type": "alchemy",
        "calc_spec": calc_spec,
        "structure_type": "zeo"}


specs = [spec]
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

with open(os.path.join( 'aws.yaml')) as f:  
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)  

db_url = db_yaml['db']  
launchpad_path = os.path.join(os.getcwd(), 'my_launchpad.yaml')  

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




