
# Fireworks Configuration

Fireworks is a workflow management tool designed for materials science simulations. The full documentation can be found here: https://materialsproject.github.io/fireworks/ . This installation guide is for Linux and macOS for the Kulkarni group at UC Davis. 

## Prerequisites 
1. This tutorial assumes that you have conda installed and configured.
2. This tutorial also assumes that you are working on MacOS or Linux machine. If you are using windows then I recommend using windows bash with Ubuntu to go through this tutorial. 


## Installing Fireworks 
1. Create a new conda environment for fireworks, with the python version set to 3.7. 
``conda create -n fw37 python=3.7 anaconda``. Major changes to the python multiprocessing library for `macos` took place in the transition from `3.7` to `3.8`, thus `3.7` is what was used for this tutorial (specifically `3.7.9`). 
2. Pick a location to store the cloned fireworks repo. The location does not matter, but it is important to keep it in its place after cloning it. 
3. Clone the kul-group fork of the fireworks repo https://github.com/kul-group/fireworks by typing 
``git clone https://github.com/kul-group/fireworks.git``. The kul-group fireworks repo is a fork of the materials project fireworks repo and includes additional Fireworks for custom optimization tasks. 
4.  After cloning the repo navigate into the repo 
``cd fireworks``
5. Activate your conda environment by typing `conda activate fw37` (replace `fw37` with the name of your conda env if you chose a different name). 
6. Install the package using pip with the -e flag to ensure that the package is editable 
``pip install -e .`` 
7. At different points you might need to install additional packages. The full list of installed packages in the conda env used when creating this tutorial can be found here. It is recommended to install the latest version of the packages as needed (i.e. when you get an error) rather than trying to install them before preceding. Use `conda` to install packages whenever possible and only use `pip` as a last result or to install packages in the dev/editable mode. The conda command for installing a certain package can be found by googling `conda install package-name`. 

## MongoDB Database Introduction  

Fireworks requires a MongoDB database to store fireworks. You can use either a local or remote MongoDB database. MongoDB used to be an open source database platform, but it switched to a  [Server Side Public License](https://www.mongodb.com/licensing/server-side-public-license).  Amazon has its own MongoDB ripoff that might or might-not work with fireworks. MongoDB is a NoSQL or document database, which is basically a standard relational database with the capacity to store JSON data in some fields. As you work with fireworks, you will notice the heavy use of JSON data. 

## Creating a Local MongoDB Database on MacOS 

1. Install [homebrew](https://brew.sh/)
2. Follow the official guide for installing MongoDB with [homebrew](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
3. Launch a local MongoDB instance with the following command `mongod --config /usr/local/etc/mongod.conf --fork`

## Setting up a Remote MongoDB Database 
MongoDB makes money by selling access to remote MongoDB database clusters through a software as a service business model. To attract customers they offer a free-tier MongoDB database option. This free-tier works great for fireworks since the total amount of data generated by fireworks is small. It can also be accessed from anywhere removing the headache of configuring port forwarding. To setup a free-tier remote MongoDB database follow these instructions. 
1. Create a MongoDB account by logging in with a google account 
2. Select create an organization and select the MongoDB Atlas option
3. Select create a new project and name it whatever you want 
4. Select build a cluster
5. Select the free `Shared Cluster` Option 
6. Select your choice of cloud provider (I chose AWS)
7. Select the region closest to you 
8. Choose a cluster name 
9. Press the `Create Cluster` button 
10. Wait for the cluster to spin up  
11. Press the connect button 
12. Select `allow access from anywhere` followed by `Add IP Address` 
13. Create a database username and note the password. This password might be exposed so don't pick the same one you use for anything else. Also be sure to write it down since it cannot be recovered. 
14. Click `Connect with your application` and note the command and host url. You will need it for the next steps. 

## Getting Fireworks to Talk with your Remote MongoDB Database 

 The next steps are getting fireworks to communicate with a the remote, MongoDB cluster. These instructions are taken from the post on the materials project [forum](https://matsci.org/t/heres-how-to-connect-to-atlas-mongodb/4816) and revised slightly for clarity. Also PulseSecure interferes with connecting to remote databases so be sure to turn that off before continuing. 
 
1. Activate your conda environment that has fireworks installed `source activate fw37`
2. install dnspython`conda install -c anaconda dnspython`
3. Remember the username and password you created in step 13 above. Your password will be called `DB USER PASSWORD` in the next step 
4.  Compute the URL-quoted DB user???s password:  
``python -c "import urllib.parse; print(urllib.parse.quote('DB USER PASSWORD'))"``
5. Note the returned `URL_QUOTED_DB_USER_PASSWORD` password, which can be different than your original password
6. Create a connection URL based off of the URL you found on the MongoDB website in step 14 and this template `mongodb+srv://DBUSERNAME:URL_QUOTED_DB_USER_PASSWORD@cluster1.6wxyz.azure.mongodb.net/fireworks ` 
7. Create `my_launchpad.yaml` by typing the following commands and replacing the host parameter with the one you assembled in step 6. 
``lpad init -u``
``Enter host parameter: mongodb+srv://DBUSERNAME:URL_QUOTED_DB_USER_PASSWORD@cluster1.6wxyz.azure.mongodb.net/fireworks  
Enter ssl_ca_file parameter:  
Enter authsource parameter: admin``
8. reset the launch pad with 
``lpad reset`` to confirm that the program works. 


## Creating a AWS PostgreSQL database for Storing Atoms Objects 
### Setting up AWS PostgreSQL Database  
1. Create an AWS account 
2. Go to the RDS amazon service 
3. Click on create database 
4. Click on standard create 
5. Select PostgreSQL 
6. select the `free tier` template 
7. Select the most recent version
8. Name the db instance something description like `db-instance` 
9. Set the master username to an easy to remember name 
10. Set a master password and write it down 
11. Click standard classes
12. In the connectivity settings select the default VPC (you will alter them later) 
13. Select yes for `Public Access` 
14. For VPC security group select `Choose Existing` 
15. For database authentication press Password authentication 
16. Click the additional configuration tap and enter an `initial database name` 
17. Press Create Database 
18. Change the network configurations to allow outside connections (see this [video](https://www.youtube.com/watch?v=XGt0vEUZXYw))
### Testing your Configuration
1. activate your fireworks environment and install the postgressql python package 
	```
	source activate fw37
	conda install -c anaconda psycopg2
2. Try to connect to the database with ASE by creating a connection string ([see ASE tutorial](https://wiki.fysik.dtu.dk/ase/ase/db/db.html#server)) that looks like this ``postgresql://user:pw@host:port/dbname`` 
3. Then try to add an Atom object to the database by running the following script
	```
	from ase.build import molecule 
	from ase.db import connect
	from ase.visualize import view
	water = molecule('H2O') 
	db = connect("postgresql://user:pw@host:port/dbname")
	index = db.write(water)
	water2 = db.get_atoms(index)
	view(water2)
5. Confirm that you see a water molecule 

