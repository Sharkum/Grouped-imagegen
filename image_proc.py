import os
import numpy as np
from PIL import Image
from rembg import remove


class image_proc:
    '''
    This class can be used to preprocess images.
    '''
    
    
    def __init__(self,img_dir,output_dir):
        self.img_dir = img_dir
        self.output_dir = output_dir
        self.imgs = []
        return
    
    def load_imgs(self):
        if self.imgs: return
        for i in os.listdir(self.img_dir):
            tmp = Image.open(os.path.join(self.img_dir,i))
            self.imgs.append(tmp)
        return 
    
    def remove_background(self):
        self.load_imgs()
        for i in range(len(self.imgs)):
            tmp = self.imgs[i]
            self.imgs[i] = remove(tmp)
            self.imgs[i].filename = tmp.filename
        return
    
    def crop_invis(self):
        self.load_imgs()
        for i in range(len(self.imgs)):
            tmp = self.imgs[i]
            mask = np.array(tmp.split()[-1])>0
            length = np.where(np.any(mask,axis=0))[0]
            height = np.where(np.any(mask,axis=1))[0]
            box = length[0], height[0], length[-1], height[-1]
            self.imgs[i] = tmp.crop(box)
            self.imgs[i].filename = tmp.filename
        return
    
    def save(self):
        for i in self.imgs:
            name = i.filename.split('/')[-1].split('.')[0] + '.png'
            i.save(os.path.join(self.output_dir,name))
        return
    
    def proc_save(self,remove_background=False,crop=False,save=True):
        #preprocessors-
        if remove_background:
            self.remove_background()
        if crop:
            self.crop_invis()
        
        #saving files
        if save:
            self.save()
        return