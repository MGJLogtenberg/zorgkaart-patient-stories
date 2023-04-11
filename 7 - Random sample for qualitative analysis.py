#Import packages
import pandas as pd
import os
import numpy as np

#Import dataset
os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Results SQ1") #Change working directory
df = pd.read_excel("probs2.xlsx",index_col=0)

#Append length information to dataframe
for_df = {} #Initiate temp dict
for idx, i in enumerate(df['review_y']): #Loop through all stories
        for_df[idx] = len(i)-6 #Count number of characters, subtract 6 (because of /nl) and append to temp dict
df['length'] = for_df.values() #Copy temp dict data to DataFrame

os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Results SQ2") #Change working directory

#Sample 50 reviews on each topic
for topic in range(1,7): #Loop through each topic
    data = df[df['prob_'+str(topic)]>.5] #Subset reviews with high probability on each topic
    data = data.sample(50) #Sample 50 stories on each topic
    data.to_excel("Reviews topic_"+str(topic)+".xlsx") #Export sample to excel

#Sample 50 reviews among hard-to-classify topics
os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Results SQ2") #Change working directory
data = df.query('prob_1 < 0.5  & prob_2 < 0.5 & prob_3 < 0.5 & prob_4 < 0.5 & prob_5 < 0.5 & prob_6 < 0.5') #Subset all stories not sign belonging to any story
data = data.sample(50) #Sample 50 stories on each topic
data.to_excel("Reviews topic_remainder.xlsx") #Export sample to excel

#Average length and rating remaining reviews
print("Average length remaining reviews:",np.mean(data['length'])) #Print average length remaining reviews
print("Average rating remaining reviews:",np.mean(data['avg_rating'])) #Print average rating remaining reviews
print() #New line
print("Average length remaining reviews:",np.mean(df['length'])) #Print average length remaining reviews
print("Average rating remaining reviews:",np.mean(df['avg_rating'])) #Print average rating remaining reviews