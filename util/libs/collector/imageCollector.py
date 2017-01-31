# open arbitrary resources (https://docs.python.org/2/library/urllib.html)
import socket
import urllib2

# urlsFile = 'cokeURL.txt'
urlsFile = 'cansURL.txt'
# reading lines of txt file (URLs)
urls = open(urlsFile, 'r')
# id number for writing images
numbering = 0
# stop iterations to downloads
iterations = 300

# url_lines = urls.readlines()
# iterate the txt file contains urls line by line
for url in urls:
	print(url)
	# notify which iteration you are in
	print(iterations)
	# make a string for a path name to write the file in
	writePath = 'downloads/' + str(numbering) + '.jpg'
	# open a file to write in with the writePath name defined
	f = open(writePath,'wb')
	try:
		# retrieve resource with the url defined
		response = urllib2.urlopen(url, timeout=0.1)
	except urllib2.URLError as err:
		print('URL error happend')
		pass
	except IOError:
		print('IO Error happend')
		pass
	except socket.timeout:
		pass
	else:
		# print response
		print response
		# if image is loaded successfully
		if response:
			# read the image
			try:
				img = response.read()
			except socket.timeout:
				pass
			else:
				# write actually the fetched image in the file location
				f.write(img)
				# increment image numbering
				numbering += 1
				# increment counts towards topper
				iterations -= 1
		
		# if k images downloaded, stop iteration
	if (iterations <= 0):
		break

# close the file for safety
f.close()