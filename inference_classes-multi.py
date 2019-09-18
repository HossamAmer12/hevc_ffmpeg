# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 23:43:32 2019

@author: ahamsala
"""
import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
# Video capture and convert rgb 
import cv2
import time

# Excel sheet stuff:
import xlrd
from xlwt import *
from xlutils.copy import copy
import math
import sys

file_xls  = int(sys.argv[1]) #xls ID 
st = int(sys.argv[2]) # start Image 
end = int(sys.argv[3]) # End Image
print(type(file_xls)) 
# print(start)
# print(end)
 # path_to_excel = PATH_TO_DISC + '/Accuracy Record ILSVRC2012 Top 1 - HEVC.xls'
PATH_TO_EXCEL = os.path.join( os.getcwd() , (('Alexnet-QF-%d.xls')%file_xls))
# path to class file names 
DATA_PATH = 'G:\\validation_generated_QF\\shard-%d\\%d\\ILSVRC2012_val_%s-QF-%d.JPEG'

PATH_TO_DISC = 'D:\comparison_project\Alex_net\Alex-net-inference'
PATH_TO_FILE_NAMES  = os.path.join(os.getcwd() , 'binsMapIndex.txt' )


#mean of imagenet dataset in BGR
imagenet_mean = np.array([104., 117., 124.], dtype=np.float32)

image_dir = r'D:\Research\org_jpg_images'

from alexnet import AlexNet
from caffe_classes import class_names


def construct_all_list(classNo):
	print('Constructing all list for Class-%d...' % classNo)
	class_filename       = 'class' + str(classNo) + '.txt'
	path_to_class_file   = os.path.join(PATH_TO_DISC + '\\classes', class_filename)
	all_list  = [x.split('\n')[0] for x in open(path_to_class_file).readlines()]
	return all_list



def mak_list():
	print('list of images is generated')
	all_list =  [x.split('\n')[0] for x in open(PATH_TO_FILE_NAMES).readlines() ]
	return all_list 

def writeFileContents(name,i):
	f = open((('error_not_found-G-%d.txt')%i), "a")
	f.write(name+'\n')
	f.close()


def rank_estimate(probs , gt_label_list , idx , sheet , col_idx, wb ):
	predictions = np.squeeze(probs)
	N = - 1000
	rank = -1 
	predictions = np.squeeze(predictions)
	top_5 = predictions.argsort()[N:][::-1]
	for rank, node_id in enumerate(top_5):
		human_string = class_names[node_id]
		score = predictions[node_id]
		if(gt_label_list[idx] == human_string):
			row = idx            
			current_rank =  1 + rank 
			style = XFStyle()
			style.num_format_str = 'general'
			    
			sheet.write(row , col_idx , current_rank , style)            
			sheet.write(row , 1 + col_idx , score.item() , style)
			wb.save(PATH_TO_EXCEL)
			break
	return current_rank





def readAndpredictloop():
	    
	    
	## reset default graph 

	tf.reset_default_graph()

	#placeholder for input and dropout rate
	x = tf.placeholder(tf.float32, [1, 227, 227, 3])
	keep_prob = tf.placeholder(tf.float32)

	#create model with default config ( == no skip_layer and 1000 units in the last layer)
	model = AlexNet(x, keep_prob, 1000, [])

	#define activation of last layer as score
	score = model.fc8

	#create op to calculate softmax 
	softmax = tf.nn.softmax(score)


	with tf.Session() as sess:

		# Create the excel sheet workbook
		path_to_excel = PATH_TO_EXCEL
		rb = xlrd.open_workbook(path_to_excel, formatting_info=True)
		wb = copy(rb)
		sheet = wb.get_sheet(0)
		style = XFStyle()
		style.num_format_str = 'general'

		# Get the ground truth list
		sheet_r  = rb.sheets()[0]
		gt_label_list = sheet_r.col_values(1)

		    
		# Initialize all variables
		sess.run(tf.global_variables_initializer())

		# Load the pretrained weights into the model
		model.load_initial_weights(sess)

		# Create figure handle
		#fig2 = plt.figure(figsize=(15,6))

		# Loop over all images
		# for i, name in enumerate(all_list[0:35000]):
		for imgID in range(st, end):
			original_img_ID = imgID
			imgID = str(imgID).zfill(8)
			shard_num  = math.floor((original_img_ID-1)/10000);
			folder_num = math.floor((original_img_ID-1)/1000)+1;
			#'G:\\validation_generated_QF\\shard-%d\\%d\\ILSVRC2012_val_%d-QF-%d.JPEG'
			start = time.time()
			qp_list = [i for i in range (0,52 , 2)]
			qp_list.append(51)
			for qf in qp_list:			
				col_idx = int( 2*qf/5) + 4 
				# print(col_idx)
				row = original_img_ID
				actual_idx = original_img_ID
				style = XFStyle()
				style.num_format_str = 'general'
				# if (sheet_r.cell(row,col_idx+1).value==u''):
				name = ((DATA_PATH)%(shard_num,folder_num,imgID,qf))
				image = cv2.imread(name)
				# Convert image to float32 and resize to (227x227)
				try :
					img = cv2.resize(image.astype(np.float32), (227,227))

					# Subtract the ImageNet mean
					img -= imagenet_mean

					# Reshape as needed to feed into model
					img = img.reshape((1,227,227,3))

					# Run the session and calculate the class probability
					probs = sess.run(softmax, feed_dict={x: img, keep_prob: 1})

					rank_estimate(probs , gt_label_list , actual_idx , sheet , col_idx, wb )
				except:
					writeFileContents(name,file_xls)
					continue

			print ('image %s is done , time: %f' %(imgID,time.time()-start))
                        
def get_sheet():
	path_to_excel = PATH_TO_EXCEL
	rb = xlrd.open_workbook(path_to_excel, formatting_info=False)
	wb = copy(rb)
	sheet = wb.get_sheet(0)
	style = XFStyle()
	style.num_format_str = 'general'

	#print('Done excel sheet creation')

	# Get the ground truth list
	sheet_r = rb.sheets()[0]
	gt_label_list = sheet_r.col_values(1)
	return gt_label_list
            
print('done list construction')
readAndpredictloop()
     