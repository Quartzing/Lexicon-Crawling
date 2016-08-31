# Python-Crawling

It is my first time to do the crawling on Python. Recently a friend asked if I can get all of the terms and their explanations from lexicon.ft.com. After taking a look at its website I found that the term pages are indexed alphabetically. Seems like this is not a hard task.

##Initial plan:
After checking the url of the term pages, the followings are found:
####1. Each index page has the url = http://lexicon.ft.com/Search?letter=A
####2. Each term page has the url = http://lexicon.ft.com/Term?term=A-H1N1

So the implementation is
####1. fetch each index page (A-Z) using requests, and find and store the urls for each term via bueatiful soup
After investigating the source code of the index page, I noticed that all of the term urls are stored in `<a href="Term?term=***">`
, so just loop all hrefs and find the ones with "Term?term=".
####2. fetch each term page using request, and find and store the term and the explanation via bueatiful soup
In its souce code, all terms are stored in `<div class="moreItemsHeader">` and explanation is stored in `<div class="definition">`, so just get element.text via bueatiful soup (do not use .string). 
####3. The result list is saved to csv file. 

This formed the initial version. After running this version, several problems are captured:
####encoding error
special characters like \xa0 \xa3 cannot be saved to the file
####most of the terms are missed
Only 10 terms are shown on each index page










