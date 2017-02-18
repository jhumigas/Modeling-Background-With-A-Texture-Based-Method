#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script example to process a sequence of image. It will output labelled image
in which each background pixel is labelled black.

Example:
	In a terminal, run::
		$ python recognize.py -t ../Sequence2/input/
	
	With required option -t the path to the image sequence folder. The folder should be input
"""

from pytexturebackground import TextureBackground
import numpy as np
from imutils import paths
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
    help="path to the images")
args = vars(ap.parse_args())

# Initialize the local binary patterns descriptor along with
# the data and label lists
desc = TextureBackground(P=5, R=2, K=5, Rregion=9, Tp=0.5, Tb=.8)

sequencePath = args["training"]
# Handling path of type ./input/ or ./input
folderName = sequencePath.split('/')[-1]
if len(folderName) < 1:
	folderName = sequencePath.split('/')[-2]

outputPath = args["training"].replace(folderName, 'result')
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

# Loop over the image sequence and process
for imagePath in paths.list_images(sequencePath):
	# Load the image, convert it to grayscale, and 'describe' it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	lbps = desc.computeLBPs(gray)
	imageLabelled = desc.foreground_detection(lbps, gray)
	cv2.imwrite(imagePath.replace(folderName, 'result'), imageLabelled)
	desc.background_modelling(lbps)