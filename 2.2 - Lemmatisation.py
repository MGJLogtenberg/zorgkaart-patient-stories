#NB: This code was adjusted to Google Colab for two reasons: (1) speed and (2) lemetisation model implementation is easier
#Import packages
import spacy
import pandas as pd
from gensim.utils import simple_preprocess

#Set Google colab and import dataset
from google.colab import drive
drive.mount('/content/drive')
get_ipython().run_line_magic('cd', '/content/drive/My\\ Drive/Thesis')
df = pd.read_excel("final_df1.xlsx",index_col=0)

#Drop rows with only stop words
before = len(df) #Decide number of rows before cleaning
df.dropna(axis=0,inplace=True) #Drop rows with only stop words (these are empty strings by now bc stop words are already removed)
after = len(df) #Decide number of rows after cleaning
print("Number of empty reviews after cleaning:",before-after) #Print number of deleted rows
df.reset_index(inplace=True) #Reset index

#Lemmatiser
#Based on: https://www.datasciencelearner.com/spacy-lemmatization-implementation-python-steps/
get_ipython().system('python -m spacy download nl_core_news_sm #Download language model')
to_df = {} #Initiate temp dict
nlp = spacy.load("nl_core_news_sm") #Load language model
for idx in range(len(df)): #Loop through each row
  review = nlp(df['review'][idx]) #Load the review within the language model (divides into tokens)
  empty_list = [] #Initiate temp list
  for token in review: #Loop through each token in the list
      empty_list.append(token.lemma_) #Transform each token (word) to its lemma, and append to temp list
  final_string = ' '.join(map(str,empty_list)) #Join each word in temp list to eachother, so that we end up with strings again
  to_df[idx] = final_string #Store the lemmatised string in temp dict
  if idx % 1000 == 0: #Print an update after each 1000 rows
    print("Number of reviews processed:",idx)
df['review'] = to_df.values() #Copy the data from the temp dict to DataFrame

#Manual flaw fixing (two significant flaws)
to_df = {} #Initiate temp dict
for idx, review in enumerate(df['review']): #Loop through each row
    review2 = review #Copy the story (so that we can alter the review without side-effects)
    if 'luistren' in review: #If typo, transform
        review2 = review2.replace('luistren','luisteren')
    if 'opluisteren' in review: #If typo, transform
        review2 = review2.replace('opluisteren','luisteren')
    if 'neemt' in review: #If typo, transform
        review2 = review2.replace('neemt','nemen')
    to_df[idx] = review2 #Copy the story copy to the temp dict
df['review'] = to_df.values() #Copy the data in temp dict to DataFrame

#Simple preprocess
to_df = {} #Initiate temp dict
for i in range(len(df)): #Loop through each row
    to_df[i] = simple_preprocess(str(df.loc[i,'review']), deacc=True) #Simple preprocess implementation
df['review'] = to_df.values() #Copy the data in temp dict to DataFrame

#Additional stop words to increase relevance
stop_words = ['huisarts','arts','patient','patiënt','dokter','dr','nummer','komen','gaan','krijgen','weer','doen','hebben','laat','maken','laten','vinden','erg','zien','willen','keer','heel','zeer','worden','we','al','ons','zijn','mogen','echt','blijven','kunnen','arts','dhr'] #Add manual stop words
to_df = {} #Initiate temp dict
for idx in range(len(df)): #Loop through each row
    no_stpwords_string="" #Initiate empty string
    for i in df.loc[idx,'review']: #Loop through each word in review
        if not i in stop_words: #If word is not a stopword, append to the empty string (so that we rebuild the review)
            no_stpwords_string += i+' '
    final_string = no_stpwords_string[:-1] #Copy the string to a temp object, without the last whitespace
    to_df[idx] = final_string #Copy the temp object to the temp dict
df['review'] = to_df.values() #Copy the data in temp dict to DataFrame

#Export
df.to_excel('final_df2.xlsx')