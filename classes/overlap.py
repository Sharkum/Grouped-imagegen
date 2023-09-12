from .generate_data import imagegen
import numpy as np
class overlap_gen(imagegen):
    
    def __init__(self, img_dir, dataset, max_imgs, output_dim, background=None, output_dir=None):
        super().__init__(img_dir, dataset, max_imgs, output_dim, background, output_dir)
        self.overlap_perc = 0.1
        return
    
    def get_overlap_perc(self):
        self.overlap_perc = np.random.choice(np.arange(0.1,0.9,0.1),1)[0]
        pass
    
    def possible_pos_for_overlap_perc(self,position,img_size,img2_size,corner):
        
        overlapping_area = self.overlap_perc * img_size[0] * img_size[1]
        # a is the constant for the hyperbolic curve
        a = overlapping_area*(-1)**((corner+1)//2+1)
        x = np.array(range(1,img_size[0]))*(-1)**(corner%2)
        y = np.ceil(a/x)
        y[abs(y)>img_size[1]] = np.nan
        x = x[~np.isnan(y)]
        y = y[~np.isnan(y)]

        # translating the points to actual positions in the canvas with respect to the new image
        x = x + position[-2*(corner%2)] - img2_size[0]*((corner+1)%2)
        y = -y + position[(-1)**(corner//2)] + img2_size[1]*(corner//2-1)
        
        x= x.astype('int64')
        y= y.astype('int64')
        
        
        possible_pos = []
        for i in range(len(x)-1):
            if x[i] < 0  or y[i] < 0:
                continue
            curr,next = y[i], y[i+1]
            n_entries = abs(next - curr)
            ys = list(range(curr,next)) if curr < next else reversed(range(next,curr))
            entries = list(zip([x[i]]*n_entries,ys))
            possible_pos.extend(entries)
        if x[-1] > 0 and y[-1] >  0:
            possible_pos.append((x[-1],y[-1]))
        return possible_pos 
    
    def get_position(self, canvas_size, img_size, possible_positions, positions_excluded,output=None):
        if self.overlapped or positions_excluded == []:
            return super().get_position(canvas_size, img_size, possible_positions, positions_excluded,output=output)
        else:
            pos_bound = canvas_size[0] - img_size[0], \
                        canvas_size[1] - img_size[1] 
                    
            corners = list(range(4))
            self.get_overlap_perc()
            
            while True:
                corner = np.random.choice(corners,1)[0]
                
                img_pos = positions_excluded[0]
                img1_size = img_pos[2]-img_pos[0], img_pos[-1]-img_pos[1]
                curve_positions = self.possible_pos_for_overlap_perc(img_pos,img1_size,img_size,corner)
                
                possible_positions = []
                for pos in curve_positions:
                    if pos[0] > pos_bound[0] or pos[1] > pos_bound[1]:
                        continue
                    else:
                        possible_positions.append(pos)
                
                if possible_positions == []: 
                    corners.remove(corner)
                else: break
                if corners == []: break
            
            if possible_positions != []:
                position = possible_positions[np.random.choice(range(len(possible_positions)),1)[0]]
                self.overlapped=True
                return position
            return []
            

    def resize_position_imgs(self, imgs, canvas):
        self.overlapped = False
        
        return super().resize_position_imgs(imgs, canvas)