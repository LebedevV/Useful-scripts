#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

l = os.listdir('.')
for li in l:
	print(li)
	if os.path.isdir(li):
		os.system("cd '"+li+"'&& sh ~/git/scripts_open/run.sh")
