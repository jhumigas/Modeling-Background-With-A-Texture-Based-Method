from pytexturebackground import TextureBackground
import numpy as np
from imutils import paths
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
    help="path to the images")
args = vars(ap.parse_args())

# initialize the local binary patterns descriptor along with
# the data and label lists
desc = TextureBackground(6, 2)

# loop over the training images
for imagePath in paths.list_images(args["training"]):
	# load the image, convert it to grayscale, and describe it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	lbps = desc.computeLBPs(gray)
	imageLabelled = desc.foreground_detection(lbps, gray)
	cv2.imwrite(imagePath.replace('input', 'result').replace('jpg', 'png'), imageLabelled)
	desc.background_modelling(lbps)