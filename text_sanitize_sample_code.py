import nltk
from nltk.collocations import *
from nltk import FreqDist

fp = open( 'stein_texts_no_format.txt' )

txt = fp.read()

sentences = nltk.sent_tokenize(txt)

newSentences = []

#get rid of indentation
for i in range( len( sentences ) ):
	newSentences.append( sentences[i].replace( "\n", " ") )

#get rid of double spaces
for i in range( len( newSentences ) ):
	newSentences[i] = newSentences[i].replace("  ", " ")

#saw this at least once
for i in range( len ( newSentences ) ):
	newSentences[i] = newSentences[i].replace("- ", "-")

#if sentences as greater than 135 characters (assumed no twitter handle is less than 5 characters, probably incorrect, just guessing), get rid of them
filteredSentences = []

for i in range( len( newSentences ) ):
	if len(newSentences[i]) < 135:
		filteredSentences.append( newSentences[i] )

#store as one big block, read nltk.sent_tokenize(fromFile) when loading info into program
# fp = open( 'stein_sentences.txt', 'a')
# 
# for i in range( len( filteredSentences ) ):
# 	fp.write( filteredSentences[i] + '\n')
# 
# fp.close()

#test reading entire database of stein sentences into a new list

fp = open( 'stein_sentences.txt' )
db = fp.readlines()
fp.close()

for i in range( len( db ) ):
	db[i] = db[i].replace("\n","")

for i in range( len( db ) ):
	if len(db) == 

sentences = nltk.sent_tokenize(db)
print sentences
