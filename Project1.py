import sys
import os
import nltk

# REQUIRES INSTALLATION OF NLTK AND OTHER PACKAGES
# OUTLINED IN: http://www.nltk.org/install.html AND
# http://www.nltk.org/data.html


# A Training Document - contains its label and feature vector
class Document(object):
	"""A Document with its vector"""

	def __init__(self, type):
		self.WORD_FREQS = {} #empty dictionary (hash table)
		self.label = type #doc label

	def addWord(self, word):
		if word in self.WORD_FREQS:
			self.WORD_FREQS[word] = self.WORD_FREQS[word]+1
		else:
			self.WORD_FREQS[word] = 1

# A Test Document - inherits from Document
class Query(Document):
	"""A Query Document"""

	def __init__(self):
		self.WORD_FREQS = {} #empty dictionary (hash table)

# Function to Toeknize and then Tag input file
def tokNTag(file):
	fid = open(file, 'r')
	doc = fid.read()
	tok = nltk.word_tokenize(doc)
	tagged = nltk.pos_tag(tok)
	fid.close()
	return tagged


# MAIN
if len(sys.argv) != 2:
	print("Usage: python Project1.py <Input Labels File>")
	sys.exit(-1)

inputLabelsFile = str(sys.argv[1])
dir = os.path.dirname(os.path.realpath(inputLabelsFile))

fid = open(inputLabelsFile, 'r')
line1 = fid.readline()
g = nltk.word_tokenize(line1)

tagged = tokNTag(dir+'/'+g[0])


print tagged[0:10]

#for line in fid:


