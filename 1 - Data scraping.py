#Import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#Collect URLs to mine
urls = [] #Initiate URL list
for j in range(421): #Loop through 421 (=number of GP overview pages on Zorgkaart as of 18/12)
    url = 'https://www.zorgkaartnederland.nl/huisarts/pagina'+str(j+1) #Set URL to appropiate page
    response = requests.get(url) #Get access to URL
    soup = BeautifulSoup(response.text, "html.parser") #Go to overview page
    for idx, i in enumerate(soup.findAll('a')): #For each overview page, find all text on the page
        if idx <= 14 or idx > 74: #If it's not in the appropiate range, skip (this is possible because each overview page is standardised)
            continue
        if 'zorgverlener' in i['href']: #Look at all links within the appropiate range: If the word 'zorgverlener' occurs, append to the URL list
            if i['href'] not in urls: #Only append if URL is not yet in this list (debug)
                urls.append(i['href'])
    if j % 50 == 0: #For each 50 overview pages, print update
        print("Progress (pages processed):",j)
#Debug: Some URLs do not concern GPs, these should be removed
to_drop = [] #Initiate list for cleaning
urls = pd.DataFrame(urls,columns=['URL']) #Set URLs in Pandas dataframe
for idx,i in enumerate(urls['URL']): #For each URL, check if it concerns a GP
    if '/zorgverlener/huisarts-' not in i: #If not, append to the to_drop list
        to_drop.append(idx)
urls.drop(to_drop,inplace=True) #Drop all URLs in the to_drop list
print("Number of URLS deleted because of cleaning:",len(to_drop)) #Print the number of dropped URLs
urls.reset_index(inplace=True,drop=True) #Reset index
urls.to_excel("URLS_backup.xlsx") #Export GP URL pages

#Collect review URLs
counter = 0 #Initiate counter (used for updates during mining)
for GP_index in range(len(urls)): #Loop through each GP URL
    #Get number of pages
    url = "https://www.zorgkaartnederland.nl"+urls['URL'][GP_index]+'/waardering/pagina1' #Set URL to first page of the GP
    response = requests.get(url) #Get access to the first GP page URL
    soup = BeautifulSoup(response.text, "html.parser") #Go to the first GP page URL
    a = soup.findAll('a') #Find all text
    pages = [] #Initiate temporary list, to store the page numbers in
    for idx,i in enumerate(a): #For each block in text
        if 'img alt="Website Patiëntenfederatie Nederland' in str(i): #Exception: If it is the link to this other website, skip
            break
        if 'class=' in str(i): #If the block of text contains a class, check if the class is a page link
            if i['class'] == None or i['class'] == ['page-link']:
                pages.append(i['title']) #If the class is a page link, append to temporary list
            if i['class'] == None or i['class'] == ['filter-radio']:
                break #Else: skip
    if pages: #If there are multiple pages for a GP, take the last digit of the temporary list (the number of GP pages)
        x = int(pages[-1].replace("Pagina ",""))
    else: #If there aren't multiple pages, take 1
        x = 1
    #Note: x now contains the number of GP pages to loop through
    #Extract review URLS on one page
    review_urls = [] #Initiate temporary list to store review URLs in
    for j in range(x): #Loop through the number of GP pages
        url = "https://www.zorgkaartnederland.nl"+urls['URL'][GP_index]+'/waardering/pagina'+str(j+1) #Set URL to the appropiate GP page
        response = requests.get(url) #Get access to the appropiate GP page URL 
        soup = BeautifulSoup(response.text, "html.parser") #Go to the appropiate GP page URL
        a = soup.findAll('a') #Find all text
        for idx,i in enumerate(a): #For each block of text
            if 'img alt="Website Patiëntenfederatie Nederland' in str(i): #Exception: If it is the link to this other website, skip
                break
            if 'class=' in str(i): #If the block of text contains a class, check if the class is a page link
                if i['class'] == ['page-link'] or i['class'] == ['filter-radio']: #Exception: If it is a page link or another link, skip
                    break
                if urls['URL'][GP_index]+'/waardering/' in i['href']: #If the class is a review link, append to temporary list
                    if i['href'] not in review_urls: #Exception: If it is not yet in the review_url (debug)
                        review_urls.append(i['href'])
    counter += len(review_urls) #Increase counter with the number of review URLs mined
    review_urls = pd.DataFrame(review_urls) #Save the mined review URLs to Pandas DataFrame
    review_urls.to_excel("Review URLs/ReviewURLs_"+urls['URL'][GP_index].split('/')[2]+".xlsx") #Export the review URLs FOR EACH GP to Excel
    if GP_index % 100 == 0: #For each 100 GPs, print an update
        print("Number of GPs processed:",GP_index)
        print("Number of review URLs mined:",counter)
