# virtual-betting
W4111 web-application project *CURRENTLY HOSTED AT http://35.231.52.41:8111/*

This repository contains the code used to develop our virtual sports betting web application. 

This site will display all NBA games for the upcoming day, and when a user has logged in, 
will let them place wagers (virtual money) on the game outcomes. Overnight, the game results
will be fetched, and the user profile will be updated accordingly. 

The betting lines that the users can bet on are updated hourly, and become unavailable once
the game starts. Only the single best betting line from the industry's top 10 sportsbooks is
presented. Users can also click on the game page for each match-up to get a few basic
statistical insights about the game. 

### Repository Overview
`Data/` contains the historic data (new data scraped daily is not appended to these CSVs).

`Packages/` contains the two primary packages used: `scraping` and `db_inserter`.

`Project_Parts/` contains the database's ER diagram and SQL schema, as well as several miscellaneous documents.

`Webpage/` contains the code used to construct the website (using Flask and Jinja in Python).



### Screenshots

![Alt text](Screenshots/Homepage.png?raw=true "Homepage")

![Alt text](Screenshots/Gamepage.png?raw=true "Gamepage")

![Alt text](Screenshots/Profile.png?raw=true "Profile")

