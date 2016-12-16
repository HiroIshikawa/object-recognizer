
import cv2
# import urllib.request
import urllib2
import urllib
import numpy as np
import os

def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'   
    # neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    neg_image_urls = urllib2.urlopen(neg_images_link).read().decode()
    
    if not os.path.exists('negatives'):
        os.makedirs('negatives')

    numbering = 1
    # iterations = 2000
    
    for url in neg_image_urls.split('\n'):
        try:
            print(url)
            urllib.urlretrieve(url, "negatives/"+str(numbering)+".jpg")
            #urllib.urlretrieve(url, "negatives/"+str(numbering)+".jpg", timeout=0.1)
            img = cv2.imread("negatives/"+str(numbering)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("negatives/"+str(numbering)+".jpg",resized_image)
            numbering += 1
            
        except Exception as e:
            print(str(e)) 

store_raw_images()