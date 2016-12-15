# object-recognizer

## Structure

  * data: data sources to build a model based upon
    * images: image data
      * cans: image data of cans
        * coke: image data of coke cans
  * model: includes trainer and constructed model
    * cascade: cascade classifier trainer and its model
      * cascade_generator: generate cascade
      * cascade_testor: test generated cascade
  * util: generic scripts for other programs
    * collector: collect images from ImageNet
    * cascade_sampling: obsolute folders/files for initial cascade training attempt


## Extraction and Matching

The most recent proejct I am working on is the Robot Arm object detection with images. How can we point a particular object from an image or a video?

First of all, we need to define the spec of inputs:

  * An image is a 2d matrix which each elements has its pixel values.
  * A video is a stack of 2d matrix which ordered in the frame rate. 


Lets think about processing an image for a object detection. Our goal is to detect a can of Coke from the iamge.
What is the unique attribute that a can of Coke have? May be:

  * Shape as a can
  * Shape of Logo
  * Color ratio (red / white)

We call these attributes as featuers. We can do pattern match with these attributes. Before moving on, I recommend you to go over Outline of object recognition (Wikipedia) .

We determine to use SURF for real-time object detection with OpenCV. [this video](https://www.youtube.com/watch?v=ZXn69V-1kEM) introduces very well about theory and implementation the SURF real-time object detection. .

To find a particular object, we may use Haar-Cascade Classifiers. [This Self Driving RC Car by Zheng Wang](https://zhengludwig.wordpress.com/projects/self-driving-rc-car/) explains how to implement real-time object detection with Haar-Cascade Classifiers. More details on how to train the classifier can be found in [a post by Thorsten Ball](http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html).

OpenCV supports Cascade Classification. [Official OpenCV Document](http://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html) on Cascade Classification gives explanation about its theoritical background and implementation. Cascade Classifier Training process is explained [here](http://docs.opencv.org/2.4/doc/user_guide/ug_traincascade.html). I recommend to refer to the official document when actually implementing the Cascade Classifier with OpenCV.

Quick note on Cascade Classifier with OpenCV:

  * To train, we separate training data to positive examples and negative ones.
  * Positive exampels should include the target object.
  * Depending on the generalization level of the object, we need more positive examples to train.
  ie. to recognize faces, we need hundreds or even thousands of images of faces with variety features.
  * Positive examples can be generated from one or a few images with OpenCV build-in function, opencv_createsamples.
  * Negative examples must not include the target object.
  * Negative examples should be made manually.
  * Negative examples sometimes called background samples or background sample images.
  * Opencv provides many command line arguments to prepare examples for classification.
  * To capture images from a video, OpenCV has VideoCapture function.
  * OpenCV, opencv_traincascade, fucntion [train prepared examples](http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set).
  1. Common arguments: specify basic information to train.
  2. Cascade parameters: specify stage type (only boosted classifier is supported today), feature type (Haar-like feature olocal binary petterns), and width and height (should exactly same values as used during training samples creation).
  3. Boosted classfier parameters: type, minimal desired hit rate, max false alarm rate, weight trim rate, max depth, anmax weak count.
  4. Haar-like feature parameters: mode (BASIC:use only upright features, or ALL:full set of upright and 45 degree rotatefeature set).
  5. Local Binary Patterns parameters: no param available

We sampled 80 images of coffee cup and 1000 negatives for testing out how the cascade works.
To be accurate, 1000 positives and 5000 negatives are suggested in some articles.


## Cascade Classifier Testing Process

1. Get negative sample images and put it in './negatives' (NOT containing object that you want to recognize)
2. Get a source positive sample image and put it in './positive_source' (containing object that you want to recognize)
3. Generate .txt for negative samples [find ./negatives -iname "*.jpg" > negatives.txt]
4. Generate complete positive images to train on [mkdir positives && cd positives && opencv_createsamples -img ../positive_source/'image-name'.jpg -bg ../negatives.txt -info annotations.lst -maxxangle 0.5 -maxyangle 0.5 -maxzangle 2.0 -w 80 -h 40]
5. Convert annotations.lst to vector file [cd .. && touch coffeeCup.vec && opencv_createsamples -info positives/annotations.lst -vec coffeeCup.vec -num 900 -w 80 -h 40]
6. Conduct cascade training [mkdir classifier && opencv_traincascade -data classifier -vec coffeeCup.vec -bg negatives.txt -numStages 1 -minHitRate 0.8 -maxFalseAlarmRate 0.5 -numPos 10 -numNeg 5 -w 80 -h 40 -mode ALL -precalcValBufSize 1024 -precalcIdxBufSize 1024]

## References:

[Tutorial: OpenCV harrtraining(Rapid Object Detection with a Cascade of Boosted Classifiers Based on Haar-like Features.)](note.sonots.com/SciSoftware/haartraining.html)

[Train Your Own OpenCV Haar Classifier](http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html) : with js script to test cascade file for static files with box drawing around target object.

[How to Install OpenCV on Ubuntu](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)

[Creating a Cascade of Haar-Like Classifiers: Step by Step](https://www.cs.auckland.ac.nz/~m.rezaei/Tutorials/Creating_a_Cascade_of_Haar-Like_Classifiers_Step_by_Step.pdf)

[Haar Cascade Training Tutorial](http://www.trevorsherrard.com/Haar_training.html) : with python script to test cascade file using webcam in real-time with box drawing around target object.

[Cascade Classifier Training](http://docs.opencv.org/2.4/doc/user_guide/ug_traincascade.html#positive-samples)

[Using AWS to Train Cascade Classifier](https://github.com/kburnham/DAND-Right-Whale-Identification/blob/master/Using%20AWS%20to%20Train%20a%20Cascade%20Classifier.md)

[Creating your own Haar Cascade OpenCV Python Tutorial](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/)