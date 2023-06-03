#Import packages
import gensim
from gensim.models.coherencemodel import CoherenceModel
from gensim.utils import simple_preprocess
import pandas as pd
import gensim.corpora as corpora
from sklearn.model_selection import train_test_split
from __future__ import print_function
import pyLDAvis
from pyLDAvis import gensim_models as vis_pack

#Import dataset
df = pd.read_excel("final_df2.xlsx",index_col=0)

#Simple preprocess
to_df = {} #Initiate temp dict
for i in range(len(df)): #Loop through each row
    to_df[i] = simple_preprocess(str(df.loc[i,'review']), deacc=True) #Simple preprocess implementation
df['review'] = to_df.values() #Copy the data in temp dict to DataFrame
#Transform data to list and make dictionary (dictionary contains each occuring word)
data = list(df['review']) #Transform data to list
id2word = corpora.Dictionary(data) # Make dictionary, where each word links to an id

#Train test split
train, test = train_test_split(data,train_size=0.8,random_state=3099) #Split data
train_corpus = [] #Initiate train corpus, corpus converts words into tuples (combi of word and frequency of that word)
for review in train: #Loop through train data, transform each review to ids (corresponding to the dictionairy) and add to the train corpus
    new = id2word.doc2bow(review)
    train_corpus.append(new) 
test_corpus = [] #Initiate test corpus, corpus converts words into tuples (combi of word and frequency of that word)
for review in test: #Loop through test data, transform each review to ids (corresponding to the dictionairy) and add to the test corpus
    new = id2word.doc2bow(review)
    test_corpus.append(new)

#Tune model
for n_topics in [6,8,10,12,14,16]: #Loop through possible n_topics
    for n_passes in [1,3,5,7,9]: #Loop through possible n_passes (inner loop; NB: goes through each combination of n_topics & n_passes)
        lda_model = gensim.models.ldamulticore.LdaMulticore(workers=5, #Specify model
                                                            corpus=train_corpus,
                                                            id2word=id2word,
                                                            num_topics=n_topics,
                                                            alpha=0.01,
                                                            eta = 1/n_topics,
                                                            passes=n_passes,
                                                            random_state=3099)
        coherence_model_umass = CoherenceModel(model=lda_model, texts=test, dictionary=id2word,coherence='u_mass') #Calculate coherence (UMass)
        coherence_model_cv = CoherenceModel(model=lda_model, texts=test, dictionary=id2word,coherence='c_v') #Calculate coherence (c_v)
        #Print relevant details
        print('Model built with n_topics:',n_topics) #n_topics
        print('Model built with n_passes:',n_passes) #n_passes
        print('Coherence (U_Mass):',coherence_model_umass.get_coherence()) #Coherence (UMass)
        print('Coherence (c_v):',coherence_model_cv.get_coherence()) #Coherence (c_v)
        print() #White row

#Visualise final model
#Interpretation: Best model has 6 topics, 7 passes
lda_model = gensim.models.ldamulticore.LdaMulticore(workers=5, #Specify final model
                                                    corpus=train_corpus,
                                                    id2word=id2word,
                                                    num_topics=6,
                                                    alpha=0.01,
                                                    eta = 0.1,
                                                    passes=7,
                                                    random_state=3099)
pyLDAvis.enable_notebook() #Allow package to show in notebook
p = vis_pack.prepare(lda_model, test_corpus, id2word, sort_topics=False) #Set visualisation of final model
p #Show visualisation of final model