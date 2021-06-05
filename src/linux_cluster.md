# Accessing and using IDUN to do scientific compuations using Python

The Idun cluster is a high-performance computational resource provided by NTNU. Getting access to Idun means that you have access to a cluster of advanced computers which provide both storage and computational resources in the form of computer cores and GPUs. Each computer is known as a node, and each node has several cores. 

You can access Idun through Secure Shell (SSH) which provide a secure connection from your computer to the cluster. SSH must be installed on your computer and can then be accessed through your chosen command-line tool. To log in to Idun from your home computer, you must first log in to the NTNU network:

```
ssh -X -l username login.stud.ntnu.no
``` 
You may then log in to the cluster. There are 3 login nodes, login1, login2 and login3. Here is how to log in using login1:

```
ssh -X -l username  idun-login1.hpc.ntnu.no
```
This is a Linux cluster, so from now on you must type Unix commands. Navigate to your home directory. It is important to remember that data on the cluster is not backed up, so make sure to back up any important files using for instance a GitHub repository.

## Linux basics
```bash
cd cluster/work/username
``` 
To list the content of a folder you can type
```bash
ls -la
```
The -la tag shows the results as a list, not ignoring any files.
To quickly read a textfile you can use cat:
```bash
cat file/path.txt
```
This just shows the content of the file, but you can't edit it. To edit a file (this can also be a simple script file with another extension than .txt) you may use the simple command-line text editor nano:

```bash
nano file/path.txt
```
On the cluster you must load in the software you intend to use. These are contained in something called modules. There are many modules to choose from, but to work with Python programs you probably only need the Anaconda module. It is good practice to remove any previously loaded modules to make sure there is no conflict between software dependencies.

## Python
```bash
 module purge
 module load Anaconda3/2020.07
``` 

If this wont load, try to find the right installation version:

```bash
module spider Anaconda3
```

You can check the the installed Python packages, as well as installing new packages using pip
```bash
#shows installed packages and their version numbers
pip list

#install new package 
pip install package_name --user 

#install package with specific version number X.X
pip install package_name==X.X --user 
```

To start a python script, simply use the `python` command.

```bash
python /path/to/file.py
```
However, you should not start large processes like this. They should be submitted through the SLURM Workload Manager (SLURM).

---
**NOTE**

If you are working from home and only occasionaly running your scripts on Idun, it would be a pain to do all the programming using the command-line. File sharing between your home computer and the NTNU cluster is not necessarily straightforward, but one simple way to do this while also providing backup and version control to your project is to initialise it as a [github](github.com) repository. Just remember to add a `.gitignore` file to your project and add the folders/filetypes you don't want to share. This would include any very large files or unimportant files. GitHub has a limit on file size as well as a limit on the number of files in a repository, so just make sure to take that into account. [Here](http://www.deanbodenham.com/learn/using-git-to-sync-different-computers.html) is a great guide to get you started.

---

## Running jobs

When you want to run your large project on the cluster you must submit it to SLURM as a job. It is then queued along with other sumbitted jobs, and will be run when the computer resources are available. You can get e-mail notifications for when the job is started, when it is completed or if it fails. More in depth documentation can be found at the [Sigma2](https://documentation.sigma2.no/jobs/job_scripts/array_jobs.html) webpage.


The first step is to create a SLURM job script. It is essentially a bash script with some extra information for SLURM. The script may have any name, but let's use the filename `job.slurm` for this example script.

```bash
#!/bin/sh
#SBATCH --partition=CPUQ
#SBATCH --account=<account>
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12000
#SBATCH --job-name="hello_test"
#SBATCH --output=test-srun.out
#SBATCH --mail-user=<email>
#SBATCH --mail-type=ALL
 
WORKDIR=${SLURM_SUBMIT_DIR}
cd ${WORKDIR}
echo "we are running from this directory: $SLURM_SUBMIT_DIR"
echo " the name of the job is: $SLURM_JOB_NAME"
echo "Th job ID is $SLURM_JOB_ID"
echo "The job was run on these nodes: $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "We are using $SLURM_CPUS_ON_NODE cores"
echo "We are using $SLURM_CPUS_ON_NODE cores per node"
echo "Total of $SLURM_NTASKS cores"

module purge
module load Anaconda/2020.07
python /path/to/file.py

uname -a

```

Let's break down this example. The first line, `#!/bin/sh` tells the computer that this is a bash script. The next lines are all commented out, but they are still read by SLURM and change the environment variables.

| Item      | Environment variable | Description |
| ----------- | ----------- |----------- |
| partition |-|-|
| account|-|The account to bill for the memory usage.|
| time| Text |The amount of time allocated for your job. The task fails if your program runs for longer than this time limit. |
| nodes| $SLURM_JOB_NUM_NODES  |The number of nodes.|
| ntasks-per-node| | The number of tasks per node. |
| mem| |The amount of memory allocated for your job. The task fails if your program exceeds this limit.|
| job-name| $SLURM_JOB_NAME| The name of the job.|
| output   |-|The file in which to save all printed outputs.|
| mail-user|-|The email to send notifications to.|
| mail-type|-|Which emails to send. |
|  |  | |

chmod u+x filename

Run it:
sbatch filename

## Jupyter Notebook 

It is possible to run an interactive Jupyter Notebook session hosted on the Idun servers on your home computer. This is done through SSH tunneling.
Start a jupyter notebook session from the folder you want to work with while logged in to Idun:

```
cd /lustre1/work/username/foldername
module load Anaconda3/2020.07
jupyter notebook --no-browser
```
You will get a message like this:
```
 To access the notebook, open this file in a browser:
        file:///run/user/1227530/jupyter/nbserver-159660-open.html
    Or copy and paste one of these URLs:
        http://localhost:8890/?token=ff0495955e8663c1f31c2f6bae32da7197127e081142e590
```
Jupyter Notebook is then hosted on localhost:8890. Note that you might get another port. We want to access this from our own localhost:XXXX to open it in our local browser.
Open a new command line window and log in to the NTNU servers:
```
ssh -X login.stud.ntnu.no -l username
``` 
Now open an SSH-tunnel from the NTNU login to the Idun login. Remember that you may use another login than login1:
 ```
ssh -L YYYY:localhost:8890 username@idun-login1.hpc.ntnu.no
``` 
YYYY can be any available port. Try 8888 for instance, or 1234.
However, we can still not access Jupyter Notebook from our browser, so we must make another tunnel from the NTNU login to our computer. Open a third command line window:
```
ssh -L XXXX:localhost:YYYY username@login.stud.ntnu.no
```
Now you can copy the link from earlier, and change the port to your chosen port XXXX. Paste that into your browser:
http://localhost:XXXX/?token=ff0495955e8663c1f31c2f6bae32da7197127e081142e590

You should be able to access your files from the Idun folder you started jupyter notebook from.
