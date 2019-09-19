
import matplotlib.pyplot as plt
import os 
import numpy as np 

import xlrd
from xlwt import *
from xlutils.copy import copy 

import time


def write_to_final(start_row, end_row, sheet, data):

	style = XFStyle()
	style.num_format_str = 'general'

	for icol, col in enumerate(data):
		
		# Skip the first two cols
		if icol < 2:
			continue

		for irow, row in enumerate(col):

			# Write only in this range
			if irow >= start_row and irow < end_row:
				sheet.write(irow, icol, row, style)
			
def write_to_final_straight_to_sheet(start_row, end_row, dst_sheet, src_sheet):

	style = XFStyle()
	style.num_format_str = 'general'

	# Skip the first two cols
	for icol in range(2, 56):
		
		col = src_sheet.col_values(icol)

		for irow, row in enumerate(col):

			# Write only in this range
			if irow >= start_row and irow < end_row:
				dst_sheet.write(irow, icol, row, style)



def readFileContents(image):
	f = open(image, "r")	
	bpp = np.loadtxt(f, delimiter ='\n', usecols =(0), unpack = True)
	f.close()
	return bpp

## reading data 
final_file = '/home/h2amer/work/workspace/alexnet_inference/Alexnet-JPEG.xls'

for idx in range (1, 50000, 100):
	
	start_time = time.time()
	START = idx
	END   = START + 99

	name = 'Alexnet-Qp-All' + '_' + str(START) + '_' + str(END) + '.xls'
	path_to_excel = os.path.join('/home/h2amer/work/workspace/alexnet_inference/', name)
		

	# Get the source sheet
	rb       = xlrd.open_workbook(path_to_excel, formatting_info=True)
	sheet_r  = rb.sheets()[0]

	# Open the desination sheet
	rb_f     = xlrd.open_workbook(final_file, formatting_info=True)
	wb_f     = copy(rb_f)
	sheet_f  = wb_f.get_sheet(0)
	
	write_to_final_straight_to_sheet(START, END, sheet_f, sheet_r)
	wb_f.save(final_file)

	elapsed_time = time.time() - start_time
	print('Done with %d in %f minutes' % (idx, elapsed_time/60.0))
