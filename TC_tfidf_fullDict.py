import sys
import os
import math
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet as wn

# REQUIRES INSTALLATION OF NLTK AND OTHER PACKAGES
# OUTLINED IN: http://www.nltk.org/install.html AND
# http://www.nltk.org/data.html


TOTAL_FREQS = {} #keep track of frequency in all docs for idf
IDF = {} #final idf weights
st = LancasterStemmer()
K = 1 # the K in KNN

# A Training Document - contains its label and feature vector
class Document(object):
	"""A Document with its vector"""

	def __init__(self, type):
		self.WORD_FREQS = {} #empty dictionary (hash table)
		self.label = type #doc label

	def addWord(self, word, weight):
		if word in self.WORD_FREQS:
			self.WORD_FREQS[word] += weight
		else:
			self.WORD_FREQS[word] = weight
			if word in TOTAL_FREQS:
				TOTAL_FREQS[word] += weight
			else :
				TOTAL_FREQS[word] = weight

	def findWords(self, tagged):
		for w in tagged:
			n = st.stem(w[0].lower())
			my = n, w[1]
#			self.addWord(my, 1)
			if w[1] == 'NN' or w[1] == 'NNS' or w[1] == 'NNP' or w[1] == 'NNPS':
				self.addWord(my, 1)
				for sw in wn.synsets(w[0], wn.NOUN):
					for swl in sw.lemmas:
						my = st.stem(swl.name.lower()), w[1]
						self.addWord(my, 1)
			#if w[1] == 'JJ' or w[1] == 'JJS' or w[1] == 'JJR':
			#	for sw in wn.synsets(w[0], wn.ADJ):
			#		for swl in sw.lemmas:
			#			my = swl.name.lower(), w[1]
			#			self.addWord(my, 0)
			if w[1] == 'VB' or w[1] == 'VBD' or w[1] == 'VBG' or w[1] == 'VBN' or w[1] == 'VBP' or w[1] == 'VBZ':
				self.addWord(my, 1)
				for sw in wn.synsets(w[0], wn.VERB):
					for swl in sw.lemmas:
						my = st.stem(swl.name.lower()), w[1]
						self.addWord(my, 1)


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
def dist(q, d, total_docs):
	numerator  = 0
	den1 = 0
	den2 = 0

	for w in q.WORD_FREQS:
		if w in IDF:
			den1 += (q.WORD_FREQS[w]**2)*(IDF[w]**2)
		else:
			den1 += (q.WORD_FREQS[w]**2)*(math.log(total_docs/1)**2)
		if w in d.WORD_FREQS:
			numerator += q.WORD_FREQS[w] * d.WORD_FREQS[w]*(IDF[w]**2)

	for w in d.WORD_FREQS:
		den2 += (d.WORD_FREQS[w]**2)*(IDF[w]**2)

	distance = numerator/(math.sqrt(den1) * math.sqrt(den2))
	return distance

# function to find KNN. Takes in one query,
# list of all docs, and the number k
def KNN(query, docs, k):
	KNN = []
	KND = []

	for doc in docs:
		distance = dist(query, doc, len(docs))

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

# function to populate the IDF dictionary
def make_idf(total_docs):
	for word in TOTAL_FREQS:
		total_docs_f = math.floor(total_docs)
		tfw_f = math.floor(TOTAL_FREQS[word])
		IDF[word] = math.log(total_docs_f/(1+tfw_f))


# MAIN
if len(sys.argv) != 4:
	print("Usage: python TC_tfidf.py <Training Labels File> <Test Labels File> <Output Labels>")
	print("Example: python TC_tfidf.py corpus1_train.labels corpus1_test.list myOutput.predicted")
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

make_idf(len(docs))

# Process test files
testLabelsFile = str(sys.argv[2])
dir = os.path.dirname(os.path.realpath(testLabelsFile))

fid = open(testLabelsFile, 'r')
fid2 = open(str(sys.argv[3]), 'w')

queries = []
for line in fid:
	lineTok = nltk.word_tokenize(line)
	curFile = lineTok[0]
	curQuery = Query(curFile)

	tagged = tokNTag(dir+'/'+curFile)
	curQuery.findWords(tagged)

	queries.append(curQuery)
	KND = KNN(curQuery, docs, K)
	possibilities = {}
	for d in KND:
		if d.label in possibilities:
			possibilities[d.label] += 1
		else:
			possibilities[d.label] = 1
	max = 0
	for p in possibilities:
		if possibilities[p] > max:
			max = possibilities[p]
			guess = p

	fid2.write(curFile+" "+guess+"\n")



fid.close
fid2.close()