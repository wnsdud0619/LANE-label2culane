import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob
import os

class Convert():
    def __init__(self):
        self.root_path = '/home/dgist/labelme2culane'
        self.json_folder_path = os.path.join(self.root_path, 'json')
        self.result_path = './txt/'        
        self.cut_img = 500
        self.img_h = 1200
        self.img_w = 1920
        self.points_num = 18
        self.step = 20
        self.cnt = 1
        self.run()

    def loadFiles(self, _base_path, _valid_ext='json'):
        file_list = [loaded_file for loaded_file in os.listdir(_base_path) if loaded_file.endswith('.' + _valid_ext)]
        assert len(file_list) is not 0, 'No Files with \'.$s\' : %s' % (_valid_ext, _base_path)
        file_list.sort()
        print('%d loaded %s in : %s' % (len(file_list), _valid_ext, _base_path))
        return file_list

    def run(self):   
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        json_list = self.loadFiles(self.json_folder_path)
        json_list.sort()
       
        print(json_list)

        for json_name in json_list:
            json_path = os.path.join(self.root_path + '/json', os.path.basename(json_name))
 
            with open(json_path, 'r') as file:
                data = json.load(file)
            print(json_name[:-5])    
            f_txt = open(self.result_path + json_name[:-5] + '.lines.txt', 'w')

            lanes = data['shapes']
            lanes_xys = []
            for lane in lanes:
                null_image = np.full((self.img_h, self.img_w, 3), (0,0,0), dtype=np.uint8)
                #cv2.namedWindow(winname='imshow', flags=cv2.WINDOW_NORMAL)
                #cv2.resizeWindow(winname='imshow', width=960, height=600)
                points = lane['points']

                xys = []
                for x, y in points:
                    if x <= 0 or y <= 0:
                        continue
                    x, y = int(x), int(y)
                    xys.append((x, y))
                    xys.sort(key=lambda x: (x[1], x[0]), reverse=True)

                #lanes_xys.append(xys)
                #lanes_xys.sort(key=lambda xys : xys[0][0])
                for i in range(1, len(xys)):
                    cv2.line(null_image, xys[i - 1], xys[i], (255,0,0), thickness=1)

                for h in range(40):
                    for w in range(self.img_w):
                        if null_image[(self.img_h-1) - self.step*h][w-1][0] == 255:
                            #print(w, self.img_h -self.step*h)
                            f_txt.write(str(w)+' ')
                            f_txt.write(str(self.img_h -self.step*h)+' ')   
                
                # cv2.imshow('imshow',null_image)
                # if cv2.waitKey(0) == 27:
                #     continue
                # cv2.destroyAllWindows()
                f_txt.write('\n')
                
            #self.cnt = self.cnt +1
            f_txt.close()  

if __name__ == '__main__':
    convert = Convert()









