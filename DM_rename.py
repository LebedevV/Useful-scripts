#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = "Vasily A. Lebedev"
__copyright__ = "Copyright 2019-2021, University of Limerick"
__license__ = "GPL-v2"
__email__ = "vasily.lebedev@ul.ie"
__website__ = "https://github.com/LebedevV/Useful-scripts"

import hyperspy.api as hs
import os

def proc_img(d,f):
	s = hs.load(d+'/'+f)
	mag = s.metadata.Acquisition_instrument.TEM.magnification
	
	return mag

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


def filter_ending(l,t):
	lf=[]
	for j in t:
		for ll in l:
			if ll.endswith(j):
				lf.append(ll)
	return lf

d='.' #Work in the current dir
l,ld = get_filelist(d) #Collect lists of files and dirs there
lf = filter_ending(l,['dm3','dm4']) #Select files of specified type


#Processing
if len(lf)>0:
	for f in lf:
		mag = proc_img(d,f)
		mag = str(int(mag)) + 'X'
		if mag not in f:
			os.rename(f,mag+'_'+f)
			print(f,' renamed')
		else:
			print(f,' not renamed')
