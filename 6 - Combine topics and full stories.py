#Import packages
import pandas as pd
import os
import numpy as np

#Import & merge
df1 = pd.read_excel("final_df.xlsx",index_col=0) #Import stories
os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Results SQ1") #Change working directory
df2 = pd.read_excel("probs.xlsx",index_col=0) #Import topics
df = pd.merge(df2,df1[['key_0','review']],on='key_0') #Merge together on key (URL) to new DataFrame
df.to_excel("probs2.xlsx") #Export
os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Code") #Change working directory to default

#Compute average length of a story
for topic in range(1,7): #Loop through each topic
    l = [] #Initiate temp list
    for i in df[df['topic']==topic]['review_y']: #Loop through each review linked to this topic
        l.append(len(i)-6) #Append the length of each review to temp list (minus 6 = length of \nl)
    print("Topic {} - average length story: {}".format(topic,np.mean(l))) #Print average length of the story for each topic