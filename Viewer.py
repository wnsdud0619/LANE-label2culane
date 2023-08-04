import multiprocessing
import threading
import os
import cv2
import math

def draw_image(pair_list, result_path):
    for pair in pair_list:
        img_file = pair[0]
        label_file = pair[1]
        img = cv2.imread(img_file)
        with open(label_file, 'r') as anno_file:
            # type truncated occluded alpha left top right bottom height width length x y z rotation_y score
            annotations = [line.strip().split(' ') for line in anno_file.readlines()]
            if not annotations:
                return

            for idx in range(len(annotations)):
                anno = annotations[idx]
                for jdx in range(int(len(anno)/2)):
                    img_x = float(anno[jdx*2])
                    img_y = float(anno[jdx*2+1])
                    cv2.circle(img, (int(img_x), int(img_y)), 10, (0, 0, 255), -1)

        save_file = os.path.join(result_path, os.path.basename(img_file))
        cv2.imwrite(save_file, img)
        print('%s is done' % save_file)

def loadFiles(_base_path, _valid_ext='png'):
    file_list = [loaded_file for loaded_file in os.listdir(_base_path) if loaded_file.endswith('.' + _valid_ext)]
    assert len(file_list) is not 0, 'No Files with \'.$s\' : %s' % (_valid_ext, _base_path)
    file_list.sort()
    print('%d loaded %s in : %s' % (len(file_list), _valid_ext, _base_path))
    return file_list

def main():
    root_path = '/home/dgist/labelme2culane'
    img_folder_path = os.path.join(root_path, 'png')
    txt_folder_path = os.path.join(root_path, 'txt')
    result_path = './display'
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    image_list = loadFiles(img_folder_path)

    paired_img_list = []
    paired_label_list = []
    for img_name in image_list:
        img_file = os.path.join(img_folder_path, img_name)
        label_file = os.path.join(txt_folder_path, os.path.basename(img_file).replace("png", "lines.txt"))
        assert os.path.isfile(label_file), 'No annotation file(%s)' % label_file
        paired_img_list.append(img_file)
        paired_label_list.append(label_file)

    pairs = list(zip(paired_img_list, paired_label_list))

    thread_count = multiprocessing.cpu_count()
    sliced_num = len(pairs) / thread_count

    threads = []
    for idx in range(thread_count):
        start = int(idx * sliced_num)
        end = int((idx + 1) * sliced_num if idx < range(thread_count)[-1] else len(pairs))
        thread = threading.Thread(target=draw_image, args=(pairs[start:end], result_path, ),)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('Done')

if __name__ == '__main__':
    main()

