from .base_api import BaseApi
import json
from pathlib import Path
import pandas as pd
from datetime import datetime



class Players(BaseApi):
    def __init__(self):
        self.dir_path = Path('data/players')
        self.file_path = Path('data/players/all_players.json')
        self.all_players = self.get_all_players()
        self.players_df = self.get_players_df()

    def get_players_df(self, position_list=['QB', 'RB', 'WR', 'TE', 'K', 'DEF']):
        df = pd.DataFrame.from_dict(self.get_all_players(), orient="index")

        return df[df.position.isin(position_list)]

    def get_all_players(self):
        TODAY = datetime.today().strftime('%Y-%m-%d')

        if self.file_path.exists() and self.dir_path.exists():

            print("Players Call: Local path and file exists, reading local version")

            with open(self.file_path) as json_file:
                players_dict = json.load(json_file)

            all_players = players_dict['players']
            last_accessed = players_dict['accessed']

            if last_accessed == TODAY:
                print('Date of players is today.')
                return all_players
            else:
                print('Date of players is old.  Making new players call')
                pass
        else:

            print("Players Call: local path and file not found, making API call")
            # make the path
            self.dir_path.mkdir(parents=True, exist_ok=True)

        # after path creation for filenotfound, go and make the API call.
        # load the response
        players_response = self._call("https://api.sleeper.app/v1/players/nfl")
        # make the dict and get the players dict
        players_dict = {'accessed': TODAY, 'players': players_response}
        all_players = players_dict['players']
        # save the dict
        with open(self.file_path, 'w') as outfile:
            json.dump(players_dict, outfile, indent=4)

        return all_players


    def get_trending_players(self, sport, add_drop, hours=24, limit=25):
        return self._call(
            f"https://api.sleeper.app/v1/players/{sport}/trending/{add_drop}?lookback_hours={hours}&limit={limit}")

    def check_cache(self):
        print(f"Dir {self.dir_path} exists:  {self.dir_path.exists()}")
        print(f"File {self.file_path} exists: {self.file_path.exists()}")

    def delete_cache(self):
        self.file_path.unlink()
