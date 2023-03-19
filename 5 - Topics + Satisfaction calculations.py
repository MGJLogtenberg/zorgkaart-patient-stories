import pandas as pd
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from sklearn.model_selection import train_test_split

df = pd.read_excel("final_df2.xlsx",index_col=0)
df.dropna(axis=0,inplace=True)
data = list(df['review'])

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

#Define Best model (has 6 topics, 7 passes)
lda_model = gensim.models.ldamulticore.LdaMulticore(workers=5,
                                                    corpus=train_corpus,
                                                    id2word=id2word,
                                                    num_topics=6,
                                                    alpha=0.01,
                                                    eta = 0.1,
                                                    passes=7,
                                                    random_state=3099)

#Reset index and drop old index
df.reset_index(inplace=True,drop=True)
df.drop('index',axis=1,inplace=True)

#Get topic probabilities for each review
dict_0 = dict.fromkeys(range(len(df)), 0) #Initiate temp dicts with 0's for the length of the number of reviews for each topic
dict_1 = dict.fromkeys(range(len(df)), 0)
dict_2 = dict.fromkeys(range(len(df)), 0)
dict_3 = dict.fromkeys(range(len(df)), 0)
dict_4 = dict.fromkeys(range(len(df)), 0)
dict_5 = dict.fromkeys(range(len(df)), 0)
for idx, i in enumerate(df['review']): #Loop through each review
    prob = lda_model.get_document_topics(id2word.doc2bow(list(simple_preprocess(str(i), deacc=True)))) #Calculate topic probabilities of that review
    for j in prob: #For each topic probability
        if j[0] == 0: #If it corresponds to appropiate topic, copy probability to temp dict
            dict_0[idx] = j[1]
        if j[0] == 1:
            dict_1[idx] = j[1]
        if j[0] == 2:
            dict_2[idx] = j[1]
        if j[0] == 3:
            dict_3[idx] = j[1]
        if j[0] == 4:
            dict_4[idx] = j[1]
        if j[0] == 5:
            dict_5[idx] = j[1]
    if idx % 10000 == 0: #Print an update after every 10,000 reviews
        print("Number of reviews processed:",idx)
df['prob_1'] = dict_0.values() #Copy data from temp dict to column in DataFrame
df['prob_2'] = dict_1.values()
df['prob_3'] = dict_2.values()
df['prob_4'] = dict_3.values()
df['prob_5'] = dict_4.values()
df['prob_6'] = dict_5.values()

#Calculate average satisfaction ratings
for topic in range(1,7): #Loop through each topic
    tot = 0 #Initiate running total
    for i in range(len(df)): #Loop through each review
        tot += df.loc[i,'prob_'+str(topic)]*df.loc[i,'avg_rating'] #Add the product of the probability of each topic and the average rating of each review to the running total
    print("Average satisfaction for topic",topic," :",tot / sum(df['prob_'+str(topic)])) #Calculate avg (running total divided by the sum of probabilities for that topic) and print this avg

#Export all keyword probabilities
for i in range(0,6): #Loop through each topic
    df2 = pd.DataFrame(lda_model.show_topic(i,50)) #Calculate dataframe with keyword probabilities
    df2.to_excel('keywords_topic'+str(i+1)+'.xlsx') #Export to Excel

#Classify each review with appropiate topic
df.drop('level_0',axis=1,inplace=True) #Drop irrelevant column
to_df = {} #Initiate temp dict
for i in range(len(df)): #Loop through each review
    l = list(df.iloc[i,3:,]) #Initiate temp list with the topic probabilities of a review
    to_df[i] = l.index(max(l)) + 1 #Take the maximum of temp list and assign to temp dict
df['topic'] = to_df.values() #Copy values in temp dict to DataFrame

#Export probability dataframe to Excel
df.to_excel('probs.xlsx')

#Print the number of reviews assigned to each topic
df['topic'].value_counts()