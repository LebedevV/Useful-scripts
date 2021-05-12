#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Vasily A. Lebedev"
__copyright__ = "Copyright 2019-2021, University of Limerick"
__license__ = "GPL-v2"
__email__ = "vasily.lebedev@ul.ie"
__website__ = "https://github.com/LebedevV/Useful-scripts"

'''
This python3 script allows one to plot integrated 2D-FFTs or ED simultaneously with XRD patterns

Analysis is performing in the current folder

FFT patterns should be saved in as files with "FFT" in name
ED patterns should be saved in as files with "ED" in name
Peak lists of each phase should be saved in 'pks' subfolder
XRD patterns should be saved in 'xrd' subfolder
'''

import os
import numpy
import scipy
import scipy.signal
import matplotlib.pyplot as plt

#Designed to parse files with structure:
'''
Line int
nm	Max Line	Avg Line
45.3603	201.756	131.528	
...
'''

def parse_lines(f1):
	k0 = open(f1)
	d0 = k0.readlines()
	k0.close()

	d0 = d0[3:]

	d0_x = []
	d0_y = []
	d0_y2 = []
	#replace to pandas
	for t in d0:
		t = t[:-2]
		#print(t)
		t = t.replace(',', '.')
		s = t.split('\t')
		#print(s)
		d0_x.append(float(s[0]))
		d0_y.append(float(s[1]))
		d0_y2.append(float(s[2]))

	d0_x = numpy.array(d0_x)
	d0_y = numpy.array(d0_y) #MaxLine
	d0_y2 = numpy.array(d0_y2) #AvgLine
	#Renorm
	#d0_y = d0_y/max(d0_y)
	#d0_y2 = d0_y2/max(d0_y2)

	return d0_x, d0_y2


def plot(diffr, sg=False, sgn=5, sgo=3):

	line_x, line_y = parse_lines(diffr)


	##########IMG###############

	plt.rcParams['figure.figsize'] = (8.0, 8.0)
	fig, ax = plt.subplots()
	plt.subplots_adjust(right=0.85, left=0, top=.95, bottom=0.05)
	ax.grid(True)
	ax.axes.get_xaxis().set_visible(False)
	ax.yaxis.tick_right()
	ax.yaxis.set_label_position("right")
	ax.set_ylim(0,max(line_x))

	ax.xaxis.label.set_size(20)
	ax.yaxis.label.set_size(20)
	ax.tick_params(labelsize=18)

	######################
	#plot FFT/ED
	ax.plot(line_y, line_x, ".r")

	plt.ylabel("$x$, nm")
	ax.set_title("Averaged intensity, rel.u.", fontsize=22, style='italic')
	#plt.xlabel("$1/d$, $nm ^{-1}$")
	plt.savefig(diffr[:-4]+'_line.png')
	#plt.show()
	plt.close()


l = os.listdir('.')

#Create lists of EDs and FFTs
line_list = []

for f in l:
	if os.path.isfile(f) and f.endswith('lint.txt'):
		line_list.append(f)

for f in line_list:
		print('Line plot for', f)
		#to smooth graphs by savgol, please, add 'sg = True'
		#for different parameters of savgol one may use sgn parameter () for window and sgo for degree

		# defaults: xrd = None, pks = None, sg = False, sgn = 5, sgo = 3
		plot(f)

print('Done!')
