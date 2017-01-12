import sys, os, glob
from sys import argv

num_samples = argv[1]

# for (i,image_file) in enumerate(glob.iglob('./source/*.jpg')):
        # process(image_file, i)

# compute number of files
num_pos_imgs = len(glob.glob('../positive_images/*.jpg'))
print num_pos_imgs

# number of vector per training
num_per_create = int(num_samples) / num_pos_imgs
print num_per_create

# choose negative image name
# my $vec = $outputdir . substr($img, $imgdirlen) . ".vec" ;

# -bgcolor 0 -bgthresh 0

for (i,image_file) in enumerate(glob.iglob('../positive_images/*.jpg')):
	command = "opencv_createsamples -num " + str(num_per_create) + " -img "+image_file+" -bg ../negatives.txt -vec ../samples/"+str(i)+".vec -maxxangle 0.5 -maxyangle 0.5 -maxzangle 2.0 -w 20 -h 20"
	print command
	os.system(command)