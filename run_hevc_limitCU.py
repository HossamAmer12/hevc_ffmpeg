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

#START = 1
#END   = 1 + 10000  


START = 1
END   = 1 + 1000


# Create bpp ORG, SSIM Org, PSNR ORG lists.
shard_num = 0

# MAIN_PATH    = '/media/h2amer/MULTICOM102/103_HA/MULTICOM103/set_yuv/'
# image_dir    = os.path.join(MAIN_PATH, 'pics')
# output_path  = os.path.join(MAIN_PATH, 'Seq-RECONS-ffmpeg-noInLoop')
# output_path_265  = os.path.join(MAIN_PATH, 'Seq-265-ffmpeg-noInLoop')
# output_path_stats = os.path.join(MAIN_PATH, 'Gen/Seq-Stats-noInLoop')
# output_path_stats_unified = os.path.join(MAIN_PATH, 'Gen/Seq-Stats-Unified-noInLoop') 



# MAIN_PATH    = '/media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/'
MAIN_PATH    = '/media/h2amer/MULTICOM-104/103_HA/MULTICOM103/set_yuv/'
image_dir    = os.path.join(MAIN_PATH, 'test')
output_path  = os.path.join(MAIN_PATH, 'Seq-RECONS-ffmpeg-noInLoop_168')
output_path_265  = os.path.join(MAIN_PATH, 'Seq-265-ffmpeg-noInLoop_168')
output_path_stats = os.path.join(MAIN_PATH, 'Gen/Seq-Stats-noInLoop_168')
output_path_stats_unified = os.path.join(MAIN_PATH, 'Gen/Seq-Stats-Unified-noInLoop_168') 



def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

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
QP.append(51)
for i in range(50, 0, -2):
    QP.append(i)
QP.append(0)

# QP.append(51)
print(QP)

# Create necessary directories
ensure_dir_exists(output_path)
ensure_dir_exists(output_path_265)
ensure_dir_exists(output_path_stats)
ensure_dir_exists(output_path_stats_unified)

# for time
t = [0.0, 0.0, 0.0, 0.0]

