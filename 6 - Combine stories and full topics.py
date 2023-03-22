#Import packages
import pandas as pd
import os

#Import & merge
df1 = pd.read_excel("final_df.xlsx",index_col=0) #Import stories
os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Results SQ1") #Change working directory
df2 = pd.read_excel("probs.xlsx",index_col=0) #Import topics
df = pd.concat([df1,df2],axis=1,keys='key_0',join='inner') #Join together on key (URL) to new DataFrame
df.to_excel("probs2.xlsx") #Export
os.chdir("C:\\Users\\mlogt\\Dropbox\\Health Humanities\\Thesis\\Code") #Change working directory to default
