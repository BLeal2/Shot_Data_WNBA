import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import time
from alive_progress import alive_bar


shots_shotchart = pd.read_csv("WNBAShots_2016_2022_PT1.csv")
unique_games = list(shots_shotchart["GAME_ID"].unique())


shots_playbyplay = pd.DataFrame({"GAME_ID":[], "time":[], "player":[], "EVENT_TYPE":[], "SHOT_TYPE":[], "DISTANCE":[], "ACTION_TYPE":[], "PLAY_DESCRIPTION":[]})
error_log = pd.DataFrame({"GAME_ID":[]})


with alive_bar(len(unique_games)) as bar:
    for game in unique_games:

        n_tries = 0

        # Create a retry mechanism (with a max limit of 5 tries) to access the website
        while n_tries < 5:

            try:
                webdriver_shot = webdriver.Chrome()
                webdriver_shot.get(f'https://stats.wnba.com/game/{game}/playbyplay/')

                time.sleep(2)

                # Get each row in play by play table
                all_plays = webdriver_shot.find_element(By.CLASS_NAME, "boxscore-pbp__inner"
                                                        ).find_element(By.TAG_NAME, "tbody"
                                                                    ).find_elements(By.TAG_NAME, "tr")
                # Get auxiliary variables
                quarter = 0

                for play in all_plays:
                    
                    # For row (play) in the table, we will find every column
                    all_cols = play.find_elements(By.TAG_NAME, "td")


                    # If there is only one column (colspan = 3), this "play" means there was a change of quarter and we should move to another play
                    if len(all_cols) == 1:
                        quarter += 1
                        continue


                    play_description = all_cols[0].text + all_cols[2].text
                    

                    # If free throw, move to another play
                    if "Free Throw" in play_description:
                        continue
                

                    # Play with successful shot
                    elif play.get_attribute("class") == "scoring":
                        
                        # Move to another play if it is the end of the quarter (info about scores)
                        if re.search('^Go to', play_description):
                            continue
                        
                        # Check if the play description has distance feet (XX')
                        if re.search(r'\d+\'', play_description):  
                
                            distance_feet = re.search(r'\d+\'', play_description).group()
                            # Get the action type which is between the distance feet and (XX PTS)
                            action_type = re.search(r'\d+\'\s(.*?)\s\(\d+\sPTS\)', play_description).group(1)
                            # Get the player name which is before the distance in feet
                            player_name = re.search(r'^(.*?)\s\d+\'', play_description).group(1)

                        # If there is no information on the distance feet, get action type differently
                        else:
                            distance_feet = None

                            # Check if the name of the player is composed by two words (the first one being a letter followed by a dot)
                            if re.search(r'^([A-Z]\. \w+)', play_description):
                                # Action type is between the first word (player) and (XX PTS)
                                action_type = re.search(r'\b\w+\b\s(.*?)\s\(\d+\sPTS\)', play_description).group(1)
                                # Get the player name composed by the first two words
                                player_name = re.search(r'^([A-Z]\. \w+)', play_description).group(1)

                            else:
                                # Action type is between the first word (player) and (XX PTS)
                                action_type = re.search(r'\b\w+\b\s(.*?)\s\(\d+\sPTS\)', play_description).group(1)
                                # Player name is the first word of the string
                                player_name = play_description.split()[0]

                        # Variables to help merge the dataframes
                        play_time = str(quarter) + "-" + all_cols[1].text[:4]
                        event_type = "Made Shot"
                        play_string = play_description


                    # Play with missed shots
                    elif "MISS" in play_description:

                        if "MISS" in all_cols[0].text:
                            play_description = all_cols[0].text
                        else:
                            play_description = all_cols[2].text

                        # Check if the play description has distance feet (XX')
                        if re.search(r'\d+\'', play_description):  
                
                            distance_feet = re.search(r'\d+\'', play_description).group()
                            # Get the action type which is after distance feet
                            action_type = re.search(r'\d+\s*\'\s*(.*)', play_description).group(1)
                            # Get the player name which is between the 'MISS' string and distance feet
                            player_name = re.search(r'MISS\s(.*?)\s\d+\'', play_description).group(1)

                        # If there is no information on the distance feet, get action type differently
                        else:
                            distance_feet = None

                            # Check if the name of the player is composed by two words (the first one being a letter followed by a dot)
                            if re.search(r'MISS [A-Z]\. \w+', play_description):
                                # Action type is after the first three words (MISS and the two words of a player's name)
                                action_type = ' '.join(play_description.split()[3:])
                                # Get the player name composed by the two words which follow the word "MISS"
                                player_name = re.search(r'^MISS ([A-Z]\.) (\w+)', play_description).group(1) + " " + \
                                    re.search(r'^MISS ([A-Z]\.) (\w+)', play_description).group(2)
                            
                            else:
                                # Action type is after the first two words (MISS and the player's name)
                                action_type = ' '.join(play_description.split()[2:])
                                # Get the player name composed by the second word of the string
                                player_name = play_description.split()[1]

                        # Variables to help merge the dataframes
                        play_time = str(quarter) + "-" + all_cols[1].text[:4]
                        event_type = "Missed Shot"
                        play_string = play_description


                    else:
                        continue


                    # Remove the "3PT" of the string if applicable
                    if "3PT" in action_type:
                        shot_type = "3PT Field Goal"
                        action_type = action_type.replace("3PT ", "")
                    else:
                        shot_type = "2PT Field Goal"
                    
                    # Save results to dataframe
                    shots_playbyplay.loc[len(shots_playbyplay)] = [game, play_time, player_name, event_type, shot_type, distance_feet, action_type, play_string]

                break

            except:
                n_tries += 1
                time.sleep(2)

        # Add the games that returned the error for manual inspection
        if n_tries == 5:
                error_log.loc[len(error_log)] = game

        play_time, player_name, event_type, shot_type, distance_feet, action_type, play_string = None, None, None, None, None, None, None

        bar()


error_log.to_csv("Errors_WNBAShots_2016_2022_PT2.csv", index=False)
shots_playbyplay.to_csv("WNBAShots_2016_2022_PT2.csv", index=False)
