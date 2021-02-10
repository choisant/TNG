#!/bin/sh
#SBATCH --partition=CPUQ
#SBATCH --account=share-nv-fys
#SBATCH --time=10:00:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --mem=24000
#SBATCH --job-name="cluster_run"
#SBATCH --output=tng-cluster-srun.out
#SBATCH --mail-user=aurorasg@stud.ntnu.no
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
module load Anaconda3/2018.12

uname -a

srun ./src/cluster_run.sh [-t "tng-100-1"] [-i $SLURM_JOB_ID] [-n "idun"] [-g 1]
srun ./src/cluster_run.sh -t "tng-100-1" -i $SLURM_JOB_ID -n "idun" -g 2
srun ./src/cluster_run.sh [-t "tng-100-1" -i $SLURM_JOB_ID -n "idun" -g 3]
srun ./src/cluster_run.sh [-t "tng-100-1" -i $SLURM_JOB_ID -n "idun" -g 4]




