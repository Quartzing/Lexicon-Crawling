# Python-Crawling

It is my first time to do the crawling on Python. Recently a friend asked if I can get all of the terms and their explanations from lexicon.ft.com. After taking a look at its website I found that the term pages are indexed alphabetically. Seems like this is not a hard task.

##Initial plan:
After checking the url of the term pages, the followings are found:
* Each index page has the url = http://lexicon.ft.com/Search?letter=A
* Each term page has the url = http://lexicon.ft.com/Term?term=A-H1N1

So the implementation is
####1. fetch each index page (A-Z) using requests, and find and store the urls for each term via bueatiful soup
After investigating the source code of the index page, we can notice that all of the term urls are stored in `<a href="Term?term=***">`
, so just loop all hrefs and find the ones with "Term?term=":
```Python
    for link in soup.find_all('a'):
        termlink = link.get('href')
        # find term link from them
        if 'Term?term=' in termlink:
            if 'http://lexicon.ft.com/' not in termlink:
                    termlink = 'http://lexicon.ft.com/'+termlink
            termlinklist.append(termlink)    
```
####2. fetch each term page using request, and find and store the term and the explanation via bueatiful soup
In its souce code, all terms are stored in `<div class="moreItemsHeader">` and explanation is stored in `<div class="definition">`, so just get element.text via bueatiful soup (do not use .string). 
```Python
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
    termlist.append([term,explanation])
```
####3. The result list is saved to csv file. 
```Python
# save to csv file
with open('output.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerows(termlist)    
    print('Results are saved to file output.csv.');
    f.close()
```
Special characters like \xa0 \xa3 will cause problem in saving a text file. Thus this line is added to remove them:
```Python
explanation = re.sub('[^a-zA-Z0-9-_*.,;:+\/\&\@\"\'\(\)\$\%\[\]]', ' ', explanation)
```

This formed the initial version. However the biggest problem is that only 10 terms are shown on each index page. It turns out to be a http request. Seems like this is not as easy as I thought to be in the beginning.

##Upgraded plan:
The solution is to mimick the action taken by clicking the "next" button. Open the developing tool in chrome and click any of the page link, we can see that in Network page, there is a new POST - "UpdateResultTerms". Click it, and in its header we can find the request url and the header data.
```
searchText:A
searchBy:Letter
ResetPaging:false
startRow:11
ODA_Parent:{"category":"Lexicon","name":"Search","label":"Search"}
```
Notice that there is a searhcText letter A, and startRow 11. Actually the startRow is the most important one: if it exceeds the max number of letter A it will automatically fetch the rows for letter B, and so on until letter Z. the task becomes to post the request to the url with different startRows until blank response is received.

First of all, we need to mimick the same data format to post request to the server to get the response.
``` Python
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
```
The response is a json string, and it has two parameters:
* html: html content to update the search result. This is what we wanted.
* json: it provides the max number of rows per page and the max number of pages.

Actually the html parameter has provided us all info we need to obtain the term links, thus it is not necessary to request the index page anymore. 

Also we wrap the codes into functions to make it more organized. 

##Final plan:
It seems the upgraded plan works well. When running through all terms, however, it is found that this version may take couple of hours. Is there any way to enhance the speed?
The answer is to parallelly post the http requests via multi-threading. This may cause the order issue, but this is much easier to handle.
```Python
import threading
def parallelProcess(targetfun,source):
    threads = [threading.Thread(target=targetfun, args=(i,)) for i in source]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
```
Then wrap the two functions and set the range for them:
```Python
# get term link list
parallelProcess(requestSearchResults,range(0,maxNumPage*termsPerPage)[0::termsPerPage])
    
# get terms and explanations
parallelProcess(parseTermPage,termlinklist)
```

Although my laptop only has 4 cores, the process has been speed up for much more than 4 times: the total fetching time has been lowered down to less than 20min. The reason is that there are always some links will be much slower to fetch. If there is only one thread, every fetching task will be blocked by those links; however with 4 threads, there will be fast lanes for those fast links to go through.






