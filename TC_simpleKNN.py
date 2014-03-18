import sys
import os
import math
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
	numerator  = 0
	den1 = 0
	den2 = 0

	for w in q.WORD_FREQS:
		den1 += (q.WORD_FREQS[w]**2)
		if w in d.WORD_FREQS:
			numerator += q.WORD_FREQS[w] * d.WORD_FREQS[w]

	for w in d.WORD_FREQS:
		den2 += (d.WORD_FREQS[w]**2)

	distance = numerator/(math.sqrt(den1) * math.sqrt(den2))
	return distance

# function to find KNN. Takes in one query,
# list of all docs, and the number k
def KNN(query, docs, k):
	KNN = []
	KND = []

	for doc in docs:
		distance = dist(query, doc)

		if len(KNN) == 0:
			KNN.append(distance)
			KND.append(doc)
			continue
		for ind in range(0, len(KNN)):
			if distance > KNN[ind]:
				KNN.insert(ind, distance)
				KND.insert(ind, doc)
				break
			elif ind == len(KNN)-1:
				KNN.append(distance)
				KND.append(doc)

	return KND[0:k]



# MAIN
if len(sys.argv) != 3:
	print("Usage: python Project1.py <Training Labels File> <Test Labels File>")
	print("Example: python Project1.py corpus1_train.labels corpus1_test.list")
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

# Process test files
testLabelsFile = str(sys.argv[2])
dir = os.path.dirname(os.path.realpath(testLabelsFile))

fid = open(testLabelsFile, 'r')
fid2 = open("Output4", 'w')

queries = []
for line in fid:
	lineTok = nltk.word_tokenize(line)
	curFile = lineTok[0]
	curQuery = Query(curFile)

	tagged = tokNTag(dir+'/'+curFile)
	curQuery.findWords(tagged)

	queries.append(curQuery)
	KND = KNN(curQuery, docs, 7)
	possibilities = {}
	for d in KND:
		print d.label
		if d.label in possibilities:
			possibilities[d.label] += 1
		else:
			possibilities[d.label] = 1
	max = 0
	for p in possibilities:
		if possibilities[p] > max:
			max = possibilities[p]
			guess = p
	print guess
	print " "

	fid2.write(curFile+" "+guess+"\n")



fid.close
fid2.close()