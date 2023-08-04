import os
cnt = 0
result_path = './'
f_train = open(result_path + 'train.txt', 'w')
f_test = open(result_path + 'test.txt', 'w')
root_path = '/media/dgist/T7/DGIST_data_6'

for (path, dir, files) in os.walk(root_path):
    files.sort()
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        if ext == '.png':
            if cnt % 5 == 0:
                new_path = path.replace(root_path, '')
                print(new_path + '/' + filename)
                f_test.write(new_path + '/' + filename)
                f_test.write('\n')
                cnt = cnt + 1
            else:    
                #print(path - str('/media/dgist/T7/DGIST_data'))
                new_path = path.replace(root_path, '')
                print(new_path + '/' + filename)
                f_train.write(new_path + '/' + filename)
                #print("%s/%s" % (path, filename))
                f_train.write('\n')
                cnt = cnt + 1
f_train.close()
f_test.close()

