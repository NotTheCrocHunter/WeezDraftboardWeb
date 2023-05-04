import pandas as pd
import json
from pathlib import Path
import os


class FantasyFootball:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
    
    def read_json(self):
        with open(self.filepath, 'r') as f:
            # read the JSON file and replace null with None
            data = f.read().replace('null', 'null')
            # parse the JSON string and convert null to None
            json_data = json.loads(data, parse_constant=lambda x: None if x == 'null' else x)
            # access the players list of dicts
            json_data = json_data['players']

        return json_data
    
    def create_dataframe(self):
        data = self.read_json()
        self.df = pd.DataFrame(data)
    
    def print_dataframe(self):
        if self.df is not None:
            print(self.df)
        else:
            print("DataFrame is empty. Please create DataFrame first using 'create_dataframe()' method.")

    def generate_html_table(self):
        num_cols = 12
        html = '<table>\n'
        for i in range(num_cols):
            html += '  <col>\n'
        html += '  <tbody>\n'
        for index, row in self.df.iterrows():
            html += '    <tr>\n'
            html += f'      <td>{row["name"]}</td>\n'
            html += f'      <td>{row["team"]}</td>\n'
            html += f'      <td>{row["position"]}</td>\n'
            for j in range(num_cols - 3):
                html += '      <td></td>\n'
            html += '    </tr>\n'
        html += '  </tbody>\n'
        html += '</table>'
        return html


"""
filepath = Path('my-app/data/players.json')
print(os.getcwd())
ff = FantasyFootball(filepath)
ff.create_dataframe()
ff.print_dataframe()
ff.generate_html_table()

"""