# for imgID in range(START, END):
for imgID in range(1, 2):
# for imgID in range(107, 107 + 1):
#for imgID in range(651, 651 + 1):
# for imgID in range(18454, 18454 + 1):

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
        #input_format = 'yuvj420p'
         

        # Calculate SSIM, PSNR, bpp
        # qp = QP[0]
        # output_265 = output_path_265 + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.265'
        # recons_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.yuv'
        # output_stats = output_path_stats + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.txt'
        # cmd = './calc_quality ' + current_image + " " + recons_image + " " + output_265 +  " " + output_stats
        # p = os.popen(cmd).read()
        #continue # continue for now

   
    # current_jpeg_image: for Y only
    #/home/h2amer/work/workspace/ML_TS/validation_original/shard-0/1/ILSVRC2012_val_00000034.JPEG
    current_jpeg_image = os.path.join('/home/h2amer/work/workspace/ML_TS/validation_original/', 'shard-' + str(shard_num) + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '.JPEG')  

    # convert jpeg into yuv ussing ffmpeg    
    # if rgbStr.__contains__('Y'):
    # cmd = 'ffmpeg -y -i ' + current_jpeg_image + ' -s ' + str(width) + 'x' + str(height) + ' -pix_fmt ' + input_format + ' ' + current_image
    # print(cmd)
    # print(current_jpeg_image)
    # print(current_image)
    # p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    # out, err = p.communicate()


    # Encode via FFMPEG x265 to a different YUV file
    lines = []

  

    for qp in QP:

        tStart = time.time()
        # 265:
        output_265 = output_path_265 + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.265'


        # ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v hevc -crf 51 -f hevc -x265-params no-deblock=1 -preset ultrafast /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265

        # cmd = 'ffmpeg -loglevel panic -y -f rawvideo -pix_fmt ' + input_format + ' -s:v ' + str(width) + 'x' + str(height) +  ' -i ' \
        #  + current_image + ' -c:v hevc -crf ' + str(qp) + ' -f hevc -preset ultrafast -x265-params no-deblock=1:no-sao=1:ctu=16:min-cu-size=8 ' + output_265
        cmd = 'ffmpeg -loglevel panic -y -f rawvideo -pix_fmt ' + input_format + ' -s:v ' + str(width) + 'x' + str(height) +  ' -i ' \
         + current_image + ' -c:v hevc -crf ' + str(qp) + ' -f hevc -preset ultrafast -x265-params no-deblock=1:no-sao=1:ctu=16:min-cu-size=8 ' + output_265
        print(cmd)

        #cmd = 'ffmpeg -y -f rawvideo -pix_fmt yuv420p -s:v 504x384 -i /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/test/1/ILSVRC2012_val_00000651_504_384_RGB.yuv -c:v hevc -crf 51 -f hevc -preset ultrafast -x265-params no-deblock=1 /media/h2amer/MULTICOM105/103_HA/MULTICOM103/set_yuv/Seq-265-ffmpeg-noInLoop/1/ILSVRC2012_val_00000651_504_384_RGB_51.265'
        
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out, err = p.communicate()

        t[0] += time.time() - tStart
        
        tStart = time.time()
        # YUV:
        tStart = time.time()
        recons_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.yuv'
        cmd = 'ffmpeg -loglevel panic -y  -i ' + output_265 + ' -s ' +  str(width) + 'x' + str(height) + ' -c:v rawvideo -pix_fmt ' + input_format + ' -preset ultrafast ' + recons_image
        print(cmd)
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out, err = p.communicate()

        # special edge cases like 706:
        if not os.path.exists(recons_image):
            cmd = 'ffmpeg -loglevel panic -y -f rawvideo -pix_fmt ' + input_format + ' -s:v ' + str(width) + 'x' + str(height) +  ' -i ' \
            + current_image + ' -c:v hevc -crf ' + str(qp) + ' -f hevc -preset ultrafast -x265-params no-deblock=1:no-sao=1:ctu=16:min-cu-size=8:allow-non-conformance ' + output_265
            p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            out, err = p.communicate()

            t[0] += time.time() - tStart

            tStart = time.time()
            recons_image = output_path + '/' + str(folder_num) + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.yuv'
            cmd = 'ffmpeg -loglevel panic -y  -i ' + output_265 + ' -s ' +  str(width) + 'x' + str(height) + ' -c:v rawvideo -pix_fmt ' + input_format + ' -preset ultrafast ' + recons_image
            p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            out, err = p.communicate()
        
            

        t[1] += time.time() - tStart
        
        tStart = time.time()
        # Calculate SSIM, PSNR, bpp
        output_stats = output_path_stats + '/' + 'ILSVRC2012_val_' + imgID + '_' + str(width) + '_' + str(height) + '_' + rgbStr + '_' + str(qp) + '.txt'
        cmd = './calc_quality ' + current_image + " " + recons_image + " " + output_265 +  " " + output_stats
        p = os.popen(cmd).read()


        t[2] += time.time() - tStart
        
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
        
    # print ('Elapsed time for 265 is %f seconds. ' % (t[0]))
    # print ('Elapsed time for YUV is %f seconds. ' % (t[1]))
    # print ('Elapsed time for calc_quality is %f seconds. ' % (t[2]))
    # print ('Elapsed time for aggregate files is %f seconds. ' % (t[3]))
    if not original_img_ID % 2:
        print('Image ID %s is done in %f seconds' % (imgID, (sum(t))) )
        t = [0.0, 0.0, 0.0, 0.0]

        # print(current_image)
        # print(recons_image)
        # print(output_265)
        # print(output_stats)
        # print(output_stats_unified)
        
        # if(err):
        #     print('')