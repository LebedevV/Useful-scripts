#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Vasily A. Lebedev"
__copyright__ = "Copyright 2019-2021, University of Limerick"
__license__ = "GPL-v2"
__email__ = "vasily.lebedev@ul.ie"
__website__ = "https://github.com/LebedevV/Useful-scripts"

import os
import cv2
import numpy as np

crop_fft = False

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

def combine_fft(d,png_dir,fft_dir,f):
	try:
#	if 1:
		scale_factor = 1

		fft_im_path = d+'/processed_data/'+fft_dir+'/'+f[:-4]+'_FFT_d-1.png'
		png_im_path = d+'/processed_data/'+png_dir+'/'+f[:-3]+'png'
		fin_im_path = d+'/processed_data/combined/fft_i/'+f[:-4]+'.png'

		fft = cv2.imread(fft_im_path)
		png = cv2.imread(png_im_path)
		scale_factor = scale_factor/(png.shape[0]/fft.shape[0])

		fft2 = cv2.resize(fft, None,fx=1/scale_factor, fy=1/scale_factor, interpolation = cv2.INTER_CUBIC)
		
		final_image = cv2.hconcat([png,fft2])
		
		cv2.imwrite(fin_im_path,final_image)
		cv2.destroyAllWindows()
	except:
		print("No combined fft image was created for ",f)

def combine_lines(d,png_dir,lin_dir,f):
	try:
#	if 1:
		scale_factor = .9

		lin_im_path = d+'/processed_data/'+lin_dir+'/'+f[:-4]+'_lint_line.png'
		png_im_path = d+'/processed_data/'+png_dir+'/'+f[:-3]+'png'
		fin_im_path = d+'/processed_data/combined/lin/'+f[:-4]+'_c.png'

		lin = cv2.imread(lin_im_path)
		#print(lin.shape)
		png = cv2.imread(png_im_path)
		#print(png.shape)
		scale_factor = scale_factor/(png.shape[0]/lin.shape[0])
		lin2 = cv2.resize(lin, None,fx=1/scale_factor, fy=1/scale_factor, interpolation = cv2.INTER_CUBIC)
		
		h1 = lin2.shape[1]
		h2 = png.shape[1]
		l1 = lin2.shape[0]
		l2 = png.shape[0]
		
		final_image = np.ones((max(h1,h2),l1+l2,3),dtype=np.uint8)
		final_image = final_image*255
		final_image[-h1:,-l1:] = lin2
		final_image[int(abs(h1-h2)/2):int(abs(h1-h2)/2)+h2,:l2] = png
		
		cv2.imwrite(fin_im_path,final_image)
		cv2.destroyAllWindows()
	except:
		print("No combined line image was created for ",f)

def combine_png(d,png_dir,fft_dir,crop_fft,f):
	try:
	#if 1:
		scale_factor = 4.

		fft_im_path = d+'/processed_data/'+fft_dir+'/'+f[:-3]+'png'
		png_im_path = d+'/processed_data/'+png_dir+'/'+f[:-3]+'png'
		fin_im_path = d+'/processed_data/'+'combined'+'/'+f[:-3]+'png'

		fft = cv2.imread(fft_im_path)
		
		#if crop_fft:
		#	dy = int(len(fft)/2)
		#	dx = int(len(fft[0])/2)
		#	fft = fft[dx-int(dx/2):dx+int(dx/2),dy-int(dy/2):dy+int(dy/2)] #TODO: check x&y directions 
		#	scale_factor*=.5
			
		png = cv2.imread(png_im_path)
		fft = cv2.resize(fft, None,fx=1/scale_factor, fy=1/scale_factor, interpolation=cv2.INTER_CUBIC)
		png[-len(fft):,-len(fft):]=fft #TODO add rectangulars support

		cv2.imwrite(fin_im_path,png)
		cv2.destroyAllWindows()
	except Exception as e:
 		print("No combined image was created for ",f)
 		print(e)

d='.' #Work in the current dir
l,ld = get_filelist(d) #Collect lists of files and dirs there
lf = filter_ending(l,['dm3','dm4','gwy']) #Select files of specified type
print(lf)
#Processing
if len(lf)>0:
	for f in lf:
		combine_png(d,'png','fft',crop_fft,f)
		combine_lines(d,'png','line_int',f)
		combine_fft(d,'png','fft_diff',f)
