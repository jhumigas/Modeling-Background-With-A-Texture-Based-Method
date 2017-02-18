# Modeling Image Background with a Texture-Based Method

This work is part of my assignment for Image Processing course.

A Texture-based method for modeling and the background and detecting moving objects is implemented here in python (pylbp), following Heikkila et Al. work about modeling background and detecting moving objects.
A matlab implementation is also provided but the processing runs very slow.

We used several image datasets for testing purpose.

Once you make sure all the required packages are available, you can just run the python code:

```
# in pylbp directory run recognize.py with the path to the image sequence to process
python recognize.py -t ../Sequence2/input/
```

##  Brief Presentation

TL;DR, here are the steps:

* Compute a pixel histogram
* Comparison of current pixel histogram to the k-model histograms
* Learn the background model (k-means algorithm on the model histograms and their weights)

The key idea is to model each pixel by a group of local adaptive binary pattern histograms that are calculated over a circular region around a pixel. 
The local binary pattern operator labels a given pixel by thresholding each pixel of the neighborhood with the value of the considered pixel. The result is considered as a binary number, hence the denomination of binary pattern.
The first step is Background modeling. The objective is to maintain a certain statistical representation of the scene to study. Here we use texture representation provided by the local binary operator.
The background model consists of a vector of k lbp histograms: these histograms are updated each time a region around a pixel is processed by the lbp operator. Furthermore each model is associated with a weight between 0 and 1 that denotes the importance of a model.
To learn the background model, we perform clustering on the LBP representation of the image with k-means algorithm.

Foreground detection is performed before updating the background model. A pixel histogram is simply compared to the current background histogram, and if the resulting proximity measure is higher than a predefined threshold, the pixel is labelled as belonging to the background.

## Example

Here we tested on sequence of images with normal background, we consider a scene where a car is moving in a street.
We used the following values for the parameters : P=6, R=2, K=3, Rregion=9, Tp=0.55, Tb=0.7

Right : Original images  | Left : Processed for foreground detection


![alt Original](https://raw.githubusercontent.com/jhumigas/Modeling-Background-With-A-Texture-Based-Method/master/Sequence1/animated/input.gif)
![alt Original](https://raw.githubusercontent.com/jhumigas/Modeling-Background-With-A-Texture-Based-Method/master/Sequence1/animated/plbp_R9.gif)


The car indeed belong to the foreground detected, we can see it *slipping* through the blacked areas, that represent the foreground.



## Requirements

Notable required packages : 

* OpenCV
* Scikit-image
* imutils
* numpy

Python required modules can be found in pylbp/req.txt. 
Install them by running : 

```
cd pylbp
pip install -r req.txt
```

## Image Datasets

*Image Datasets will be provided soon for testing purposes*

* Sequence 1 taken form [PETS](http://ftp.pets.rdg.ac.uk/pub/PETS2001/) database
* Sequence 2, 3 taken from [ChangeDetection.Net](http://wordpress-jodoin.dmi.usherb.ca/static/dataset/baseline/), a University of Sherbrooke dataset

## Sources

* Heikkila, M., & Pietikainen, M. (2006). [A texture-based method for modeling the background and detecting moving objects](http://aiweb.techfak.uni-bielefeld.de/files/BackgroundSubstraction.pdf). IEEE transactions on pattern analysis and machine intelligence, 28(4), 657-662.
* [Local Binary Patterns with Python & OpenCV](http://www.pyimagesearch.com/2015/12/07/local-binary-patterns-with-python-opencv/)