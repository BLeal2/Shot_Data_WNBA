import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import re
from alive_progress import alive_bar


game_ids = pd.read_csv("WNBA_2016_2022_Games.csv")["WNBA GameID"].astype(int).unique()
shots_dataset = pd.DataFrame({"GAME_ID": [], 
                              "TEAM_ID": [], "TEAM_NAME": [], 
                              "PLAYER_ID": [], "PLAYER_NAME": [],				
                              "EVENT_TYPE": [], "SHOT_TYPE": [],
                              "ZONE_NAME": [],
                              "LOC_X": [], "LOC_Y": [], 
                              "QUARTER": [], "MINS_LEFT": [], "SECS_LEFT": []})
error_log = pd.DataFrame({"GAME_ID":[]})

team_id, team_name, player_id, player_name, event_type, shot_type = None, None, None, None, None, None
zone_name, loc_x, loc_y, quarter, mins_left, secs_left = None, None, None, None, None, None


with alive_bar(len(game_ids)) as bar:
    for game in game_ids:

        n_tries = 0

        # Create a retry mechanism (with a max limit of 5 tries) to access the website
        while n_tries < 5:

            try:
                # Create a webdriver instance for each game
                webdriver_shot = webdriver.Chrome()
                webdriver_shot.get(f'https://stats.wnba.com/game/{game}/shotchart/?sct=plot')
                
                time.sleep(2)
                shots = webdriver_shot.find_elements(By.CLASS_NAME, "shotplot__shot")
                
                for shot in shots:

                    team_id, team_name = shot.get_attribute("data-team-id"), shot.get_attribute("data-team-name")
                    player_id, player_name = shot.get_attribute("data-player-id"), shot.get_attribute("data-player-name")

                    event_type = "Missed Shot" if shot.get_attribute("data-madeflag") == "false" else "Made Shot"
                    shot_type = shot.get_attribute("data-shot-type")

                    loc_x, loc_y = shot.get_attribute("data-x"), shot.get_attribute("data-y")
                    quarter = shot.get_attribute("data-period")

                    clock_time = shot.get_attribute("data-clock")
                    mins_left, secs_left = clock_time.split(":")[0], clock_time.split(":")[1]

                    text_description = re.search(r'<title>(.*?)</title>', str(shot.get_attribute('innerHTML'))).group(1)
                    zone_name = text_description.split(" - ")[-1]

                    shots_dataset.loc[len(shots_dataset)] = [game, team_id, team_name, player_id, player_name, 
                                                            event_type, shot_type, zone_name, loc_x, 
                                                            loc_y, quarter, mins_left, secs_left]
        
                webdriver_shot.quit()

                break

            except:
                n_tries += 1
                time.sleep(2)


        # Add the games that returned the error for manual inspection
        if n_tries == 5:
                error_log.loc[len(error_log)] = game

        team_id, team_name, player_id, player_name, event_type, shot_type = None, None, None, None, None, None
        zone_name, loc_x, loc_y, quarter, mins_left, secs_left = None, None, None, None, None, None
        
        bar()


error_log.to_csv("Errors_WNBAShots_2016_2022_PT1.csv", index=False)
shots_dataset.to_csv("WNBAShots_2016_2022_PT1.csv", index=False)             