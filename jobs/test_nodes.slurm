#!/bin/sh
#SBATCH --partition=CPUQ
#SBATCH --account=share-nv-fys
#SBATCH --time=00:05:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --mem=1000
#SBATCH --job-name="basic_properties"
#SBATCH --output=test-nodes-srun.out
#SBATCH --mail-user=aurorasg@stud.ntnu.no
#SBATCH --mail-type=ALL
#SBATCH --wait-all-nodes=1
 
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

#launched on Node 1
srun --nodes=1 echo 'hello from node 1' >> test.txt &

#Launched on Node2
srun --nodes=1 echo 'hello from node 2' >> test.txt &