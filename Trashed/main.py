# main Python script
from flask import Flask, jsonify, render_template
from fantasy_football import FantasyFootball
from pathlib import Path
import os

app = Flask(__name__)

# create a new instance of FantasyFootball and generate the HTML table
filepath = Path('my-app/data/players.json')
ff = FantasyFootball(filepath)
ff.create_dataframe()
html_table = ff.generate_html_table()

@app.route('/')
def index():
    print(os.getcwd())
    return render_template('my-app/templates/index.html', html_table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
