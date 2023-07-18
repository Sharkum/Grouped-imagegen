import sys
import datetime
from classes.generate_data import image_proc,imagegen
from classes.splitter import train_val_splitter
import torch 
import onnxruntime as ort


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    
    splitter = train_val_splitter('output_dir/images','output_dir/labels',output_dir='output_dir')
    splitter.split()
    
    endtime = datetime.datetime.now()
    print(f'{(endtime-starttime).seconds/3600} hours')
    