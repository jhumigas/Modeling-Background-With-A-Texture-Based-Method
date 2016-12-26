# Modelling Image Background with a texture-Based Method

This work is part of my assignment for Image Processing course.

A Texture-based method for modelling and the background and detecting moving objects is implemented here in python (pylbp), following Heikkila et Al. work about modelling background and detecting moving objects[1].
A matlab implementation is also provided but the processing runs very slow.

We used several image datasets for testing purpose.

Once you make sure all the required packages are available, you can just run the python code:

```
# in pylbp directory run recognize.py with the path to the image sequence
python recognize.py -t ../Sequence2/input/
```

##  Brief Presentation

The key idea is to model each pixel by a group of local adaptive binary pattern histograms that are calculated over a circular region around a pixel. 
The local binary pattern operator labels a given pixel by thresholding each pixel of the neighborhood with the value of the considered pixel. The result is consider as a binary number, hence the denomination of binary pattern.
The first step is Background Modelling. The objective is to maintain a certain representation of the scene to study. Here we use texture representation provided by the local binary operator.
The background model consists of a vector of k lbp histograms: these histograms are updated each time a region around a pixel is processed by the lbp operator. Furthermore each model is associated with a weight between 0 and 1 that denotes the importance of a model.
To learn the background model, k-means algorithm is used in the following step:

* Compute a pixel histogram
* Comparison of current pixel histogram to the k-model histograms
* Learn the background model (k-means algorithms on the model histograms and the weights)

Foreground detection is performed before updating the background model. A pixel histogram is simply compared to the current background histogram, and if the resulting proximity measure is higher than a predefined threshold, the pixel is labelled as belonging to the background.

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

## Image Dataset

* Sequence 1 taken form [PETS](http://ftp.pets.rdg.ac.uk/pub/PETS2001/) database
* Sequence 2, 3 taken from [ChangeDetection.Net](http://wordpress-jodoin.dmi.usherb.ca/static/dataset/baseline/), a University of Sherbrooke dataset

## Sources

Heikkila, M., & Pietikainen, M. (2006). [A texture-based method for modeling the background and detecting moving objects](http://aiweb.techfak.uni-bielefeld.de/files/BackgroundSubstraction.pdf). IEEE transactions on pattern analysis and machine intelligence, 28(4), 657-662.