print("Final number of review URLs mined:",counter) #Print the number of review URLs mined

#Collect reviews
for_df = {} #Initiate temp dicts (1 for score, 1 for story)
for_df2 = {}
path = #Set path in which I kept the review URLs
files = os.listdir(path) #Initiate list with all files in the folder
counter = 0 #Set counter (used for updates)
for idx_GPs, i in enumerate(files): #Loop through each file (each file contains the review URLs of one GP)
    review_urls = pd.read_excel(path + files[idx_GPs],names=[0,'URL']) #Read the URLs
    if review_urls.empty: #If there are no review URLs for this GP, skip this GP
        continue
    for j in review_urls['URL']: #Loop through each review URL
        url = "https://www.zorgkaartnederland.nl"+j #Set to review page URL
        response = requests.get(url) #Get access to the review page
        #Collect average score
        soup = BeautifulSoup(response.text, "html.parser") #Go to the review page
        span = soup.findAll('span') #Find all data in the span container (this is where the score is stored)
        for idx, k in enumerate(span): #Loop through all content in the container
            if 'filter-result__score' in str(k): #If the average score is encountered, save in temp object
                score = k.text
        for_df[j] = score #Copy temp object to temp dict (scores)
        #Collect story
        soup = BeautifulSoup(response.text, "html.parser") #Go to the review page
        p = soup.findAll(['p','h2']) #Find all text on the review page (including second headers, necessary for excluding responses)
        for idx, k in enumerate(p): #Loop through each text element
            #Both "De redactie kan een waardering niet op waarheid controleren." and "Reactie van/namens" indicate the end of the story, break because the story was the element right before this
            if "De redactie kan een waardering niet op waarheid controleren." in k.text:
                break
            if "Reactie van/namens" in k.text:
                break
            review = k.text #Store the story in temp object
        for_df2[j] = review #Copy temp object to temp dict (stories)
        counter += 1 #Increase counter with 1 (for 1 review)
    if idx_GPs % 100 == 0: #Print an update after each 100 reviews
        print("Number of GPs processed:",idx_GPs)
        print("Number of reviews processed:",counter)
        #Backup stuff
        #backup_avg = pd.Series(for_df,name='avg_rating').T
        #backup_review = pd.Series(for_df2,name='review').T
        #backup = pd.merge(left=backup_avg,right=backup_review,left_on=backup_avg.index,right_on=backup_review.index)
        #backup.to_excel("Backup/after_"+str(idx_GPs)+".xlsx")

#Export
print("Number of GPs processed:",idx_GPs) #Print number of GPs processed
print("Number of reviews processed:",counter) #Print number of reviews processed
final_avg = pd.Series(for_df,name='avg_rating').T #Set temp dict (scores) to pandas Series
final_review = pd.Series(for_df2,name='review').T #Set temp dict (stories) to pandas Series
final = pd.merge(left=final_avg,right=final_review,left_on=final_avg.index,right_on=final_review.index) #Merge the two Series to one DataFrame
final.to_excel("final_df.xlsx") #Export