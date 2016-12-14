import urllib

# urlsFile = 'cokeURL.txt'
urlsFile = 'cansURL.txt'

# reading lines of txt file (URLs)
urls = tuple(open(urlsFile, 'r'))

# id number for writing images
numbering = 0

# stop iterations to downloads
iterations = 50

for url in urls:
	print iterations
	writePath = 'downloads/' + str(numbering) + '.jpg'
	f = open(writePath,'wb')
	img = urllib.urlopen(url).read()
	if img:
		f.write(img)
		# increment image numbering 
		numbering += 1
		# increment counts towards topper
		iterations -= 1
	
	# if k iterations
	if (iterations <= 0):
		break

f.close()