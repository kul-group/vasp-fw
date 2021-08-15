# Running a Fireworks Job with SLURM 

## Requirements
1. Access to a remote server with jobs managed by SLURM
2. Have installed minconda installed on that remote cluster 
3. Completion of the database setup steps in the previous fireworks configuration tutorial 

## Setup
1. Pick a directory to run the fireworks jobs 
2. Skim, but do not follow the materials project tutorial on [queues](https://materialsproject.github.io/fireworks/queue_tutorial.html)
3. Create a custom `quadapter_slurm.yaml` script for slurm modeled off of mine below and place it in your chosen directory
	```
	_fw_name: CommonAdapter
	_fw_q_type: SLURM
	ntasks: 1
	rocket_launch: rlaunch -w /home/dda/fw_things/fun/q2/my_fworker.yaml -l /home/dda/fw_things/fun/q2/my_launchpad.yaml singleshot
	cpus_per_task: 1
	ntasks_per_node: 1
	walltime: '01:00:00'
	queue: null
	account: null
	job_name: null
	logdir: /home/dda/fw_things/fun/q2/logging
	pre_rocket: source activate fw37
	post_rocket: null
	```
4. Add a custom my_launchpad.yaml and my_worker.yaml file to that folder as well. These should be based off of the instructions in the previous tutorials 
5. Follow the materials project tutorial on [queues](https://materialsproject.github.io/fireworks/queue_tutorial.html) but explicitly specify the location of the quadapter_slurm script with the -q flag for example `qlaunch -q qadapter_slurm.yaml singleshot`


