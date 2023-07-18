sbatch --output=$3 --error=$4 --export=batch_size=$2 gpu_$1.sh
squeue -u $USER