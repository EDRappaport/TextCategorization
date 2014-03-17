import sys
import os
import nltk
#from nltk.tokenize import TreebankWordTokenizer

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

	def findWords(self, tagged):
		for w in tagged:
			if w[1] == 'NN' or w[1] == 'NNS' or w[1] == 'NNP' or w[1] == 'NNPS':
				self.addWord(w[0])

# A Test Document - inherits from Document
class Query(Document):
	"""A Query Document"""

	def __init__(self):
		self.WORD_FREQS = {} #empty dictionary (hash table)

# Function to Toeknize and then Tag input file
def tokNTag(file):
	fid = open(file, 'r')
	doc = fid.read()
	sentTok = nltk.sent_tokenize(doc)
	tagged = []
	for sent in sentTok:
		wordTok = nltk.word_tokenize(sent)
		t = nltk.pos_tag(wordTok)
		tagged.extend(t)
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
doc1 = Document(g[1])

tagged = tokNTag(dir+'/'+g[0])
doc1.findWords(tagged)

print doc1.WORD_FREQS
newFile = open('Output', 'w')
newFile.write(str(tagged))

#for line in fid:


