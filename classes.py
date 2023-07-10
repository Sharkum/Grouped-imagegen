import os
import numpy as np
import pandas as pd
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
    
    def load_imgs(self,limit=None):
        if self.imgs: return
        imgs = os.listdir(self.img_dir)
        if not limit: 
            samples=len(imgs)
        else:
            samples = min(limit,len(imgs))
        for i in range(samples):
            tmp = Image.open(os.path.join(self.img_dir,imgs[i]))
            tmp.load()
            self.imgs.append(tmp)
        return 
    
    def remove_background(self,limit=None):
        print('removing background')
        self.load_imgs(limit=limit)
        for i in range(len(self.imgs)):
            if not limit and i%(len(self.imgs)//100) == 0:
                print(i)
            tmp = self.imgs[i]
            print(i)
            self.imgs[i] = remove(tmp)
            print(i)
            self.imgs[i].filename = tmp.filename
        return
    
    def crop_invis(self,limit=None):
        print('removing invis')
        self.load_imgs(limit=limit)
        for i in range(len(self.imgs)):
            if not limit and i%(len(self.imgs)//100) == 0:
                print(i)
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
    
    def proc_save(self,remove_background=False,crop=False,save=True,limit=None):
        #preprocessors-
        if remove_background:
            self.remove_background(limit=limit)
        if crop:
            self.crop_invis(limit=limit)
        
        #saving files
        if save:
            self.save()
        return
    

class imagegen:
    '''
    This image generator will generate images based on random selection of images
    '''

    def __init__(self,img_dir,max_imgs,output_dim, background=None,output_dir=None):
        self.n_imgs = 0
        self.imgs_selected = []
        self.imgs = []
        
        self.max_imgs = max_imgs
        self.img_dir = img_dir
        self.output_dim = output_dim
        self.background = background
        self.output_dir = output_dir
        if self.background:
            self.canvas = Image.open(self.background).resize(self.output_dim)
        else:
            self.canvas = Image.new('RGB',self.output_dim,0)

        return
    
    def select_images(self,verbose=False):
        self.n_imgs = np.random.choice(range(2,self.max_imgs), 1)
        if verbose:
            print(f'{self.n_imgs} images were selected')
        
        self.imgs = np.array(os.listdir(self.img_dir))
        selected_ind = np.random.choice(len(self.imgs),size=self.n_imgs,replace=False)
        if verbose:
            print(f'{selected_ind} were the indices that were selected')
        self.imgs_selected = []
        for ind in selected_ind:
            path = os.path.join(self.img_dir,self.imgs[ind])
            tmp = Image.open(path)
            tmp.label = int(path.split('/')[-1][7])
            self.imgs_selected.append(tmp)
        return
    
    def get_newsize(self,img,canvas,size_perc):
        ratio_img = img.size[0]/img.size[1]
        ratio_canvas = canvas.size[0]/canvas.size[1]
        
        if ratio_img > ratio_canvas:
            canvasfit = (canvas.size[0],int(canvas.size[0]/ratio_img))
        else:
            canvasfit = (int(canvas.size[1]*ratio_img),canvas.size[1])
            
        new_size = int(canvasfit[0]*size_perc), int(canvasfit[1]*size_perc)
        
        return new_size
    
    def position_possible(self,position,positions_excluded):
        
        for pos in positions_excluded:
            if not(position[0] > pos[2] or pos[0] > position[2]):
                return False
            
            if not(position[3] > pos[1] or pos[3] > position[1]):
                return False

        return True
        
    def get_position(self, canvas_size,img_size, possible_positions,positions_excluded):
        
        pos_bound = canvas_size[0] - img_size[0], \
                    canvas_size[1] - img_size[1]        
        
        ind_pos = []
        for i in range(pos_bound[0]*pos_bound[1]):
            pos = possible_positions[i]
            pos = [pos[0],pos[1],pos[0]+img_size[0],pos[1]+img_size[1]]

            if self.position_possible(pos,positions_excluded):
                ind_pos.append(pos)
        
        if len(ind_pos) == 0:
            return False
        
        possible_positions = ind_pos
        
        position = possible_positions[np.random.choice(range(len(possible_positions)),1)[0]]
        
        return position
    
    def pascal_to_yolo_bbox(self,boxes, w, h):
        res = []
        for bbox in boxes:
            x_center = ((bbox[2] + bbox[0]) / 2) / w
            y_center = ((bbox[3] + bbox[1]) / 2) / h
            width = (bbox[2] - bbox[0]) / w
            height = (bbox[3] - bbox[1]) / h
            res.append([x_center, y_center, width, height])
        return res
    
    def resize_position_imgs(self,imgs,canvas):
        
        max_size = 1/self.n_imgs
        min_size = max_size*3/4
        output = canvas.copy()
        
        positions_excluded = []
        labels = []
        
        for img in imgs:
            
            size_perc = np.random.choice(np.arange(min_size,max_size,0.01),1)

            new_size = self.get_newsize(img,canvas,size_perc)
            
            img_resized = img.resize(new_size)
            
            pos_bound = canvas.size[0] - new_size[0], \
                        canvas.size[1] - new_size[1]
            
            possible_positions = np.dstack(np.meshgrid(range(pos_bound[0]),range(pos_bound[1]))).reshape(-1,2).tolist()
            
            position = self.get_position(canvas.size,new_size, possible_positions, positions_excluded)
            
            if not position:
                continue
                
            positions_excluded.append([position[0], position[1], position[0]+new_size[0], position[1]+new_size[1]])
            labels.append(img.label)
            
            mask = img_resized.split()[-1]
            
            output.paste(img_resized,position,mask=mask)
        
        return output, np.array(self.pascal_to_yolo_bbox(positions_excluded,self.output_dim[0],self.output_dim[1])), np.array(labels)
    
    def generate_batch(self,seed,batch_size,verbose=False):
        
        np.random.seed(seed)
        
        for i in range(batch_size):
            self.select_images(verbose=verbose)
        
            new_img, bounds, labels = self.resize_position_imgs(self.imgs_selected,self.canvas)
            
            annots = np.hstack((labels.reshape(-1,1),bounds))
            
            if not self.output_dir:
                raise ValueError(self.output_dir)
            
            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)
            
            images_path = self.output_dir + '/images'
            labels_path = self.output_dir + '/labels'
            
            if not os.path.exists(images_path):
                os.mkdir(images_path)
            if not os.path.exists(labels_path):
                os.mkdir(labels_path)
            
            new_img.save(f'{images_path}/{seed}_{i}.jpg')
            np.savetxt(f'{labels_path}/{seed}_{i}.txt',annots,fmt='%1.16f')
            
        return

    def test_resize(self,verbose=False):
        self.generate_batch(1,3)

        return 