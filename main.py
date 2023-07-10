import sys
import datetime
from classes import *
import torch 


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print(f"Using device: {device}")
        
    processor = image_proc('images','procc_images')
    processor.proc_save(remove_background=True,crop=True,save=True,limit=10)
    
    # generator = imagegen('images',8,(1280,720),'backgournd.png','output_dir')
    
    endtime = datetime.datetime.now()
    print(f'{(endtime-starttime).seconds/3600} hours')
    