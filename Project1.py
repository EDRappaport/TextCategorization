import sys
import os
import nltk

if len(sys.argv) != 2:
	print("Usage: python Project1.py <Input Labels File>")
	sys.exit(-1)

inputLabelsFile = str(sys.argv[1])
dir = os.path.dirname(os.path.realpath(inputLabelsFile))

