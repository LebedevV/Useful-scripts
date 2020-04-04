#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Vasily A. Lebedev"
__copyright__ = "Copyright 2019-2020, University of Limerick"
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
import scipy
import scipy.signal
import matplotlib.pyplot as plt

#Designed for xy files with structure:
'''
Sample "Test"
lambda = 0.1
2Theta	I
...
'''
def parse_xrd(name):
	k1 = open('./xrd/'+name)

	#Uncomment, if you wish to take phase name from the file name. Not recommended.
	'''
	ph_name = name.split('/')
	ph_name = ph_name[-1]
	ph_name = ph_name[:-4]
	#'''
	wavel = 1.54
	ph_name = ''
	while 1:
		s = k1.readline()
		if "Sample" in s:
			ph_name = s.split('\"')
			ph_name = ph_name[1]
		if 'lambda' in s:
			wavel = s.split('=')[1]
			wavel = float(wavel)
			break

	wavel = wavel/10 #Angstroms to nm

	s = k1.readline()
	d1 = k1.readlines()
	k1.close()

	d1_x = []
	d1_y = []

	#replace to pandas
	for s in d1:
		s = s.replace('   ', ' ')
		s = s.replace('  ', ' ')
		s = s.replace('  ', ' ')
		s = s.replace(',', ' ')
		s = s.replace('\t', ' ')
		s = s.split(' ')

		d1_x.append(float(s[0]))
		d1_y.append(float(s[1]))

	d1_y = scipy.array(d1_y)
	d1_x = scipy.array(d1_x)

	d1_x = 2*scipy.sin(d1_x*scipy.pi/180./2.)/wavel
	d1_y = d1_y/max(d1_y)

	return ph_name, d1_x, d1_y


#Designed for pks files with structure:
'''
...
Peaklist "Phase name"
   d	2Theta	I	...
...
'''
#LaTeX notation in phase name is allowed, "$CuSO_{4}\cdot 5 H_{2}O$"

def parse_pks(name):
	k1 = open('./pks/'+name)
#	k1 = open(l)

	while 1:
		s = k1.readline()
		#print(s)
		if 'Peak' in s and 'list' in s:
			break

	ph_name = s.split('\"')
	ph_name = ph_name[1]

	#Uncomment, if you wish to take phase name from the file name. Not recommended.
	'''
	ph_name = name.split('/')
	ph_name = ph_name[-1]
	ph_name = ph_name[:-4]
	'''

	s = k1.readline()
	d1 = k1.readlines()
	k1.close()

	d1_x = []
	d1_y = []
	#replace to pandas
	for s in d1:
		s = s.replace('   ', ' ')
		s = s.replace('  ', ' ')
		s = s.replace('  ', ' ')
		s = s.replace(',', ' ')
		s = s.replace('\t', ' ')
		s = s.split(' ')

		d1_x.append(float(s[1]))
		d1_y.append(float(s[3]))

	d1_y = scipy.array(d1_y)
	d1_x = scipy.array(d1_x)
	d1_x = 10./d1_x #From direct Angstroms to reciprocal nm's
	d1_y = d1_y/max(d1_y) #Renorm to 1

	return ph_name, d1_x, d1_y


def parse_ed(f1):
	k0 = open(f1)
	d0 = k0.readlines()
	k0.close()
	d0 = d0[3:]

	d0_x = []
	d0_y = []

	for t in d0:
		q = len(t)-2
		t = t[:q]
		t = t.replace(',', '.')
		s = t.split('  ')
		d0_x.append(float(s[0]))
		d0_y.append(float(s[1]))

	d0_x = scipy.array(d0_x)
	d0_y = scipy.array(d0_y)
	d0_x = d0_x / 10**9 #m-1 to nm-1
	d0_y = d0_y/max(d0_y) #Renorm to 1
	return d0_x, d0_y


#Designed to parse files with structure:
'''
PSDF
nm-1	Max FFT	Avg FFT
0.00150927	0.487692	0.165491
...
'''

def parse_fft(f1):
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
		t = t.replace(',', '.')
		s = t.split('\t')
		d0_x.append(float(s[0]))
		d0_y.append(float(s[1]))
		d0_y2.append(float(s[2]))

	d0_x = scipy.array(d0_x)
	d0_y = scipy.array(d0_y) #MaxFFT
	d0_y2 = scipy.array(d0_y2) #AvgFFT
	#Renorm
	d0_y = d0_y/max(d0_y)
	d0_y2 = d0_y2/max(d0_y2)

	return d0_x, d0_y


