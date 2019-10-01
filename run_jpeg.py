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

import os.path
import sys


PATH_TO_EXCEL = os.path.join( os.getcwd() , 'Alexnet50K-HEVC.xls') 

# START = 1
# END = 2

# For initial debugging:
# START = 1000
# Y only testing ILSVRC2012_val_00000126_504_376_Y.yuv
# START = 34
# END = START + 1 

# START = int(sys.argv[1])
# END   = 1 + int(sys.argv[2]) 
# print(START,END)

START = 1
END = 1 + 50000

# Create bpp ORG, SSIM Org, PSNR ORG lists.
shard_num = 0

MAIN_PATH = '/media/h2amer/MULTICOM-104/'

image_dir    = os.path.join(MAIN_PATH, 'validation_original')
image_QF_dir = os.path.join(MAIN_PATH, 'validation_generated_QF')
output_path  = os.path.join(MAIN_PATH, 'Seq-RECONS-ffmpeg')
output_path_stats = os.path.join(MAIN_PATH, 'Gen/Seq-Stats') 
output_path_stats_unified = os.path.join(MAIN_PATH, 'Gen/Seq-Stats-Unified') 



MAIN_PATH_hevc    = '/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/'
image_dir_hevc    = os.path.join(MAIN_PATH_hevc, 'pics')

# image_dir_hevc    = os.path.join(MAIN_PATH, 'set_yuv_102/pics')

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
QP.append(int(sys.argv[1]))
# for i in range(95, 0, -5):
#     QP.append(i)
# QP.append(0)
print(QP)

# for time
t = [0.0, 0.0, 0.0, 0.0]

# for imgID in range(START, END):
# for imgID in range(107, 107 + 1):
# for imgID in range(10001, 10001 + 1):
# for imgID in range(1, 1 + 2):
# for imgID in range(1, 1 + 2):
prev_t = 0
current_t = 0
for imgID in range(START, END):
# for imgID in range(34, 34 + 1):

    original_img_ID = imgID
    imgID = str(imgID).zfill(8)
    prev_shard = shard_num
    shard_num  = original_img_ID//10001
    

    check_shard = (original_img_ID-1)/10000
    # if not check_shard % 1 and original_img_ID != 10001 or prev_shard > shard_num and prev_shard != 0: # check if a number is integer
    if prev_shard > shard_num and prev_shard != 0: # check if a number is integer
        shard_num = shard_num + 1
    
    folder_num = math.ceil(original_img_ID/1000)

    glob_path = image_dir_hevc + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '*.yuv'

    filesList = glob.glob(glob_path)
    name = filesList[0].split('/')[-1].split('.')[0]
    rgbStr = name.split('_')[-1]
    height = int(name.split('_')[-2])
    width = int(name.split('_')[-3])

     
    if rgbStr.__contains__('Y'):
        input_format = 'gray'
    else:
        input_format = 'yuvj420p' # full range pixel format (0-255)
         


    # Construct current YUV image (from old dataset)
    # current_image = image_dir_hevc + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '.yuv'

    # from constructed dataset only in the first QP
    current_jpeg_image = image_dir + '/shard-' + str(shard_num) +  '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '.JPEG'
    current_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_ORG_' +  '.yuv'
    # current_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_ORG_' + str(QP[0]) + '.yuv'
    if not QP[0]:
        tStart = time.time()
        # convert JPEG into YUV:
        cmd = 'ffmpeg -loglevel panic -y -i ' + current_jpeg_image + ' -s ' +  str(width) + 'x' + str(height) + ' -pix_fmt ' + input_format + ' ' + current_image
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out, err = p.communicate()
        t[0] += time.time() - tStart


    # Encode via FFMPEG x265 to a different YUV file
    lines = []

  
    # 265: Put it as null
    output_265 = 'NULL'


    for qp in QP:

        tStart = time.time()

        # recons_image:
        recons_jpeg_image = image_QF_dir + '/shard-' + str(shard_num) + '/' + str(folder_num) + '/ILSVRC2012_val_' + imgID + '-QF-' + str(qp) + '.JPEG'

        # recons yuv image:
        recons_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.yuv'


        # convert JPEG into YUV:
        # ffmpeg -i test-640x480.jpg -s 640x480 -pix_fmt yuv420p test-yuv420p.yuv
        cmd = 'ffmpeg -loglevel panic -y -i ' + recons_jpeg_image + ' -s ' +  str(width) + 'x' + str(height) + ' -pix_fmt ' + input_format + ' ' + recons_image
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out, err = p.communicate()

        t[1] += time.time() - tStart

        #print(cmd)
        # print(current_image)
        # print(recons_image)
        # exit(0)

        
        tStart = time.time()
        # Calculate SSIM, PSNR, bpp
        output_stats = output_path_stats + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.txt'
        cmd = './jpeg_quality ' + current_image + " " + recons_image + " " + output_265 +  " " + output_stats
        p = os.popen(cmd).read()
        t[2] += time.time() - tStart
        # print(imgID, p)

        
        # if len(QP) != 1:        
        #     tStart = time.time()
        #     # Merge the text files on the go
        #     output_stats_unified = output_path_stats_unified + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '.txt'
        #     lines = readFileContents(output_stats)
        #     writeFileContents(output_stats_unified, lines)
        #     os.remove(output_stats)
        #     t[3] += time.time() - tStart
        
        # print(imgID)
        # print(qp)
    
    # Remove all original versions except the one for 100
    # if QP[0] != 100:
    #     os.remove(current_image)

    # print ('Elapsed time for 265 is %f seconds. ' % (t[0]))
    # print ('Elapsed time for YUV is %f seconds. ' % (t[1]))
    # print ('Elapsed time for calc_quality is %f seconds. ' % (t[2]))
    # print ('Elapsed time for aggregate files is %f seconds. ' % (t[3]))
    if not original_img_ID % 10:
        print('QP %d => Image ID %s is done in %f seconds' % (QP[0], imgID, (sum(t))) )
        t = [0.0, 0.0, 0.0, 0.0]

        # print(current_image)
        # print(recons_image)
        # print(output_265)
        # print(output_stats)
        # print(output_stats_unified)
        
        # if(err):
        #     print('')

print('Done!')
