import math
import sys
import os
import nltk

# MAIN
if len(sys.argv) != 5:
	print("Usage: python SplitTrainingSet.py <Training Labels File> <Output Training File> <Output Test File> <percentage>")
	sys.exit(-1)

trainingLabelsFile = str(sys.argv[1])
dir = os.path.dirname(os.path.realpath(trainingLabelsFile))
percentage = float(sys.argv[4])

fid = open(trainingLabelsFile, 'r')

typeCounts = {}
# Get numbers of each type
for line in fid:
	lineTok = nltk.word_tokenize(line)
	curFile = lineTok[0]
	curLabel = lineTok[1]

	if curLabel in typeCounts:
		typeCounts[curLabel]+= 1
	else:
		typeCounts[curLabel] = 1
fid.close()

print typeCounts

# typecounts will now contain number of items to keep in training
for t in typeCounts:
	typeCounts[t] = math.floor(typeCounts[t]*percentage)

fid_i = open(trainingLabelsFile, 'r')
fid_training = open(str(sys.argv[2]), 'w')
fid_test = open(str(sys.argv[3]), 'w')
fid_testAnswers = open(str(sys.argv[3])+"Answers", 'w')

for line in fid_i:
	lineTok = nltk.word_tokenize(line)
	curFile = lineTok[0]
	curLabel = lineTok[1]

	if typeCounts[curLabel] > 0:
		fid_training.write(line)
		typeCounts[curLabel] -= 1
	else:
		fid_test.write(curFile+"\n")
		fid_testAnswers.write(line)

fid_i.close()
fid_training.close()
fid_test.close()

