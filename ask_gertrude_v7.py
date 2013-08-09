#TO DO:
#add cron stuff
#clean this up, this is super messy code

SHORTLOG = 'ask_gertrude_shortlog.txt'
LOGFILE = 'ask_gertrude_log.txt'
RESEARCHLOG = 'ask_gertrude_research.txt'
STEINSENTENCES = 'stein_sentences.txt'

from config import *
from datetime import datetime
import sys
import twitter, os, random

api = twitter.Api(consumer_key = CKEY,
                  consumer_secret = CSECRET,
                  access_token_key = ATKEY,
                  access_token_secret = ATSECRET)

# grab all ids the bot has replied to to avoid responding to the same status repeatedly (spam prevention)
if os.path.exists(SHORTLOG):
    fp = open(SHORTLOG)
    alreadyMessaged = fp.readlines()
    for i in range( len( alreadyMessaged ) ):
	alreadyMessaged[i] = int(alreadyMessaged[i])				#ids are later stored as strings, so int casting here
	fp.close()

if os.path.exists(RESEARCHLOG):
    fp = open(RESEARCHLOG)
    alreadyResearched = fp.readlines()
    for i in range( len( alreadyResearched ) ):
	alreadyResearched[i] = int(alreadyResearched[i])				#ids are stored as strings, so int casting here
	fp.close()

# check to see if there are any replies, respond if those replies also contain a question mark
# then build a list of Status objects that meet that criteria
users = []
filteredUIds = []
filteredUsers = []
replies = api.GetReplies()
for i in range(len(replies)):

	if replies[i].text.find('?') != -1:
		users.append( replies[i] )

#in case there are no new messages, check to see if anyone has used the term Gertrude Stein lately
research = api.GetSearch('"Gertrude Stein"')

#temporarily create two sets of Ids, return the difference between them (for questions)
a = []
b = []
for i in range( len( alreadyMessaged)):
	a.append(alreadyMessaged[i])

for i in range( len( users )):
	b.append(users[i].id)

#filter out duplicates
filteredUIds = list( set(b) - set(a) )

#build new list of status objects from filtered list
for i in range( len( filteredUIds ) ):
	filteredUsers.append( api.GetStatus(filteredUIds[i]) )

#check to see if anyone from the research field has been contacted
c = []
d = []
filteredResearch = []
filteredNewContacts = []
for i in range( len( alreadyResearched )):
	c.append( alreadyResearched[i])

for i in range( len( research ) ):
	d. append( research[i].id)

#filter out duplicates here
filteredResearch = list( set( d ) - set( c ) )

for i in range( len( filteredResearch ) ):
	filteredNewContacts.append( api.GetStatus(filteredResearch[i]))

newFilter = []

#check to make sure @ask_gertrude (and other frequently contacted users) is not in new contacts list
for i in range( len( filteredNewContacts ) ):
	if filteredNewContacts[i].user.screen_name != 'ask_gertrude' or 'Gertrude_Stein_':	#Gertrude_Stein_ is not getting filtered out
		newFilter.append(filteredNewContacts[i])

#load sentences into db
fp = open( STEINSENTENCES )
db = fp.readlines()
fp.close()

#get rid of indentation from db
for i in range( len( db ) ):
	db[i] = db[i].replace("\n","")

# this is where the response sentences will go
sentences = []

if len(filteredUsers) == 0:
	#instead, should search for statuses containing the term "Gertrude Stein" and ask if they have any questions
	print "Nothing to reply to today, checking to see if anyone has a question!"
	if newFilter == 0:
		print "No new tweets matching my criteria. So lonely. Calling it a day."
		sys.exit()
	newreplyTo = random.randint( 0, len(newFilter) - 1)
	print "Found " + str(len(newFilter)) + " new users, randomly chosing number " + str(newreplyTo) + " to ask!"
	newContacts = newFilter[newreplyTo].user.screen_name
	print "Responding to @" + str(newContacts) + "!"
	newreplyId = newFilter[newreplyTo].id
	salutation = 'Dear @'
	formatting = ', '
	question = ' Do you need any #advice? '
	numCharacters = len( newContacts ) + len( salutation ) + len( question ) + len( formatting )
	for i in range( len( db ) ):
		if len( db[i] ) < numCharacters:
			sentences.append( db[ i ] )
	print "Number of possible sentences " + str( len( sentences ) )
	choice = random.randint( 0, len( sentences ) - 1 )
	print "Choosing sentence at position " + str(choice)
	print sentences[choice]	
	api.PostUpdate( salutation + newContacts + formatting + sentences[ choice ] + question, newreplyId )

elif len(filteredUsers) == 1:
	#then reply to that one
	print len(filteredUsers)	#just to double check, delete prior to finalization
	print "Found only one question, responding to it!"
	selected = filteredUsers[0].user.screen_name
	replyId = filteredUsers[0].id
	salutation = 'Dear @'
	formatting = ', '
	tag = ' #advice'
	numChar = len( selected ) + len( salutation ) + len( formatting ) + len( tag )
	print "Number of characters left = " + str(numChar)	#use this to determine which line from steinDB to select from
	for i in range( len( db ) ):
		if len(db[i]) < numChar:
			sentences.append( db[i] )
	print "Number of possible sentences "  + str(len( sentences))
	choice = random.randint( 0, len( sentences ) - 1 )
	print "Choosing sentence at position " + str(choice)
	api.PostUpdate( salutation + selected + formatting + sentences[choice] + tag, replyId )
	print salutation + selected + formatting + sentences[choice] + ' replyId is ' + str(replyId)

elif len(filteredUsers) >= 2:
	#if two or more responses, randomly choose one to respond to
	print 'number of total unanswered questions = ' + str( len( filteredUsers ) )
	replyTo = random.randint( 0, len(filteredUsers) - 1)
	print "Found " + str(len(filteredUsers)) + ", randomly chosing number " + str(replyTo) + " to respond to!"
	selected = filteredUsers[replyTo].user.screen_name
	replyId = filteredUsers[replyTo].id
	salutation = 'Dear @'
	formatting = ', '
	tag = ' #advice'
	numChar = len( selected ) + len( salutation ) + len( formatting ) + len( tag )
	for i in range( len( db ) ):
		if len(db[i]) < numChar:
			sentences.append( db[i] )
	print "Number of possible sentences "  + str(len( sentences ) )
	choice = random.randint( 0, len( sentences ) - 1 )	
	api.PostUpdate( salutation + selected + formatting + sentences[choice] + tag, replyId )
	print salutation + selected + formatting + sentences[choice] + ' replyId is ' + str(replyId)

#this simply keeps the status Ids to avoid duplicate responses
if len(filteredUsers) >= 1:
	fp = open(SHORTLOG, 'a')
	fp.write( '\n' + str(replyId) )
	fp.close()
	
	#this is used for record keeping and debugging
	fp = open(LOGFILE, 'a')
	today = datetime.now()
	fp.write( '\n'+ 'replied to ' + str(selected) + ', status Id = ' + str(replyId) + ' (' + str(today.month) + '/' + str(today.day) + '/' +str(today.year) + ')' )
	fp.close()
	print 'Updated the records, done for now!'

else:
	#this tracks who has been contacted following a search (another spam prevention measure)
	fp = open(RESEARCHLOG, 'a')
	fp.write( '\n' + str(newreplyId) )
	fp.close()
	print 'Done for now!'

sys.exit()

#TO DO:
#cron stuff