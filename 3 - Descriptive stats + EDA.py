#Import packages
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

#Import dataset
df = pd.read_excel("final_df2.xlsx",index_col=0)

#Wordcloud: overall
long_string = ' '.join(list(df['review'].values)) #Join all reviews into one string
#Based on: https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0
wordcloud = WordCloud(collocations=False,background_color="white", contour_width=3, contour_color='steelblue') #Set wordcloud settings
wordcloud.generate(long_string) #Generate wordcloud
wordcloud.to_file('wordcloud_all.pdf') #Export to file

#Subset ratings into low, medium and high
low_ratings = df[df['avg_rating'] < 6]
med_ratings = df[(df['avg_rating'] >= 6) & (df['avg_rating'] < 9)]
high_ratings = df[df['avg_rating'] >= 9]

#Low ratings word cloud (explanation code: see above)
long_string = ' '.join(list(low_ratings['review'].values))
wordcloud = WordCloud(collocations=False,background_color="white", contour_width=3, contour_color='steelblue')
wordcloud.generate(long_string)
wordcloud.to_file('wordcloud_low.pdf')

#Medium ratings word cloud (explanation code: see above)
long_string = ' '.join(list(med_ratings['review'].values))
wordcloud = WordCloud(collocations=False,background_color="white", contour_width=3, contour_color='steelblue')
wordcloud.generate(long_string)
wordcloud.to_image()

#High ratings word cloud (explanation code: see above)
long_string = ' '.join(list(high_ratings['review'].values))
wordcloud = WordCloud(collocations=False,background_color="white", contour_width=3, contour_color='steelblue')
wordcloud.generate(long_string)
wordcloud.to_image()

#Histogram of average ratings in reviews
plt.figure(figsize=(10,4)) #Set figure+size
sns.histplot(df['avg_rating'],binwidth=0.5) #Define histplot
plt.xlabel("Average rating") #Define X label
plt.ylabel("Number of reviews") #Define Y label
plt.xlim(0.9,10.1) #Set X axis limits
plt.savefig('hist_grades.pdf', dpi=100) #Export figure

#Print dataset sizes each
print(len(df[df['avg_rating']<6]))
print(len(df[(df['avg_rating']>=6) & (df['avg_rating']<9)]))
print(len(df[df['avg_rating']>=9]))