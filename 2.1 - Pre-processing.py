#Import packages
import pandas as pd
from stop_words import get_stop_words
import re
import time
import phunspell

#Import dataset
df = pd.read_excel("final_df.xlsx",index_col=0)

#Some cleaning
df = df.replace({'\n':''},regex=True) #Remove tabs
df = df.apply(lambda x: x.astype(str).str.lower()) #Lower casing
#Based on: https://www.geeksforgeeks.org/normalizing-textual-data-with-python/
to_df = {} #Initiate dict for temporary data storage
for idx, i in enumerate(df['review']): #Loop through each row
    no_number_string = re.sub(r'\d+','',i) # remove numbers
    no_punc_string = re.sub(r'[^\w\s]','', no_number_string) # remove all punctuation except words and space
    no_wspace_string = no_punc_string.strip() # remove white spaces   
    to_df[idx] = no_wspace_string #Store cleaned string in dict
df['review'] = to_df.values() #Copy dict data to df

#Debug: Remove xd for number to prevent mix of words
to_df = {} #Initiate dict for temporary data storage
for idx,i in enumerate(df['review']): #Loop through each row
    if "xd" in i: #If, number in review
        string = i #Copy review to temp object
        string = string.replace('xd',' nummer ') #Replace xd with 'nummer'
        string = string.replace('_','') #Delete '_'
        string = " ".join(string.split()) #Split each string to list and join again, such that each word is seperated by only one whitespace
        to_df[idx] = string #Copy string to temp dict
    else: #Else, copy review to temp dict
        to_df[idx] = i
df['review'] = to_df.values() #Copy dict data to df

#Spellchecker with limited time window
pspell = phunspell.Phunspell('nl_NL') #Initiate spellchecker
def SpellCheck(i,j): #Define function: for each word in review that is possibly misspelled, replace with suggestion
    for suggestion in pspell.suggest(j):
        i = i.replace(j,suggestion)
        break #Note: Only take the first suggestion
for idx,i in enumerate(df['review']): #Loop through each row
    misspelled = pspell.lookup_list(i.split()) #Look up each misspelled word
    startTime = time.time() #Set start time
    for j in misspelled: #For each misspelled word, suggest a new word (only if there is a suggestion and it can be done within 5 seconds)
        if j not in ['dr','dr.']: #Exception: dr & dr. are not misspelled
            if pspell.suggest(j): #If there is a suggestion, correct within 5 seconds or skip
                startTime = time.perf_counter()
                timeout = startTime + 5
                while time.time() < timeout:
                    SpellCheck(i,j) #Spellcheck misspelled word
    to_df[idx] = i #Store new story in temp dict
    if idx % 500 == 0: #Print update after each 500 rows
        print("Number of reviews processed:",idx)
df['review'] = to_df.values() #Copy dict data to df

#Remove stop words
#Based on: https://www.geeksforgeeks.org/normalizing-textual-data-with-python/
stop_words = get_stop_words('dutch') #Load stop_word list
stop_words = stop_words + ['huisarts','arts','patient','dokter','dr'] #Add manual stop words
to_df = {} #Set temp dict
for idx in range(len(df)): #Loop through each row
    no_stpwords_string="" #Set empty string to build from
    for i in [df['review'][idx]][0].split(): #Loop through each word in the story
        if not i in stop_words: #If the word is NOT in the stop word list, append to empty string
            no_stpwords_string += i+' '
    to_df[idx] = no_stpwords_string[:-1] #Copy empty string to temp dict (without last char = a whitespace)
df['review'] = to_df.values() #Copy dict data to df

df.to_excel('final_df1.xlsx') #Export data