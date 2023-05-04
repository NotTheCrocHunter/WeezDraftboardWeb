# main Python script
from flask import Flask, jsonify, render_template
from pathlib import Path
import os
from draftboard_brain import DraftBoardBrain

app = Flask(__name__)

# create a new instance of FantasyFootball and generate the HTML table
filepath = Path('data/players.json')
ff = DraftBoardBrain(filepath)
ff.create_dataframe()
html_table = ff.generate_html_table()

@app.route('/')
def index():
    return render_template('index.html', html_table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
