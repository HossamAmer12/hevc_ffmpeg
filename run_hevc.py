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

START = 1
END = 2

# Create bpp ORG, SSIM Org, PSNR ORG lists.
shard_num = 0

MAIN_PATH    = '/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/'
image_dir    = os.path.join(MAIN_PATH, 'pics')
output_path  = os.path.join(MAIN_PATH, 'Seq-RECONS-ffmpeg')
output_stats = os.path.join(MAIN_PATH, 'Seq-Stats-ffmpeg') 


QP = []
QP.append(51)
for i in range(50, 0, -2):
    QP.append(i)
QP.append(0)

for imgID in range(START, END):

    original_img_ID = imgID
    imgID = str(imgID).zfill(8)
    prev_shard = shard_num
    shard_num  = original_img_ID//10001
    

    check_shard = (original_img_ID-1)/10000
    if not check_shard % 1 and original_img_ID != 10001 or prev_shard > shard_num: # check if a number is integer
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

    # Encode via FFMPEG x265 to a different YUV file
    for qp in QP[0:1]:
        output_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.yuv'
        cmd = 'ffmpeg -f rawvideo -vcodec rawvideo -s ' + str(width) + 'x' + str(height) +  ' -pix_fmt yuv420p -i ' \
        + current_image + ' -c:v libx265 -crf ' + str(qp) + ' -preset ultrafast ' + output_image
        
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out, err = p.communicate()

        # print(current_image)
        # print(output_image)
        # if(err):
        #     print('')
        
        # Calculate SSIM, PSNR, bits
        output_stats = output_stats + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.txt'


 #    filesList = glob.glob(path_to_txt_files + 'ILSVRC2012_val_' + imgID + '*.txt')
 #    name = filesList[0].split('/')[-1]
	# qp = name.split('_')[-1].split('.')[0]
	# rgbStr = name.split('_')[-2]
	# height = int(name.split('_')[-3])
	# width  = int(name.split('_')[-4])

 #    INPUT_FILE = path_out_txt_files + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '.txt'
	# OUTPUT_ENC_FILE="./test_file/1000_0.265"
	# OUTPUT_DEC_FILE="./test_file/1000_0.yuv"
	# QP=0


	# cmd=['ffmpeg', '-f rawvideo -vcodec rawvideo -s', str(width), 'x', str(height), '-pix_fmt yuv420p -i', INPUT_FILE, '-c:v libx265 -crf ', QP, '-preset ultrafast', OUTPUT_DEC_FILE1]
	# print(cmd)
    #subprocess.call(['ffmpeg', '-i', INPUT_FILE, 'output.avi'])

