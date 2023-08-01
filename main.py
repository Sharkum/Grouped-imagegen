import sys
import datetime
from classes.generate_data import image_proc,imagegen
from classes.overlap import overlap_gen
from classes.splitter import train_val_splitter
import torch 
import onnxruntime as ort

def generate_images(input_dir,set,background,output_dir,size=15000):
    generator = imagegen(f'{input_dir}/{set}',8,(1280,720),background,f'{output_dir}/{set}')
    with open('seed','r+') as f:
        seed = int(f.readline())
        f.seek(0)
        f.write(str(seed+1))
        f.truncate()
        generator.generate_batch(seed=seed,batch_size=size,verbose=True)
        
def generate_overlapping_images(input_dir,set,background,output_dir,size=15000,seeding=True):
    generator = overlap_gen(f'{input_dir}/{set}',set,8,(1280,720),background,f'{output_dir}')
    if seeding:
        with open('seed','r+') as f:
            seed = int(f.readline())
            f.seek(0)
            f.write(str(seed+1))
            f.truncate()
            generator.generate_batch(seed=seed,batch_size=size,verbose=True)
    else: generator.generate_batch(seed=0,batch_size=size,verbose=True)
        
def split_input_images(images,labels,output_dir):
    splitter = train_val_splitter(images,labels,output_dir)
    splitter.proc_split()
    return

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    
    # split_input_images('procc_images','labels','procc_images')
    generate_overlapping_images('procc_images','train','background.png','random_overlapping_images')
    
    endtime = datetime.datetime.now()
    print(f'{(endtime-starttime).seconds/3600} hours')
    