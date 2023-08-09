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

# ../.environment/bin/python3 train.py --cfg yolov5s.yaml --batch $batches --epochs $epochs --data data_random_overlap.yaml --img 1280 --name random_overlap_train
../.environment/bin/python3 val.py --weights ./runs/train/random_overlap_train/weights/best.pt --img 1280 --data data_random_overlap.yaml --task test --name random_overlap_test