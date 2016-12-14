# object-recognizer

## Structure

  * data: data sources to build a model based upon
    * images: image data
      * cans: image data of cans
        * coke: image data of coke cans
  * model: includes trainer and constructed model
    * cascade: cascade classifier trainer and its model
  * util: generic scripts for other programs
    * image_collector: collect images from ImageNet


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

We determine to use SURF for real-time object detection with OpenCV. this video introduces very well about theory and implementation the SURF real-time object detection. .

To find a particular object, we may use Haar-Cascade Classifiers. This Self Driving RC Car by Zheng Wang explains how to implement real-time object detection with Haar-Cascade Classifiers. More details on how to train the classifier can be found a post by Thorsten Ball .

OpenCV supports Cascade Classification. Official OpenCV Document on Cascade Classification gives explanation about its theoritical background and implementation. Cascade Classifier Training process is explained here. I recommend to refer to the official document when actually implementing the Cascade Classifier with OpenCV.

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
  * OpenCV, opencv_traincascade, fucntion train prepared examples.
  1. Common arguments: specify basic information to train.
  2. Cascade parameters: specify stage type (only boosted classifier is supported today), feature type (Haar-like feature olocal binary petterns), and width and height (should exactly same values as used during training samples creation).
  3. Boosted classfier parameters: type, minimal desired hit rate, max false alarm rate, weight trim rate, max depth, anmax weak count.
  4. Haar-like feature parameters: mode (BASIC:use only upright features, or ALL:full set of upright and 45 degree rotatefeature set).
  5. Local Binary Patterns parameters: no param availabl