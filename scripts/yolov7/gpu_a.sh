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

# ../.environment/bin/python3 train.py --workers 8 --device 0 --batch-size $batches --epochs $epochs --data ./data_random_overlap.yaml --img 1280 1280 --cfg cfg/training/yolov7.yaml --weights '' --name yolov7 --hyp data/hyp.scratch.p5.yaml
../.environment/bin/python3 test.py --device 0 --batch-size $batches --verbose --data ./data_random_overlap.yaml --img 1280 --weights 'runs/train/yolov72/weights/best.pt' --name yolov7 --task test