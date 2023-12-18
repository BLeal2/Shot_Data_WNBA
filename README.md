# Shot by Shot Data in WNBA
This github repository uses the Selenium Python library to scrape shot by shot data of WNBA regular season games, spanning from 2017 to 2022.

### Instructions
This directory should be read by starting with the "Game Data" folder. This folder contains the code to extract the characteristics of each regular season game, from 2016 to 2022, available in the WNBA website. The code can be found in the jupyter notebook "Scrapping Game Data", while the results can be found in the "WNBA_2016_2022_shots" csv file.

After gathering all game information, one should look into each shot attempted in the games extracted previously. To extract information about the location, team, player, event type, shot type, zone and time, in which the shot was attempted, the "Scrapping Shot Data PT1 - Shotcharts" python file was created. Additionally, in order to get a similar dataset to the NBA one, the "Scrapping Shot Data PT2 - PlaybyPlay" was created to extract action type and distance from the basket. The results of the shot data scrapping for each year can be found under the folder "WNBAShots_TESTED".

This directory is composed by two jupyter notebook files and it should be used to merge together all the information gathered previously, for both NBA and WNBA.
