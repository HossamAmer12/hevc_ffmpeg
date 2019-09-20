# ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 504x336  -i /media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/pics/1/ILSVRC2012_val_00001000_504_336_RGB.yuv -c:v libx265 -crf 0 -preset ultrafast bla.265
# ffmpeg -f rawvideo -pix_fmt yuv420p -s:v 504x336  -i /media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/pics/1/ILSVRC2012_val_00001000_504_336_RGB.yuv -c:v hevc -f hevc bla.265


import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import cv2
import time

# Excel sheet stuff:
import xlrd
from xlwt import *
from xlutils.copy import copy

import subprocess as sp # for sh files

import glob
# import tensorflow as tf


PATH_TO_EXCEL = os.path.join( os.getcwd() , 'Alexnet50K-HEVC.xls') 

# START = 1
# END = 2

# For initial debugging:
# START = 1000
# Y only testing ILSVRC2012_val_00000126_504_376_Y.yuv
# START = 34
# END = START + 1 

START = 1
END   = 1 + 50000  



# Create bpp ORG, SSIM Org, PSNR ORG lists.
shard_num = 0

MAIN_PATH    = '/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/'
image_dir    = os.path.join(MAIN_PATH, 'pics')
output_path  = os.path.join(MAIN_PATH, 'Seq-RECONS-ffmpeg')
output_path_265  = os.path.join(MAIN_PATH, 'Seq-265-ffmpeg')
output_path_stats = os.path.join(MAIN_PATH, 'Gen/Seq-Stats') 
output_path_stats_unified = os.path.join(MAIN_PATH, 'Gen/Seq-Stats-Unified') 

def readFileContents(image):
    f = open(image, "r")    
    lines = f.readlines()
    f.close()
    return lines

def writeFileContents(image, lines):
    f = open(image, "a")
    f.write(''.join(lines))
    f.close()


QP = []
# QP.append(51)
# for i in range(50, 0, -2):
#     QP.append(i)
QP.append(51)
print(QP)

# for time
t = [0.0, 0.0, 0.0, 0.0]

for imgID in range(START, END):

    original_img_ID = imgID
    imgID = str(imgID).zfill(8)
    prev_shard = shard_num
    shard_num  = original_img_ID//10001
    

    check_shard = (original_img_ID-1)/10000
    if not check_shard % 1 and original_img_ID != 10001 or prev_shard > shard_num and prev_shard != 0: # check if a number is integer
        shard_num = shard_num + 1
    
    folder_num = math.ceil(original_img_ID/1000)

    glob_path = image_dir + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '*.yuv'
    filesList = glob.glob(glob_path)
    name = filesList[0].split('/')[-1].split('.')[0]
    rgbStr = name.split('_')[-1]
    height = int(name.split('_')[-2])
    width = int(name.split('_')[-3])

     # Construct current image
    current_image = image_dir + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '.yuv'

    if rgbStr.__contains__('Y'):
        input_format = 'gray'

    else:
        input_format = 'yuv420p'

    # Calculate SSIM, PSNR, bpp
    tStart = time.time()
    qp = QP[0]
    output_265 = output_path_265 + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.265'
    recons_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.yuv'
    output_stats = output_path_stats + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.txt'
    cmd = './calc_quality ' + current_image + " " + recons_image + " " + output_265 +  " " + output_stats
    p = os.popen(cmd).read()
    print(imgID, p)
    t[0] += time.time() - tStart

    if not original_img_ID % 50:
        print('Image ID %s is done in %f seconds' % (imgID, (sum(t))) )
        t = [0.0, 0.0, 0.0, 0.0]


   