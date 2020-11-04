# Description : Entry point for Simple Question Answer Chatbot
# Program Argument :
#		datasetName = "Name of dataset text file" eg. "Beyonce.txt"
# Usage :
#		$ python3 P2.py dataset/IPod

from DocumentRetrievalModel import DocumentRetrievalModel as DRM

from ProcessedQuestion import ProcessedQuestion as PQ
from DocumentRetrievalModelWM import DocumentRetrievalModelWM as DRMWM
from ProcessedQuestionWM import ProcessedQuestionWM as PQWM
import argparse
import re
import sys
from gensim.models import Word2Vec
import nltk
nltk.download('averaged_perceptron_tagger')

def main(datasetName, use_word_embeddings):
	print("Bot> Hey there, my name is WikiV2! Please hold while I load up my dependencies :)")
	
	# Loading Dataset
	try:
		datasetFile = open(datasetName,"r", encoding="utf-8")
	except FileNotFoundError:
		print("Bot> Oops! I am unable to locate \"" + datasetName + "\"")
		exit()

	# Retrieving paragraphs : Assumption is that each paragraph in dataset is
	# separated by new line character
	paragraphs = []
	for para in datasetFile.readlines():
		if(len(para.strip()) > 0):
			paragraphs.append(para.strip())

	# Loading Model
	modelName = datasetName.replace("dataset", "models").replace(".txt", ".h5")
	model =  Word2Vec.load(modelName)

	# Processing Paragraphs
	if use_word_embeddings:
		drm = DRMWM(paragraphs, model, True, True)
	else:
		drm = DRM(paragraphs, True, True)

	print("Bot> Hey! I am ready. Ask me Anything!")
	print("Bot> You can say 'Bye Bye' anytime you want")
	print("Bot> If you feel that a response from me is wrong, say 'WRONG' ")
	# Greet Pattern
	greetPattern = re.compile("^\ *((hi+)|((good\ )?morning|evening|afternoon)|(he((llo)|y+)))\ *$",re.IGNORECASE)

	# Trigger "Wrong output"
	wrongOutput = re.compile("^\ *((hi+)|((Wrong\ )?wrong|WRONG|wrong)|(he((llo)|y+)))\ *$",re.IGNORECASE)


	isActive = True
	while isActive:
		userQuery = input("You> ")
		if(not len(userQuery)>0):
			print("Bot> You need to ask something")

		## Trigger Greetings
		elif greetPattern.findall(userQuery):
			response = "Hello!"

		## Trigger Wrong Output
		## Insert code here to handle trigger wrong output
		elif wrongOutput.findall(userQuery):
			collected_dataset=""
			isActiveTraining = True
			print("Please provide responses to improve the bot...")

			while isActiveTraining:
				userQuery = input("Enter your question > ")
				numQuery = input("Enter the number of correct responses you would like to provide for the above question > ")
				answer_array=[]

				for i in range(1,int(numQuery)+1):
					answer = input("Enter correct response " + str(i) + " > ")

				isActiveTraining = False
				collected_dataset = collected_dataset + "\t" + userQuery
				response = "Thanks for your input!"

			text_file = open("dataset/user_provided_dataset.txt","wt")
			n = text_file.write(collected_dataset)
			text_file.close()

			print("Additional datapoints collected.")
			
	


		elif userQuery.strip().lower() == "bye":
			response = "Bye Bye!"
			isActive = False
		else:
			# Proocess Question
			if use_word_embeddings:
				pq = PQWM(userQuery, model, True,False,True)
			else:
				pq = PQ(userQuery,True,False,True)

			# Get Response From Bot
			response =drm.query(pq)

		userQuery_wordArray= [w.lower() for w in nltk.word_tokenize(userQuery)]
		if (userQuery_wordArray[-1]=="?" or userQuery_wordArray[-1]=="."):
			userQuery_wordArray.pop()

## Handling "Who"

		if (userQuery_wordArray[0]=='who'):
			response = response + " "+ userQuery[4:]
			if (response[-1]=="?"):
				response = response[:-1] + "."

## Handling "Where"

		if (userQuery_wordArray[0]=="where"):
			if (userQuery_wordArray[1]=="is") and (userQuery_wordArray[2]=="the"):
				response = response + userQuery[5:]
				if (response[-1]=="?"):
					response = response[:-1] + "."
			else:
				sentence=""
				for word in userQuery_wordArray[3:]:
					sentence = sentence+word+" "

				response = userQuery_wordArray[2] +" is "+ sentence +"in "+response+'.'

## Handling "When"

		if (userQuery_wordArray[0]=="when"):
			sentence=""
			for word in userQuery_wordArray[2:]:
				sentence = sentence+word+" "
			response = sentence + "in " + response+"."

## Capitalise the first letter of the sentence for aesthetics
		response=response.capitalize()

				
		print("Bot>",response)

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(
        description='P2.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-dataset', type=str, required=True,
                       help="""Filepath to the dataset""")
    parser.add_argument('-use_word_embeddings', action='store_true',
                       help="""Filepath to the dataset""")
    args = parser.parse_args()

    main(args.dataset, args.use_word_embeddings)