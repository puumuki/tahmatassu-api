#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from distutils.core import setup
import glob

setup(
	name='tahmatassu-api',
	version='1.0',
	description='Tahmatassujen Resepetikirjan Application Interface',
	author='Teemu Puukko',
	author_email='teemuki@gmail.com',
	packages=['tahmatassu'],
	license='LICENSE.txt',
	long_description=open('README.md').read(),
	keywords=['webapp','recipe'],
	scripts=glob.glob('bin/*.py')
)
