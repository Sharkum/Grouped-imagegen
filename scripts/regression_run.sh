#!/bin/bash
#SBATCH -p gpu_a100_8
#SBATCH -N 1
#SBATCH -n 2 
#SBATCH --mem 500GB
#SBATCH -t 12:00:00 
#SBATCH --job-name="cnn"
#SBATCH --gres=gpu:1
#SBATCH --mail-user=sharanhpc@gmail.com
#SBATCH --mail-type=ALL

spack load anaconda3@2022
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home//mohansc/.conda/envs/gpu_tf3/lib/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home//mohansc/.conda/envs/gpu_tf3/lib/python3.8/site-packages/tensorrt/
source activate gpu_tf3 

echo 'iter='$iter
echo 'iters='$iterations
python3 cnn_model.py $iter $iterations
