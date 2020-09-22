#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = "Vasily A. Lebedev"
__copyright__ = "Copyright 2019-2020, University of Limerick"
__license__ = "GPL-v2"
__email__ = "vasily.lebedev@ul.ie"
__website__ = "https://github.com/LebedevV/Useful-scripts"

'''
This python2 script is a wrapper to the pygwy for the batch convert of usual TEM data to png
Author is grateful to the Gwyddion developers team, and personally to David Nečas
'''

import sys
import os
import cv2 #for the combine_png function only

#For FFT angular integration
import numpy as np
#import matplotlib.pyplot as plt

'''
Pygwy have to be compiled and installed in advance
Please, consult http://gwyddion.net , http://gwyddion.net/documentation/head/pygwy/ 
and https://sourceforge.net/p/gwyddion/discussion/pygwy/ for details
'''

#local path to pygwy lib
sys.path.append('/usr/local/lib64/python2.7/site-packages/')
import gwy

#For FFT angular integration
sys.path.append('/usr/local/share/gwyddion/pygwy/')
import gwyutils


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

#Create dirs for results
def create_dirs(d,ld,overwrite=False):
	l = ['png','fft','combined','logphi','diff_txt','fft_diff']
	p = ''
#######To rewrite
	try:
		for ll in l:
			os.mkdir(d+'/'+ll)
	except:
		print('Dir already exists')
#######
	return p


#Find all filenames with the selected type
def filter_ending(l,t):
	lf=[]
	for j in t:
		for ll in l:
			if ll.endswith(j):
				lf.append(ll)
	return lf


#General processing
#A lot of stuff currently binded to settings of Gwyddion/Save As...
#Please, make sure that these settings are correct
def proc_img(d,f,p):

	print(d+'/'+f)

	#open
	c = gwy.gwy_file_load(d+'/'+f,gwy.RUN_NONINTERACTIVE)
	gwy.gwy_app_data_browser_add(c)
	ids = set(gwy.gwy_app_data_browser_get_data_ids(c))
	print(ids)
	#select window
	gwy.gwy_app_data_browser_select_data_field(c, 0)

	#Is it an Image or a Diffraction pattern?
	#there is no obviuos ways to distinguish TEM and STEM images
	data = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)

	rotate = False
	angle = 203.5
	if rotate:
		ext = data.new_alike()
		data2 = data.new_rotated(ext,angle=angle/180.*np.pi,interp=gwy.INTERPOLATION_BSPLINE,resize=gwy.ROTATE_RESIZE_CUT)
		cc = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
		j = gwy.gwy_app_data_browser_add_data_field(data2, cc, True)
		gwy.gwy_app_data_browser_select_data_field(cc, j)
	else:
		cc = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
		data2 = data
	#gwy.gwy_app_data_browser_select_data_field(c, 2)
	#data = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)


	si = data2.get_si_unit_xy()
	txt_si=si.get_string(gwy.SI_UNIT_FORMAT_PLAIN)

	#import of all current saveas-settings
	settings = gwy.gwy_app_settings_get()
	#settings['/module/rotate/angle'] = 90

	ids = set(gwy.gwy_app_data_browser_get_data_ids(c))
	print(ids)

	#override of some saveas-settings
	settings['/module/pixmap/title_type'] = 0
	settings['/module/pixmap/ztype'] = 0
	settings['/module/pixmap/xytype'] = 2
	settings['/module/pixmap/draw_maskkey'] = False

	settings["/module/pixmap/inset_draw_label"] = True
	settings["/module/pixmap/inset_draw_text_above"] = False
	settings["/module/pixmap/draw_frame"] = False
	settings["/module/pixmap/inset_draw_ticks"] = False
	settings["/module/pixmap/inset_pos"] = 3 #bottom left
	settings["/module/pixmap/inset_xgap"] = 0.5
	settings["/module/pixmap/inset_ygap"] = 0.5

	settings["/module/pixmap/scale_font"] = False
	settings["/module/pixmap/font_size"] = 40.
	settings["/module/pixmap/outline_width"] = 0.
	settings["/module/pixmap/line_width"] = 10.

	# ... (*lots* of possible settings, see ~/.gwyddion/settings)

	#Rescale to 1024px
	res = data2.get_xres()
	print(res)
	settings['/module/pixmap/zoom'] = 1024./res

	if txt_si == 'm':
		print("Image")
		#Saving the original image
		#'''
		#change palette
		cc['/0/base/palette'] = 'Gray'
		#change range of palette to Auto
		cc['/0/base/range-type'] = int(gwy.LAYER_BASIC_RANGE_AUTO)
		#inset_length "10 nm"
	
		#Changing scalebar color to white
		settings['/module/pixmap/inset_color/blue'] = 1.
		settings['/module/pixmap/inset_color/red'] = 1.
		settings['/module/pixmap/inset_color/green'] = 1.

		#Save png
		gwy.gwy_file_save(cc,d+'/png'+p+'/'+f[:-3]+'png',gwy.RUN_NONINTERACTIVE)
		#'''

		#Automated patterns detection by PSDF
		'''
		line = gwy.DataLine(1, 1, True)
		dd = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
		dd.rpsdf(line, gwy.INTERPOLATION_LINEAR, gwy.WINDOWING_HANN, -1)
	
		ux = line.get_si_unit_x()
		uy = line.get_si_unit_y()
		print ux.get_string(gwy.SI_UNIT_FORMAT_PLAIN)
		print uy.get_string(gwy.SI_UNIT_FORMAT_PLAIN)

		phys_y = line.get_data()
		#print([xx for xx in range(0,len())])
		#print(line.get_dx())
	 
		print(line.get_data()[0])
		print(line.get_data()[1])
		plt.plot(phys_y)
		plt.show()	
		'''
		
		#FFT plot
		#'''
		gwy.gwy_app_data_browser_select_data_field(c, 0)
		dd = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
		cc = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
		empty = dd.new_alike()
		fftre = dd.new_alike()
		fftim = dd.new_alike()
		# see http://gwyddion.net/documentation/head/pygwy/gwy.DataField-class.html#fft2d
		dd.fft2d(empty, fftre, fftim,
			gwy.WINDOWING_HANN,
			#gwy.WINDOWING_NONE,
			gwy.TRANSFORM_DIRECTION_FORWARD,
			gwy.INTERPOLATION_LINEAR, True, 1)
		fftre.fft_postprocess(True)
		fftim.fft_postprocess(True)
		fftre.hypot_of_fields(fftre, fftim)
		#modulus
		'''
		a = fftre.get_data()
		visualize = fftre.new_alike()
		visualize.set_data([numpy.sqrt(x) for x in a])
		print max([numpy.sqrt(x) for x in a]),min([numpy.sqrt(x) for x in a])
		#'''
		#visualize.filter_gaussian(1)
		#probably we need in some outliers filter here
