sbatch --output=$2 --error=$3 gpu_$1.sh
squeue -u $USER