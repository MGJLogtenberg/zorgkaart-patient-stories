# “Maybe this doctor should learn to listen…”: A mixed-methods approach to identify common topics and practices in Dutch patient stories about their general practitioner

Overview of the repository (number indicates the order to run):

1 - Data scraping: Code to scrape the reviews from Zorgkaart (deleted)

    I deleted this part of the code in accordance with my ethical considerations regarding copyright. For more information, see Section 5.1 of my thesis.

2 - Cleaning: Code to clean the reviews

    2.1 - Preprocessing: Basic cleaning, spellchecking and stop word removal

    2.2 - Lemmatisation: Lemmatise all reviews

    2.3 - English review removal: Identify and remove all English reviews

3 - Descriptive stats + EDA: Code to visualise word clouds, histogram and dataset sizes

4 - LDA model tuning: Code to tune LDA model and visualise tuning results

    4.1 - LDA model (tuning): Tune LDA model

    4.2 - LDA tuning visualisation: Visualise tuning results

5 - Topics + Satisfaction rating calculations: Code to calculate the average satisfaction, assign topics to each review, and get keyword probabilities

6 - Combining topics and full stories: Code to combine topics probabilities and full stories for analysis + examples (this code also includes calculation of average length for each topic)

7 - Random sample for qualitative analysis: Code to append length information, sample 50 stories for each topic (+ 50 hard-to-classify stories) and print the average length of hard-to-classify topics and average overall


_For the code in 4 to 7, the notebooks including the final run were also uploaded. In this way the reader can see the results of the code_


Please credit: Martijn Logtenberg
