# Python-Crawling

It is my first time to do the crawling on Python. Recently a friend asked if I can get all of the terms and their explanations from lexicon.ft.com. After taking a look at its website I found that the term pages are indexed alphabetically. Seems like this is not a hard task.

Now let get started. 
After checking the url of the term pages, the followings are found:
1. Each index page has the url = http://lexicon.ft.com/Search?letter=A
2. Each term page has the url = http://lexicon.ft.com/Term?term=A-H1N1

So the plan is to 
1. fetch each index page (A-Z) using requests, and find and store the urls for each term via bueatiful soup
2. fetch each term page using request, and find and store the term and the explanation via bueatiful soup


