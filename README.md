# Python-Crawling

It is my first time to do the crawling on Python. Recently a friend asked if I can get all of the terms and their explanations from lexicon.ft.com. After taking a look at its website I found that the term pages are indexed alphabetically. Seems like this is not a hard task.

##Initial plan:
After checking the url of the term pages, the followings are found:
* Each index page has the url = http://lexicon.ft.com/Search?letter=A
* Each term page has the url = http://lexicon.ft.com/Term?term=A-H1N1

So the implementation is
####1. fetch each index page (A-Z) using requests, and find and store the urls for each term via bueatiful soup
After investigating the source code of the index page, we can notice that all of the term urls are stored in `<a href="Term?term=***">`
, so just loop all hrefs and find the ones with "Term?term=".
####2. fetch each term page using request, and find and store the term and the explanation via bueatiful soup
In its souce code, all terms are stored in `<div class="moreItemsHeader">` and explanation is stored in `<div class="definition">`, so just get element.text via bueatiful soup (do not use .string). 
####3. The result list is saved to csv file. 
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









