#!/bin/bash
#SBATCH -p gpu_a100_8
#SBATCH -N 1
#SBATCH -n 2 
#SBATCH --mem 500GB
#SBATCH -t 12:00:00 
#SBATCH --job-name="proc"
#SBATCH --gres=gpu:1
#SBATCH --mail-user=sharanhpc@gmail.com
#SBATCH --mail-type=ALL

spack load anaconda3@2022
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home//psaxena/.conda/envs/Imageproc/lib/
source activate Imageproc

python3 -u main.py