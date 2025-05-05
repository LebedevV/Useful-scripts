#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os

ll = os.listdir('.')
l = []
for i in ll:
	if i.endswith('.tif'):
		l.append(i)
		
for i in l:
	print(i)
	im = cv2.imread('./'+i)
	cv2.imwrite(i[:-3]+'png',im)