def plot(diffr, xrd=None, pks=None, sg=False, sgn=5, sgo=3, direct=False, ed=False):

	if ed:
		fft_x, fft_y = parse_ed(diffr)
	else:
		fft_x, fft_y = parse_fft(diffr)

	if direct:
		fft_x = 10/fft_x
	if sg:
		fft_x, fft_y = scipy.signal.savgol_filter([fft_x, fft_y], sgn, sgo, axis=1, deriv=0)


	if xrd:
		xrd_set = []
		for i in xrd:
			xrd_ph, xrd_d, xrd_i = parse_xrd(i)
			if sg:
				xrd_d, xrd_i = scipy.signal.savgol_filter([xrd_d, xrd_i], sgn, sgo, axis=1, deriv=0)
			if direct:
				xrd_d = 10/xrd_d
			xrd_set.append([xrd_ph, xrd_d, xrd_i])

	if pks:
		pks_l = []
		for i in pks:
			pks_ph, pks_d, pks_i = parse_pks(i)
			if direct:
				pks_d = 10/pks_d
			pks_l.append([pks_ph, pks_d, pks_i])


	##########IMG###############

	plt.rcParams['figure.figsize'] = (8.0, 6.0)
	fig, ax = plt.subplots()
	plt.subplots_adjust(right=0.95, left=0.1, top=0.95, bottom=0.13)
	ax.grid(True)
	#ax.axes.get_yaxis().set_visible(False)
	if direct:
		ax.set_xlim(0.5, 5)
	else:
		ax.set_xlim(2, 12)

	ax.xaxis.label.set_size(16)
	ax.yaxis.label.set_size(16)
	ax.tick_params(labelsize=14)

	######################
	#plot FFT/ED
	if ed:
		ax.plot(fft_x, fft_y, "b", label="ED")
	else:
		ax.plot(fft_x, fft_y, "b", label="FFT max")

	#plot peaks
	c = ['r', 'g', 'c', 'm', 'y'] #Colors order for a limited number of patterns
	if pks:
		if len(pks_l) <= len(c):
			i = 0
			for p in pks_l:
				ax.bar(p[1], p[2], label=p[0], width=.03, color=c[i])
				i += 1
		else:
			for p in pks_l:
				ax.bar(p[1], p[2], label=p[0], width=.03)
	#plot xrd
	if xrd:
		for a in xrd_set:
			ax.plot(a[1], a[2], label=a[0]+' XRD')
	######################
	if direct:
		ax.legend(loc='upper left', fontsize=16)
	else:
		ax.legend(loc='upper right', fontsize=16)

	plt.ylabel("$I$, rel. units")

	if direct:
		plt.xlabel("$d$, $\\AA$")
		plt.savefig(diffr[:-3]+'_d.png')
	else:
		plt.xlabel("$1/d$, $nm ^{-1}$")
		plt.savefig(diffr[:-3]+'_d-1.png')
	plt.close()


l = os.listdir('.')

#Are there any pks files?
try:
	pks = os.listdir('./pks')
except:
	pks = None
if pks == []:
	pks = None

#Are there any xrd files?
try:
	xrd = os.listdir('./xrd')
except:
	xrd = None

if xrd == []:
	xrd = None

#Create lists of EDs and FFTs
fft_list = []
ed_list = []

for f in l:
	if os.path.isfile(f) and ((f[-3:] == 'TXT') or (f[-3:] == 'txt') or f.endswith('.ed')):
		if 'FFT' in f:
			fft_list.append(f)
		elif 'ed' in f or 'ED' in f:
			ed_list.append(f)

for f in fft_list:
		print('FFT plot for', f)
		#to smooth graphs by savgol, please, add 'sg = True'
		#for different parameters of savgol one may use sgn parameter () for window and sgo for degree

		# defaults: xrd = None, pks = None, sg = False, sgn = 5, sgo = 3
		plot(f, pks=pks, xrd=xrd, direct=False, sg=True)
		plot(f, pks=pks, xrd=xrd, direct=True, sg=True)

for f in ed_list:
		print('ED plot for', f)
		#to smooth graphs by savgol, please, add 'sg = True'
		#for different parameters of savgol one may use sgn parameter () for window and sgo for degree
		plot(f, pks=pks, xrd=xrd, direct=False, sg=True, ed=True)
		plot(f, pks=pks, xrd=xrd, direct=True, sg=True, ed=True)
print('Done!')
