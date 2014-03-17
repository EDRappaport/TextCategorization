import sys
import os
import nltk

# REQUIRES INSTALLATION OF NLTK AND OTHER PACKAGES
# OUTLINED IN: http://www.nltk.org/install.html AND
# http://www.nltk.org/data.html

if len(sys.argv) != 2:
	print("Usage: python Project1.py <Input Labels File>")
	sys.exit(-1)

inputLabelsFile = str(sys.argv[1])
dir = os.path.dirname(os.path.realpath(inputLabelsFile))
fid = open(inputLabelsFile, 'r')
line1 = fid.readline()
g = nltk.word_tokenize(line1)
fid2 = open(dir+'/'+g[0], 'r')
doc = fid2.read()

g2 = nltk.word_tokenize(doc)
g3 = nltk.pos_tag(g2)


print g3

#for line in fid:


