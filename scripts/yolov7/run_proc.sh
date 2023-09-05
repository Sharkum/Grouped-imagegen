sbatch --output=$4 --error=$5 --export=batches=$2,epochs=$3 gpu_$1.sh
squeue -u $USER