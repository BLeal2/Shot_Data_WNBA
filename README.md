## Shot by Shot Data in WNBA
This github repository uses the Selenium Python library to scrape shot by shot data of WNBA regular season games, spanning from 2017 to 2022.

### Instructions
Due to the extensive amount of time the code takes to run, the repository is divided into four parts:

- The first python file to run is "Scapping Game Data - Game Calendar", which contains the code to extract the characteristics of each regular season game, from 2016 to 2022, available in the WNBA website. 

- Following this, to extract information about the shot by shot data regarding location, team, player, event type, shot type, zone and time, the "Scrapping Shot Data PT1 - Shotcharts" python file should be used.
  
- The "Scrapping Shot Data PT2 - PlaybyPlay" was created to extract action type and distance from the basket.

- Finally, the jupyter notebook "Merging Extracted Data" should be used to merge together all the information gathered previously.
