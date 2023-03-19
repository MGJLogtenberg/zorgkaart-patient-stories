#Import packages
import pandas as pd

#Import dataset
df = pd.read_excel("final_df2.xlsx",index_col=0)

#Drop rows with only stop words
before = len(df) #Decide number of rows before cleaning
df.dropna(axis=0,inplace=True) #Drop rows with only stop words (these are empty strings by now bc stop words are already removed)
after = len(df) #Decide number of rows after cleaning
print("Number of empty reviews after cleaning:",before-after) #Print number of deleted rows
df.reset_index(inplace=True) #Reset index

#The code below is a copy of the code for the LDA model (uncleaned). It was used to identify English words that were problematic and ended up in common topics. These words were consequently used to identify English reviews
#import gensim.corpora as corpora
#import gensim
#from gensim.models.coherencemodel import CoherenceModel
#from gensim.utils import simple_preprocess
#from __future__ import print_function
#import pyLDAvis
#from pyLDAvis import gensim_models as vis_pack
#data = list(df['review'])
#to_df = {}
#for idx, review in zip(range(len(data)),data):
#    to_df[idx] = simple_preprocess(str(review), deacc=True)
#data = list(to_df.values())
# Create Dictionary: each word links to an id
#id2word = corpora.Dictionary(data)
#Corpus converts words into tuples (combi of word and frequency of that word)
#corpus = []
#for review in data:
#    new = id2word.doc2bow(review)
#    corpus.append(new)
#lda_model = gensim.models.ldamulticore.LdaMulticore(workers=5,
#                                                    corpus=corpus,
#                                                    id2word=id2word,
#                                                    num_topics=10,
#                                                    alpha=0.01,
#                                                    eta = 0.1,
#                                                    passes=9,
#                                                    random_state=3099)
#pyLDAvis.enable_notebook()
#p = vis_pack.prepare(lda_model, corpus, id2word)
#p

#Problematic english word list
#english_words = ['to','the','and','point','doctor','my','with','very','he','you','not','for','she','that','have', 'this','it','up','her','time','on','but','as','good','always','an']

#Identify English reviews
#for idx, i in enumerate(df['review']): #Loop through each review
#    for j in i.split(' '): #Loop through each word within each review
#        if j in english_words: #If that word is included in the problematic English word list, print the review index, review and break the inner loop
#            print(idx)
#            print(idx,i)
#            print()
#            break

#Drop English reviews
#Conclusion: These reviews are in English
english_reviews = [144, 452, 492, 796, 1007, 1273, 1385, 1394, 1896, 1981, 1982, 1983, 2008, 2372, 2397, 2427, 2811, 2896, 3479, 4133, 4699, 4763, 5244, 5247, 5603, 5705, 5745, 5834, 6273, 7177, 7726, 8149, 8424, 8476, 8791, 8804, 8854, 9002, 9019, 9040, 9042, 9043, 9046, 9183, 9705, 9833, 10147, 10236, 10267, 10372, 10379, 11005, 11935, 11996, 12680, 12882, 12983, 13084, 13085, 13087, 13333, 13349, 13352, 13544, 13560, 13788, 14026, 14255, 14508, 14585, 14830, 14958, 14962, 14968, 15504, 15585, 16449, 16581, 17161, 17236, 17269, 17297, 18453, 18463, 19131, 19569, 19987, 19992, 20024, 20274, 20446, 20448, 20535, 20603, 20669, 20767, 20975, 21191, 21242, 21370, 21373, 21406, 22458, 22466, 23296, 23341, 24154, 24720, 24267, 24347, 24843, 25265, 25560, 25855, 26630, 27213, 27215, 27217, 28025, 28935, 29105, 29311, 29450, 29496, 29617, 29761, 30254, 30263, 31190, 31720, 31727, 31787, 32106, 32240, 32538, 32746, 33184, 33226, 33445, 33624, 33627, 33629, 33661, 33852, 34049, 34053, 34098, 34433, 34494, 34498, 34939, 35031, 35041, 35044, 35174, 35565, 35949, 36397, 36444, 36712, 37113, 37149, 37207, 37274, 37485, 37499, 37501, 37521, 37634, 37784, 38321, 38884, 39360, 39595, 39793, 39984, 41222, 41283, 41301, 41317, 41876, 42155, 42577, 42622, 43139, 43404, 43407, 43655, 44059, 44750, 44837, 44841, 44906, 45117, 45358, 46527, 46528, 47807, 47966, 48276, 48332, 48336, 48751, 49212, 49320, 49409, 49654, 49999, 50149, 50390, 50477, 50728, 50955, 50967, 52349, 52354, 52492, 52769, 53197, 53200, 53201, 53243, 53914, 54846, 54902, 55079, 55371, 55791, 56288, 56299, 56364, 56451, 56562, 56696, 57416, 58367, 58374, 58376, 58617, 58622, 58632, 58785]
df.drop(df.iloc[english_reviews].index,axis=0,inplace=True) #Drop English reviews
df.reset_index(inplace=True,drop=True) #Reset index
print("Number of English reviews:",len(english_reviews)) #Print number of English reviews

#Export
df.to_excel('final_df2.xlsx')