import sys
import os
import array
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

	def findWords(self, tagged):
		for w in tagged:
			if w[1] == 'NN' or w[1] == 'NNS' or w[1] == 'NNP' or w[1] == 'NNPS':
				self.addWord(w[0])

# A Test Document - inherits from Document
class Query(Document):
	"""A Query Document"""

	def __init__(self, fn):
		self.WORD_FREQS = {} #empty dictionary (hash table)
		self.fileName = fn

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

# Function to calculate distance between two documents
def dist(q, d):
	return distance

# function to find KNN. Takes in one query,
# list of all docs, and the number k
def KNN(query, docs, k):
	KNN = array.array('i',(-1,)*k)
	KND = []
	for i in range(0, k):
		KND.append(0)

	for doc in docs:
		distance = dist(query, doc)

		ind = KNN.index(-1) 
		if ind < k:
			KNN[ind] = distance
			KND[ind] = doc

		elif 


# MAIN
if len(sys.argv) != 3:
	print("Usage: python Project1.py <Training Labels File> <Test Labels File>")
	sys.exit(-1)

#Process training files
trainingLabelsFile = str(sys.argv[1])
dir = os.path.dirname(os.path.realpath(trainingLabelsFile))

fid = open(trainingLabelsFile, 'r')

docs = []
for line in fid:
	lineTok = nltk.word_tokenize(line)
	curFile = lineTok[0]
	curLabel = lineTok[1]
	curDoc = Document(curLabel)

	tagged = tokNTag(dir+'/'+curFile)
	curDoc.findWords(tagged)

	docs.append(curDoc)

fid.close()


for d in docs:
	print d.label

# Process test files
testLabelsFile = str(sys.argv[2])
dir = os.path.dirname(os.path.realpath(testLabelsFile))

fid = open(testLabelsFile, 'r')

queries = []
for line in fid:
	curFile = nltk.word_tokenize(line)
	curQuery = Query(curFile)

	tagged = tokNTag(dir+'/'+curFile)
	curQuery.findWords(tagged)

	queries.append(curQuery)

fid.close()