#		i = gwy.gwy_app_data_browser_add_data_field(visualize, cc, True)
		i = gwy.gwy_app_data_browser_add_data_field(fftre, cc, True)
		#key = gwy.gwy_name_from_key(gwy.gwy_app_get_data_title_key_for_id(i))
		#cc[key] = 'FFT Modulus'
		gwy.gwy_app_data_browser_select_data_field(cc, i)

		#Radial integration of the obtained FFT, direct approach
		#Needs to be fixed
		'''
		prof = gwy.DataLine(1, 1.)
		dd.copy_units_to_data_line(prof)
		data.angular_average(prof, None, gwy.MASK_IGNORE, data.itor(1024.0), data.jtor(1024.0), data.itor(2000), 10000)
		fh = open(d+'/fft_diff'+p+'/'+f[:-4]+'_FFT.txt', 'w')
		fh.write("Radial profile\n")             
		fh.write('m-1\n')  
		dx = prof.get_dx()
		for i, y in enumerate(prof.get_data()):
			fh.write('%g  %g\n' % (i*dx*10**9, y))
		fh.close()
		'''

		#Save FFT image with the appropriate palette and inset scalebar color
		cc['/'+str(i)+'/base/palette'] = 'DFit'#'Blue-Violet'
		cc['/'+str(i)+'/base/range-type'] = int(gwy.LAYER_BASIC_RANGE_AUTO)
		gwy.gwy_file_save(cc,d+'/fft'+p+'/'+f[:-3]+'png',gwy.RUN_NONINTERACTIVE)
		#'''

		#'''
		#psdf2d
		gwy.gwy_app_data_browser_select_data_field(c, 0)
		dd = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
		cc = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

		old_id = set(gwy.gwy_app_data_browser_get_data_ids(cc))
		gwy.gwy_process_func_run('psdf_logphi',cc, gwy.RUN_IMMEDIATE)
		new_id = set(gwy.gwy_app_data_browser_get_data_ids(cc))
		i_psdf = list(new_id - old_id)
	#	i = gwy.gwy_app_data_browser_add_data_field(psdf, cc, True)
	#	key = gwy.gwy_name_from_key(gwy.gwy_app_get_data_title_key_for_id(i))
	#	cc[key] = 'PSDF'

		gwy.gwy_app_data_browser_select_data_field(cc, i_psdf[0])
		cc['/2/base/palette'] = 'DFit'#'Blue-Violet'
		cc['/2/base/range-type'] = int(gwy.LAYER_BASIC_RANGE_AUTO)
		gwy.gwy_file_save(cc,d+'/logphi'+p+'/'+f[:-3]+'png',gwy.RUN_NONINTERACTIVE)


		#Look for a max value for each R
		#'''
		psdf = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD) #get psdf
		np_psdf = gwyutils.data_field_data_as_array(psdf)

		yoff = psdf.get_yoffset()
		#print(yoff,"y off")
		psdf_dy = psdf.get_dy()
		#print(psdf_dy,"y dy")
		max_fft_y = [max(i) for i in np_psdf.T]
		avg_fft_y = [sum(i)/len(i) for i in np_psdf.T]
		i = 0
		max_fft_x = []
		while i<len(max_fft_y):
			max_fft_x.append(np.exp(yoff + i*psdf_dy)/10**9)
			i+=1
		"""
		plt.plot(max_fft_x,max_fft_y)
		plt.xlabel('$1/d, nm^{-1}$')
		plt.ylabel('Max FFT value, rel. u.')
		plt.savefig(d+'/fft_diff'+p+'/'+f[:-4]+'_FFT.png')
		plt.close()
		"""

		fh = open(d+'/fft_diff'+p+'/'+f[:-4]+'_FFT.ed', 'w')
		fh.write("PSDF\n")             
		fh.write('nm-1\tMax FFT\tAvg FFT\n')
		i = 0
		while i<len(max_fft_y):
			fh.write('%g\t%g\t%g\t\n' % (max_fft_x[i], max_fft_y[i], avg_fft_y[i]))
			i+=1

		#'''


		#Similar approach, but without numpy and gwyutils
		#needs to be fixed
		'''
		gwy.gwy_app_data_browser_select_data_field(c, 0)
		dd = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
		cc = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)

		prof = gwy.DataLine(1, 1.)
		dd.rpsdf(prof,gwy.INTERPOLATION_LINEAR,gwy.WINDOWING_HANN,0)
		y = prof.get_data()
		plt.plot(y)
		plt.show()
		plt.close()
		#'''



	elif txt_si == 'm^-1':
		print('Diffraction pattern')
		#'''

		#change palette
		c['/0/base/palette'] = 'Gray-inverted'
		#change range of palette to Auto
		c['/0/base/range-type'] = int(gwy.LAYER_BASIC_RANGE_AUTO)

		#data.data_changed()
		#inset_length "10 nm"
	
		#Changing scalebar color to black
		settings['/module/pixmap/inset_color/blue'] = 0.
		settings['/module/pixmap/inset_color/red'] = 0.
		settings['/module/pixmap/inset_color/green'] = 0.

		#Save png
		gwy.gwy_file_save(c,d+'/png'+p+'/'+f[:-3]+'png',gwy.RUN_NONINTERACTIVE)
		#'''

		#Radial integration of diffraction pattern
		#Needs to be fixed
		'''
		#xres = data.get_xres()
		xr = data.get_xreal()
		prof = gwy.DataLine(1, 1.0)
		data.angular_average(prof, None, gwy.MASK_IGNORE, data.itor(1024.0), data.jtor(1024.0), data.itor(1024.0), 1000)
		fh = open('myrprofile.txt', 'w')
		dx = prof.get_dx()
		for i, y in enumerate(prof.get_data()):
			fh.write('%g  %g\n' % (i*dx, y))
		fh.close()
		#'''

	gwy.gwy_app_data_browser_remove(c)



def combine_png(d,png_dir,fft_dir,f):
	try:
	#if 1:
		scale_factor = 4.

		fft_im_path = d+'/'+fft_dir+'/'+f[:-3]+'png'
		png_im_path = d+'/'+png_dir+'/'+f[:-3]+'png'
		fin_im_path = d+'/'+'combined'+'/'+f[:-3]+'png'

		fft = cv2.imread(fft_im_path)
		png = cv2.imread(png_im_path)
		fft = cv2.resize(fft, None,fx=1/scale_factor, fy=1/scale_factor, interpolation = cv2.INTER_CUBIC)
		png[-len(fft):,-len(fft):]=fft

		cv2.imwrite(fin_im_path,png)
		cv2.destroyAllWindows()
	except:
		print("No combined image was created for ",d)


d='.' #Work in the current dir
l,ld = get_filelist(d) #Collect lists of files and dirs there
lf = filter_ending(l,['dm3','dm4','gwy']) #Select files of specified type

#Processing
if len(lf)>0:
	p = create_dirs(d,ld)
	for f in lf:
		proc_img(d,f,p)
		combine_png(d,'png','fft',f)
