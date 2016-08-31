import requests
from bs4 import BeautifulSoup
import string
import csv
import re

# loop start
# prepare storage list
termlinklist = []
for letter in string.ascii_uppercase:
    print(letter)
    htmlPage = requests.get('http://lexicon.ft.com/Search?letter='+letter).text
    soup = BeautifulSoup(htmlPage,'html.parser')
    for link in soup.find_all('a'):
        termlink = link.get('href')
        # find term link from them
        if 'Term?term=' in termlink:
            if 'http://lexicon.ft.com/' not in termlink:
                    termlink = 'http://lexicon.ft.com/'+termlink
            termlinklist.append(termlink)    
    
    
# get terms and explanations for each content
termlist = []
for termlink in termlinklist:
    print(termlink)
    # open term link
    termHTML = requests.get(termlink).text
    termSoup = BeautifulSoup(termHTML, 'html.parser')
    # get term title div        
    title = termSoup.find_all('div',{'class':'moreItemsHeader'})
    # get title div string
    titleString = title[0].text
    # get title term, delete "Difinition of " totally 14 words
    term = titleString[14:]
    # get term explanation
    explanation = termSoup.find_all('div',{'class':'definition'})[0].text       
    # remove unnecessary characters
    explanation = re.sub('[^a-zA-Z0-9-_*.,;:+\/\&\@\"\'\(\)\$\%\[\]]', ' ', explanation)
    # parse term link
    termlist.append([term,explanation])
    

# output final status
print('Totally '+str(len(termlist))+' terms and their explanations are fetched.')

# save to csv file
with open('output.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerows(termlist)    
    print('Results are saved to file output.csv.');
    f.close()


        


	