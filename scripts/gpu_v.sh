#!/bin/bash
#SBATCH -p gpu_v100_2
#SBATCH -N 1
#SBATCH -n 2 
#SBATCH --mem 250GB
#SBATCH -t 1-00:00:00 
#SBATCH --job-name="proc"
#SBATCH --gres=gpu:1
#SBATCH --mail-user=sharanhpc@gmail.com
#SBATCH --mail-type=ALL

source activate Imagegen

python3 main.py