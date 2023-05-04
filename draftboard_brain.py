import pandas as pd
import json
from pathlib import Path
import os
import numpy as np
import math

class DraftBoardBrain:
    def __init__(self, filepath, cols=12):
        self.filepath = filepath
        self.df = None
        self.dbdf = None
        self.cols = cols

    def read_json(self):
        with open(self.filepath, 'r') as f:
            # read the JSON file and replace null with None
            data = f.read().replace('null', 'null')
            # parse the JSON string and convert null to None
            json_data = json.loads(data, parse_constant=lambda x: None if x == 'null' else x)
            # access the players list of dicts
            json_data = json_data['players']

        return json_data
    

    def create_draftboard_dataframe(self):
        
        data = self.read_json()
        max_cols = self.cols
        max_rows = math.ceil(len(data)/max_cols)
        max_cells = max_cols * max_rows
        empty_cells = max_cells - len(data)
        new_shape = (max_rows, max_cols)

        # remove unnecessary keys from players
        player_list = [{'name': d['name'], 'team': d['team'], 'position': d['position'], 'class': d['position'].lower()} for d in data]

        for x in range(empty_cells):
            player_list.append({'name': '', 'team': '', 'position': '', 'class': ''})

        arr = np.array(player_list)
        arr = np.reshape(arr, new_shape)
        # snake order
        arr[1::2, :] = arr[1::2, ::-1]

        
        self.dbdf = arr

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
        rows = self.df['name_team_pos'].values.tolist()
        player_positions = self.df['position'].tolist()
        num_rows = len(rows)
        num_open_cells = num_cols - num_rows % num_cols
        rows += [''] * num_open_cells
        for i in range(0, len(rows), num_cols):
            html += '    <tr>\n'
            for j in range(num_cols):
                cell_value = rows[i+j] if i+j < num_rows else ''
                cell_class = player_positions[i+j] if i+j < num_rows else ''
                html += f'      <td class={cell_class.lower()}>{cell_value}</td>\n'
            html += '    </tr>\n'
        html += '  </tbody>\n'
        html += '</table>'
        return html

    def generate_html_table_draftboard(self):

        self.create_draftboard_dataframe()

        arr = self.dbdf
        html = '<table>\n'
        for row in arr:
            html += '  <tr>\n'
            for cell in row:
                name = cell['name']
                team = cell['team']
                position = cell['position']
                cell_class = cell['class']
                html += f'    <td class="{cell_class}">'
                html += f'<div class="name">{name}</div>'
                html += f'<div class="team-pos">{team} {position}</div>'
                html += '</td>\n'
            html += '  </tr>\n'
        html += '</table>'
        return html




filepath = Path('data/players.json')
print(os.getcwd())
ff = DraftBoardBrain(filepath)
ff.create_dataframe()
ff.create_draftboard_dataframe()
# print(ff.dbdf)
print(ff.generate_html_table_draftboard())
# ff.print_dataframe()   
# print(ff.generate_html_table())

