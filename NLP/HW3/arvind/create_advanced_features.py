from collections import namedtuple
import csv
import sys
import glob
import os
import re

def get_utterances_from_file(dialog_csv_file):
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    with open(os.getcwd()+"/"+dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict):

    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            continue		#Skipping the iteration if no there are no TOKEN/POS pairs present in an utterance

    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)


#Main Function

utterances = get_utterances_from_filename(sys.argv[1])	#Retrieve utterances for each .csv filename passed
line_no =1
speaker_list=[]
output_string=""
for index, utterance in enumerate(utterances):		#Iterate through each utterance in the file and retrieve the index as well.
	output_string=""
	token_string=""
	pos_string=""
	
	if(utterance[0]!=""):				#Check if dialog_tag is present or else insert UNKNOWN tag
		dialog_tag = utterance[0]
	else:
		dialog_tag = "UNKNOWN"
	
	speaker = utterance[1]
	if(line_no == 1 or line_no == 2):
		speaker_list.append(speaker)
	else:
		speaker_list.pop(0)
		speaker_list.append(speaker)

	token_pos_list = utterance[2]
	token_list=[]
	pos_list=[]
	for token_pos in token_pos_list:
		token = token_pos[0]
		pos = token_pos[1]
		token_string+="\tTOKEN_"+token
		pos_string+="\tPOS_"+pos
		token_list.append(token)
		pos_list.append(pos)

		
	token_bigrams = zip(token_list,token_list[1:])		#Retrieve Bigrams of TOKENS	
	for i in token_bigrams:
		bigram = "/".join(i)
		token_string+="\tTOKEN_"+bigram

	pos_bigrams = zip(pos_list,pos_list[1:])		#Retrieve Bigrams of POS tags
	for i in pos_bigrams:
		bigram = "/".join(i)
		pos_string+="\tPOS_"+bigram
		
	token_trigrams = zip(token_list,token_list[1:],token_list[2:])		#Retrieve Trigrams of TOKENS
	for i in token_trigrams:
		trigram = "/".join(i)
		token_string+="\tTOKEN_"+trigram
	
	pos_trigrams = zip(pos_list,pos_list[1:],pos_list[2:])		#Retrieve Trigrams of POS tags
	for i in pos_trigrams:
		trigram = "/".join(i)
		pos_string+="\tPOS_"+trigram
	
	output_string+=dialog_tag
	if(line_no == 1):		#Check if it is the first line of the csv file, if so insert a feature f[0] as 1 	
		output_string+="\tf[0]=1"
	if(len(speaker_list)==2 and speaker_list[0] != speaker_list[1]):
		output_string+="\tf[1]=0"	#Check if the speakers have changed in consecutive utterances, if so insert f[1] as 0
	if("?" in token_list):		#Check if the utterance is a question, if so insert f[2] as 1
		output_string+="\tf[2]=1"				
	output_string+=token_string	#Insert list of TOKENS starting from unigrams followed by bigrams followed by trigrams
	output_string+=pos_string	#Insert corresponding list of POS tags for unigrams followed by bigrams followed by trigrams
	if(index+1 < len(utterances)):		# Extracting the first word of next utterance
		first_word = utterances[index+1].pos
		if(first_word):
			first_word_next_line = first_word[0]
			if(first_word_next_line):
				output_string+="\tfirst_word_next_line_"+str(first_word_next_line.token)
	line_no+=1
	sys.stdout.write(output_string+"\n")
sys.stdout.write("\n")

