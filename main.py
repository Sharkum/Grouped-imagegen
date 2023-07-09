import sys
from classes import *


if __name__ == '__main__':
    
    processor = image_proc('images','procc_images')
    processor.proc_save(remove_background=True,crop=True,save=True)
    
    # generator = imagegen('images',8,(1280,720),'backgournd.png','output_dir')