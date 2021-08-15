# VASP-FW 
### Bridging the gap between VASP and fireworks    
This package bridges fireworks and ASE/VASP/MAZE-sim so that jobs can easily be submitted.   

## Requirements 
This package only works with the Kulkarni group fork of fireworks found [here](https://github.com/kul-group/fireworks). Install this package before continuing. Python 3.7 and Python 3.8 work well with this package. Python 3.9 has some issues on the MacOS operating system. 

 ## Installation
1. Activate your fireworks conda environment ``source activate fw37``
2. Clone the repo, navigate into it, and install the package in developer/editible mode 
```bash
git clone https://github.com/kul-group/vasp-fw.git
cd vasp-fw
pip install -e . 
```

## Additional Guides 
1. [Fireworks Configuration](https://github.com/kul-group/vasp-fw/blob/main/fireworks_config.md)
2. [Running SLURM Jobs](https://github.com/kul-group/fireworks-guide/blob/main/running_slurm_jobs.md)
3. [VASP-FW Tutorial](https://github.com/kul-group/vasp-fw/blob/main/tutorial.md)
