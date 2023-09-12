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

# ../.environment/bin/python3 tools/train.py --batch $batches --conf configs/yolov6l6.py --epochs $epochs --height 720 --width 1280 --data ./data_random_overlap.yaml --device 0 --name l6_model
../.environment/bin/python3 tools/eval.py --data ./data_random_overlap.yaml --verbose --do_pr_metric True --batch $batches --height 720 --width 1280 --task test --weights runs/train/new_labels4/weights/best_ckpt.pt --device 0 --name new_labels_test
# ../.environment/bin/python3 tools/infer.py --yaml ./data_random_overlap.yaml --weights runs/train/new_labels3/weights/best_ckpt.pt --source ../random_overlapping_images/images/test/ --device 0