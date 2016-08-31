import requests
from bs4 import BeautifulSoup
import json
import csv
import re


# fetch one page and get term links
def requestSearchResults(startRow):
    print('Row: '+str(startRow))
    postdata={'searchTex':'A',
              'searchBy':'Letter',
              'ResetPaging':'false',
              'startRow':startRow,
              'ODA_Parent':'%7B%22category%22%3A%22Lexicon%22%2C%22name%22%3A%22Search%22%2C%22label%22%3A%22Search%22%7D'
              }
    response = requests.post(
        url='http://lexicon.ft.com/UpdateResultTerms',
        data=postdata,
        headers={ 'X-Requested-With': 'XMLHttpRequest'}
    )
    # parse response json
    responseJSON = json.loads(response.text)
    # get parsed search results
    soup = BeautifulSoup(responseJSON['html'],'html.parser')    
    # get all links
    terms = [];
    for link in soup.find_all('a'):
        termlink = link.get('href')
        # find term link from them
        if 'Term?term=' in termlink:
            if 'http://lexicon.ft.com/' not in termlink:
                    termlink = 'http://lexicon.ft.com/'+termlink
            terms.append(termlink)
    # return link list for this request
    return terms

    
    
# get terms and explanation from a term link
def parseTermPage(termlink):
    
    try:        
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
        print(termlink)
        return True
    except:
        print('Fetching failed: '+ termlink)
        return False
        
def saveCSVFile(filename,listname,content):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(listname)    
        print(content+' are saved to file '+filename+'.');
        f.close()
        
# loop start
# constants
termsPerPage = 10
maxNumPage = 1201
# prepare storage list
termlist = []
failurelist = []
termlinklist = []
for i in range(1200,maxNumPage):
    startRow = i * termsPerPage  
    terms = requestSearchResults(startRow)
    if not terms:
        print('Seaching finished.')
        break
    
    termlinklist = termlinklist + terms
    
# get terms and explanations for each content
for termlink in termlinklist:
    success = parseTermPage(termlink)
    if not success:
        failurelist.append([termlink])
        

    

# output final status
print('Totally '+str(len(termlist))+' terms and their explanations are fetched.')
# save to csv file
saveCSVFile('output.csv',termlist,'Terms and explanations')
saveCSVFile('log.csv',failurelist,'Failure logs')


        


	