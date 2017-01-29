# object-recognizer

## Structure

  * data: data sources to build a model based upon
    * images: image data
      * negative: collections of background images in different size
      * positive: collections of positive images for different objects
  * model: includes trainer and constructed model
    * cascade: cascade classifier trainer and its model
      * cascade_generator: generate cascade
        * bin: buliding a training
        * positive_images: should contain processed positive images
        * tools: include a script to merge vector files
        * negative_images: should contain processed negative images
      * cascade_storage: store cascades generated by cascade_generater
      * cascade_testor: test stored cascades
  * util: generic scripts for other programs
    * bin: conduct all necessary precondition tasks for building training
    * libs: collection of program to conduct individual precondition tasks


## Cascade Classifier Training Process (Commands and Arguments)

1. Get negative sample images and put it in './negative_images' (NOT containing object that you want to recognize)

2. Get source positive sample images and put it in './positive_images' (containing object that you want to recognize)

3. To generate vec files from the samples, run 

      `$ python bin/build_training.py [sample_width] [sample_height] [z_angle_rotation] [num_of_saples_to_generate] [to_show_sample]`

4. Conduct cascade training

      `$ opencv_traincascade -data classifier -vec samples.vec -bg negatives.txt -numStages 15 -numPos 2900 -numNeg 1450 -w 20 -h 40 -mode ALL -precalcValBufSize 1024 -precalcIdxBufSize 1024`


## How to train better cascade

  * Preconditioning source images (Cropping and grayscaling):
    * If you want to detect a object with its outline (a shape of cans etc..), you should crop positive images with some extra space around the outline of the object.
    * The size of positive images should be as close as possible but it is not needed to be exactly same.
    * Do not forget grayscale every negative and positive images before proceeding.
    * To generalize, the variety of positive images is important. If you want to find a cans from different angles, you should feed in cans images took from differnt angles.
  * Creating samples:
    * Make sure positive samples generated by running opencv_createsamples is preferable from the perspective of processing machine. It is highly recommended to understand how cascade trainer learns from images by reading technical documents.
    * If you want to detect a target object in bright backgroudn, you may need to configure the -inv (invert the color of sample images) or -randinv (invert the color of sample images in random).
  * Training a cascade:
    * The more samples to feed in the training process brings better result.
    * The good ratio of the positive and negative samples is 2:1.
    * The more buffer size given, the faster the training process becomes.
    * The good acceptance ratio is nearly 10e-5. Beyond that, it's over training and cascade can become too sensitve to particular features of positive samples.


## Test Cascade

      `$ python testCascadeRealTime.py {cascade object width} {cascade object height} {scale factor} {minimum neighbors} {webcam frame width} {webcam frame height}`

For example,
      
      `$ python testCascadeRealTime.py 20 50 1.1 22 800 600`


## Running background process on server

  * access server: `$ ssh userid@remoteserver`
  * run script with nohup (dont forget & at the end): `$ nohup opencv_traincascade.... &`
  * to find the process run to get process ID : `ps auxwww|grep -i 'opencv_traincascade'`
  * this works too: `ps -eaf | grep opencv_traincascade`
  * to kill the process of the process ID : `kill -9 IDnumber`


