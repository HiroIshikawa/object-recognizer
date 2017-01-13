# open arbitrary resources (https://docs.python.org/2/library/urllib.html)
import urllib2
import cv2

# urlsFile = 'cokeURL.txt'
# urlsFile = 'cansURL.txt'
# reading lines of txt file (URLs)
# urls = tuple(open(urlsFile, 'r'))

# id number for writing images
numbering = 0
# stop iterations to downloads
iterations = 100

neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'   
# neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
urls = urllib2.urlopen(neg_images_link).read().decode()
    
# iterate the txt file contains urls line by line
for url in urls.split('\n'):
	# notify which iteration you are in
	print iterations
	# make a string for a path name to write the file in
	# writePath = 'negatives/' + str(numbering) + '.jpg'
	# open a file to write in with the writePath name defined
	# f = open(writePath,'wb')
	try:
		# retrieve resource with the url defined
		response = urllib2.urlopen(url, timeout=1)
		urllib.urlretrieve(url, "negatives/"+str(numbering)+".jpg")
	except urllib2.URLError as err:
		print 'URL error happend'
		pass
	except IOError:
		pass
	else:
		# print response
		print response
		# if image is loaded successfully
		if response:
			# read the image
			img = response.read()
			# write actually the fetched image in the file location
			f.write(img)
			urllib2.urlretrieve(url, "neg/"+str(pic_num)+".jpg")
			# read downloaded negative samples
			img = cv2.imread("negatives/"+str(numbering)+".jpg",cv2.IMREAD_GRAYSCALE)
			# get the image shpae
			# height, width = img.shape
			# if the size is mode than 0
			if img is not None:
	            # should be larger than samples / pos pic (so we can place our image on it)
				resized_image = cv2.resize(img, (100, 100))
	            # write resized negative images
				cv2.imwrite("negatives/"+str(numbering)+".jpg",resized_image)
	            # increment image numbering
				numbering += 1
				# increment counts towards topper
				iterations -= 1
		
		# if k images downloaded, stop iteration
	if (iterations <= 0):
		break

# close the file for safety
f.close()