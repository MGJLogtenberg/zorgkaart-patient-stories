#Import packages
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#Visualisation: n_topics on UMass coherence
df = pd.read_excel("Results LDA coherence.xlsx",index_col=0) #Import appropiate data
plt.figure(figsize=(12, 4), dpi=80) #Set figure
sns.lineplot(data=df.T,palette='Blues') #Define lineplot
plt.axvline(x=6,ls=(0, (1, 10))) #Set vertical line on X axis
plt.title('Results LDA model tuning, coherence scores UMass per number of topics') #Set plot title
plt.ylabel('UMass Coherence Score') #Set Y label
plt.xlabel('Number of topics') #Set X label
plt.legend(title='Number of passes') #Set legend
plt.savefig("LDA_tuning_ntopics.pdf") #Export figure

#Visualisation: n_passes on c_v coherence (explanation above)
df = pd.read_excel("Results LDA coherence.xlsx",'C_v',index_col=0)
plt.figure(figsize=(12, 4), dpi=80)
sns.lineplot(data=df,palette='Blues')
plt.axvline(x=7,ls=(0, (1, 10)))
plt.title('Results LDA model tuning, coherence scores c_v per number of passes')
plt.ylabel('c_v Coherence Score')
plt.xlabel('Number of passes')
plt.legend(title='Number of topics')
plt.savefig("LDA_tuning_npasses.pdf")