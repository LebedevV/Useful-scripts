import numpy as np
import hyperspy.api as hs
import sys,os
from datetime import datetime as dt


os.mkdir('tiff')

l = os.listdir()

for ll in l:
	print(ll)
	if os.path.isfile(ll):
		#try:
		if 1:
			s = hs.load(ll)
			#if s.original_metadata.DetectorMetadata.DetectorName == "HAADF":
			#	print(s.original_metadata.BinaryResult.PixelSize.height)
			print(s)
			if type(s) == type([1,2]):
				i = 0
				while i<len(s):
					h = s[i].original_metadata.BinaryResult.PixelSize.height
					w = s[i].original_metadata.BinaryResult.PixelSize.width
					f = open('./tiff/'+ll[:-4]+'_'+str(i)+'.txt','w')
					f.write(str(h)+'\n'+str(w))
					f.close()
					s[i].save('./tiff/'+ll[:-4]+'_'+str(i)+'.tif')
					i+=1
			else:
				h = s.original_metadata.BinaryResult.PixelSize.height
				w = s.original_metadata.BinaryResult.PixelSize.width
				f = open('./tiff/'+ll[:-4]+'.txt','w')
				f.write(str(h)+'\n'+str(w))
				f.close()
				s.save('./tiff/'+ll[:-4]+'.tif')
		#except:
		#	print('Not able to open a file',ll)
		
		
		
