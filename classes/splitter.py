import os,shutil
import numpy as np

class train_val_splitter:
    ''' This class is used to split a folder images into train,val,test splits
    '''
    def __init__(self, images,labels, output_dir):
        self.images = images
        self.labels = labels
        self.output_dir = output_dir
        pass
    
    def mv_files(self,input_dir,files,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for file in files:
            shutil.move(os.path.join(input_dir,file),output_dir)
        pass
    
    def split(self,seed = 0,train=0.6,val=0.2):
        np.random.seed(seed)
        images = np.array(sorted(os.listdir(self.images)))
        labels = np.array(sorted(os.listdir(self.labels)))
        n = len(images)
        
        shuffled_order = list(range(n))
        np.random.shuffle(shuffled_order)
        
        train_len,val_len = int(train*n),int(val*n)
        train_ind = shuffled_order[:train_len]
        val_ind = shuffled_order[train_len:train_len+val_len]
        test_ind = shuffled_order[train_len+val_len:]
        
        split_names = {'images':{},'labels':{}}
        
        split_names['images']['train'], split_names['labels']['train'] = images[train_ind], labels[train_ind]
        split_names['images']['val'], split_names['labels']['val'] = images[val_ind], labels[val_ind]
        split_names['images']['test'], split_names['labels']['test'] = images[test_ind], labels[test_ind] 
        
        for i in split_names.keys():
            output_dir = os.path.join(self.output_dir,i)
            for split in split_names[i].keys():
                input_dir = self.images if i == 'images' else self.labels
                self.mv_files(input_dir, split_names[i][split],os.path.join(output_dir,split))
        
        pass