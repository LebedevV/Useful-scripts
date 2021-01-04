#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Vasily A. Lebedev"
__copyright__ = "Copyright 2019-2020, University of Limerick"
__license__ = "GPL-v2"
__email__ = "vasily.lebedev@ul.ie"
__website__ = "https://github.com/LebedevV/Useful-scripts"

import os
import cv2

#Collect file and dirs lists
def get_filelist(d):
	l = os.listdir(d)
	#l = sorted(l)
	lf = []
	ld = []
	for i in l:
		if os.path.isfile(d+'/'+i):
			lf.append(i)
		elif os.path.isdir(d+'/'+i):
			ld.append(i)
	return lf,ld

#Find all filenames with the selected type
def filter_ending(l,t):
	lf=[]
	for j in t:
		for ll in l:
			if ll.endswith(j):
				lf.append(ll)
	return lf

def combine_png(d,png_dir,fft_dir,f):
	try:
	#if 1:
		scale_factor = 4.

		fft_im_path = d+'/processed_data/'+fft_dir+'/'+f[:-3]+'png'
		png_im_path = d+'/processed_data/'+png_dir+'/'+f[:-3]+'png'
		fin_im_path = d+'/processed_data/'+'combined'+'/'+f[:-3]+'png'

		fft = cv2.imread(fft_im_path)
		png = cv2.imread(png_im_path)
		fft = cv2.resize(fft, None,fx=1/scale_factor, fy=1/scale_factor, interpolation = cv2.INTER_CUBIC)
		png[-len(fft):,-len(fft):]=fft

		cv2.imwrite(fin_im_path,png)
		cv2.destroyAllWindows()
	except:
		print("No combined image was created for ",f)

d='.' #Work in the current dir
l,ld = get_filelist(d) #Collect lists of files and dirs there
lf = filter_ending(l,['dm3','dm4','gwy']) #Select files of specified type
print(lf)
#Processing
if len(lf)>0:
	for f in lf:
		combine_png(d,'png','fft',f)