## Issues and fixes log

  * [Follow this link to install and debug the opwncv on raspberrypi]](http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/)
  * To link, you should be in virtual env. If you wronglly linked outside of virtual env, you should be able to
    unlink and activate to get in the virtual env and relink again. Make sure reboot the pi after this. Then test it.
  * 1. unlink in the virtual env | .
    `(cv)pi$ cd ~/.virtualenvs/cv/lib/python2.7/site-packages/`
    `(cv)pi$ unlink cv2.so`
    2. link again in virtual environment. 
    `(cv)pi$ ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so`
    3. deactivate 
    `(cv)pi$ deactivate`
    4. sudo reboot 
    `pi$ sudo reboot`
    5. reacess 
    `yourmachine$ ssh pi@remoteaddress`
    6. go to virtual end (workon cv)
    `pi$ workon cv`
    7. open python interpreter and test whetehr opencv works
    `(cv)pi$ python`
    `>>> import cv2`
  * what caused that?: 
    * carefully observe how we installed the open cv (http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)
  * $ scp -r path/to/send/from to@remoteaddress:~/path/to/receive
  * Installing the smbus tools in the virtualenvironment.
    * At this point, the most promising way to do fix this is to create new virtual environment wiht global system config.
    * [Use this guide](http://stackoverflow.com/questions/12079607/make-virtualenv-inherit-specific-packages-from-your-global-site-packages)
    * [This too](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
  * On installing opencv on the digital ocean/school server
    * first of all, you need to access through school VPN if you are not on campus
    * throughout this, we are using python2.7. opencv version may different in the environemnt.
    * in my local environemnt, 2.4.10. On server (digital ocean, school), 3.1.0. On pi, 3.0.0. 
    * following [this guide to install](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)
    * completed the instllation process successfully.
  * On running the training in the school server.
    * should rebulid better precondition for the next training.
    * the assumption to make better cascade training is
      * cropping better ( make sure include the outline of the object )
      * put more different positive images
      * train more stages
  * On uninstalling / reinstalling the opencv on pi
    * I started following [this link](http://stackoverflow.com/questions/24598160/unistall-opencv-2-4-9-and-install-3-0-0)
    * Since I built it from source, I would use `ls
    * sudo make uninstall` in the path that I did `sudo make install`
    * the reason I did not install well enough was that `sudo nano /etc/apt/sources.list` and commnet out the last line as suggested to
      run the command `sudo apt-get update` etc.. [This is a reference](http://raspberrypi.stackexchange.com/questions/10600/apt-get-update-gives-me-errors-with-mirrordirector-raspbian-org)
    * I run into a trouble that I could not proceed the apt-get command and any other required command on pi.
      I decided to reflesh evrything from scratch to reinstall the environment.
    * Basiaclly what you need to get the pi back to factory version, you push shift when you are rebooting.
    * [This is a reference](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=104790)
    * I got data corruption while reinstalling the OS. I decided to clean the SD card and remount the Raspbian OS again.
    * It might be good idea to have an extra sd when any software related isseus happened.

## References:

[How to Install OpenCV on Ubuntu](http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/) - How to instlal OpenCV on your machine.

[Cascade Classifier Training](http://docs.opencv.org/2.4/doc/user_guide/ug_traincascade.html#positive-samples) - Official document of cascade training by OpenCV 2.4

[Official Tutorial for Cascade Training](http://docs.opencv.org/3.2.0/dc/d88/tutorial_traincascade.html) - Official document of cascade training by OpenCV 3.0+

[Tutorial: OpenCV haartraining (Rapid Object Detection With A Cascade of Boosted Classifiers Based on Haar-like Features)](http://note.sonots.com/SciSoftware/haartraining.html) - Detailed cascade training process including optimal training configuration insights.

[Creating your own Haar Cascade OpenCV Python Tutorial](https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/) - Step by step guide to create first cascade training on Python.

[Train your own OpenCV Haar classifier](https://github.com/mrnugget/opencv-haar-classifier-training) - Another well written step by step guide to train cascade. Original source of the vecter merge code.

[Strategy to Make Cascade Training Fast](http://answers.opencv.org/question/7141/about-traincascade-paremeters-samples-and-other/) - Explains insights to configure the parameters better to get more accurate result of traininig.

[How to run a Python script in the background even after I logout SSH?](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=how%20to%20keep%20running%20python%20script%20on%20server%20withtou%20ssh%20connection)

[SSH Essentials: Working with SSH Servers, Clients, and Keys](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)

[Pi Camera Basic Recipes](http://picamera.readthedocs.io/en/release-1.10/recipes1.html)

[Pi Camera Advanced Recipes](http://picamera.readthedocs.io/en/release-1.11/recipes2.html)

[Install guide: Raspberry Pi 3 + Raspbian Jessie + OpenCV 3](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)

[Common errors using Pi Camera module](http://www.pyimagesearch.com/2016/08/29/common-errors-using-the-raspberry-pi-camera-module/)