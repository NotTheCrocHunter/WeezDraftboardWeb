from sleeper_wrapper import Players
import psycopg2
import psycopg2.sql
from psycopg2.extras import Json, execute_values
from psycopg2.extensions import AsIs, adapt
import json
import logging
import os
import django
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
# from api.models import Player

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dotenv_path = os.path.join(os.path.dirname(__file__), 'WeezDraftboardWeb', '.env')
load_dotenv(dotenv_path)
postgres_pw = os.getenv('POSTGRES_PASSWORD')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeezDraftboardWeb.settings')
# django.setup()


class FFDBManager(Players):
    def __init__(self):
        # init the Players class
        super().__init__()
        # Connect to PostgreSQL server
        # add pw to env
        self.conn = psycopg2.connect(database="postgres", user="postgres", password=postgres_pw, host="localhost",
                                     port="5432")
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        # Check DB Schema# Create database "weez_fantasy_nfl" if it doesn't exist
        self.check_db_schema()
        
        # Insert/update for adding player records
        # self.insert_all_players_records()

    def check_db_schema(self):
        self.cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'weez_fantasy_nfl'")
        exists = self.cursor.fetchone()
        if not exists:
            print('Creating weez_fantasy_nfl database')
            self.cursor.execute("CREATE DATABASE weez_fantasy_nfl")
        else:
            print('weez_fantasy_nfl database exists, connecting now')
        # Connect to "weez_fantasy_nfl" database
        self.conn = psycopg2.connect(database="weez_fantasy_nfl", user="postgres", password=postgres_pw,
                                        host="localhost", port="5432")
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        # Create "all_players" table if it doesn't exist
        print('Checking if all_players table exists')
        self.cursor.execute("SELECT to_regclass('public.all_players')")
        exists = self.cursor.fetchone()[0]
        if not exists:
            print('all_players table does not exist')
            print(self.cursor.mogrify(self.create_all_players_table()))
            self.cursor.execute(self.create_all_players_table())
        else:
            print('All players table exists')

    def create_all_players_table(self):

        #####################################
        # BUILD THE CREATE TABLE statement
        #####################################

        print('starting create_all_players_table')

        # Create the all_players table
        table_name = 'all_players'
        columns = []
        s = self.players_df.dtypes
        # print(s)
        id_keys = [k for k in s.keys() if k[-2:] == "id"]
        for column_name, dtype in s.items():
            # print(dtype)
            if column_name == 'player_id':
                columns.append(f"{column_name} VARCHAR(255) PRIMARY KEY")
            elif column_name in id_keys:
                columns.append(f"{column_name} VARCHAR(255) NULL")
            elif column_name == 'search_rank':
                columns.append(f"{column_name} INT NULL")
            elif column_name == 'fantasy_positions':
                columns.append(f"{column_name} text[] NULL")
            elif column_name == 'metadata':
                columns.append(f"{column_name} JSONB NULL")
            elif dtype == 'int64':
                columns.append(f"{column_name} INT NULL")
            elif dtype == 'float64':
                columns.append(f"{column_name} VARCHAR(255) NULL")
            elif dtype == 'datetime64[ns]':
                columns.append(f"{column_name} TIMESTAMP NULL")
            else:
                columns.append(f"{column_name} VARCHAR(255) NULL")

        column_str = ', '.join(columns)
        create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str});"

        return create_table_stmt

    def select_wrs(self):
        pass
    
    def see_all_players(self):
        # view all ff relevant players from all players where position is in ['QB', 'RB', 'WR', 'TE]
        self.cursor.execute("SELECT * FROM all_players")
        
        return self.cursor.fetchall()
    
    def see_relevant_players(self):
        # view all ff relevant players from all players where position is in ['QB', 'RB', 'WR', 'TE]
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'PK', 'DEF']
        query = "SELECT * FROM all_players WHERE position IN %s"
        self.cursor.execute(query, (tuple(positions), )) # LIMIT 2")
        return self.cursor.fetchall()
    
    def select_db_for_matching(self):
        # view all ff relevant players from all players only grabbing the fields for matching, where position is in ['QB', 'RB', 'WR', 'TE]
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'PK', 'DEF']
        query = "SELECT full_name, position, team, player_id FROM all_players WHERE position IN %s"
        self.cursor.execute(query, (tuple(positions), )) # LIMIT 2")
        cols = [desc[0] for desc in self.cursor.description]
        return cols, self.cursor.fetchall()

    def get_all_columns(self):
        self.cursor.execute("SELECT * FROM all_players")
        cols = [desc[0] for desc in self.cursor.description]
        return cols
    
    def insert_all_players_records(self):
        print('starting all player records insert')
        error_count = 0
        success_count = 0

        for player in self.all_players:
            p = self.all_players[player]
            cols = p.keys()
            values = []
            update_values = []
            for c in cols:
                if type(p[c]) is dict:
                    values.append(Json(p[c]))
                    update_values.append(f"{c} = {Json(p[c])}")
                elif p[c] is not None:
                    values.append(p[c])
                    if p[c] != '':
                        update_values.append(f"{c} = '{p[c]}'")
                elif p[c] is None:
                    values.append(None)
                    # skip the update_values here for nulls/nones

            # values = [Json(p[c]) if type(p[c]) is dict else p[c] if p[c] is not None else None for c in cols]
            # This is the old update statement.  We are skipping for now
            # TODO add DO UPDATE SET %s to insert statement
            # old update_values join  AsIs(", ".join(update_values))
            insert_statement = 'INSERT INTO all_players(%s) VALUES %s ' \
                                'ON CONFLICT (player_id) DO NOTHING'
            # print(cursor.mogrify(insert_statement, (AsIs(", ".join(cols)), tuple(values),)))
            # cursor.execute(insert_statement, (AsIs(", ".join(cols)), tuple(values), tuple(update_values)))
            # AsIs(", ".join(update_values))

            try:
                self.cursor.execute(insert_statement, (AsIs(", ".join(cols)), tuple(values)))
                success_count += 1
            except Exception as e:
                print(f"error {e} on player {player}")
                error_count += 1

        print(f"error count: {error_count}")
        print(f"Success count: {success_count} ")

    def insert_all_players_records_new(self):
        print('starting all player records insert')
        error_count = 0
        success_count = 0

        # Extract the column names from the first player
        first_player = next(iter(self.all_players.values()))
        cols = list(first_player.keys())

        # Extract the data for all players
        data = []
        for player in self.all_players.values():
            row = []
            print(player)
            for col in cols:
                if type(player[col]) is dict:
                    row.append(Json(player[col]))
                else:
                    row.append(player[col])

            data.append(row)
            print(row)
        # Construct the INSERT statement
        insert_statement = 'INSERT INTO all_players (%s) VALUES %%s ON CONFLICT (player_id) DO NOTHING' % ", ".join(
            cols)
        print(self.cursor.mogrify(insert_statement))
        # Execute the INSERT statement with execute_values
        try:
            execute_values(self.cursor, insert_statement, data)
            success_count = len(data)
        except Exception as e:
            print(f"error {e} on players insert")
            error_count = len(data)

        print(f"error count: {error_count}")
        print(f"Success count: {success_count} ")

    def check_db_schema_new(self):
        if not self._database_exists("weez_fantasy_nfl"):
            logger.info("Creating weez_fantasy_nfl database")
            self._execute("CREATE DATABASE weez_fantasy_nfl")

        self.conn = psycopg2.connect(
            database="weez_fantasy_nfl",
            user="postgres",
            password="docker",
            host="localhost",
            port="5432",
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        self._create_table_if_not_exists("all_players", self._get_all_players_columns())

    def _database_exists(self, database_name):
        self.cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database_name,)
        )
        return bool(self.cursor.fetchone())

    def _create_table_if_not_exists(self, table_name, columns):
        if not self._table_exists(table_name):
            logger.info(f"Creating {table_name} table")
            create_table_stmt = self.create_all_players_table()  # f"CREATE TABLE {table_name} ({columns})"
            self._execute(create_table_stmt)

    def _table_exists(self, table_name):
        self.cursor.execute(f"SELECT to_regclass('public.{table_name}')")
        return bool(self.cursor.fetchone())

    def _get_all_players_columns(self):
        column_types = [
            ("player_id", "VARCHAR(255) PRIMARY KEY"),
            ("search_rank", "INT"),
            ("full_name", "VARCHAR(255)"),
            ("first_name", "VARCHAR(255)"),
            ("last_name", "VARCHAR(255)")]

    def fuzzy_match_sources(self, json_data, db_data):
        # list to store unmatched players
        unmatched_players = []

        # Iterate over the JSON data and update the matching records in the database
        for json_player in json_data:
            match_found = False

            for db_player in db_data[1]:
                # Perform fuzzy matching on Name, Position, and Team values
                name_match = fuzz.partial_ratio(json_player['name'], db_player[0])
                position_match = fuzz.partial_ratio(json_player['position'], db_player[1])
                team_match = fuzz.partial_ratio(json_player['team'], db_player[2])
                sleeper_id = db_player[3]

                # Adjust the matching criteria as per your requirement
                if name_match >= 80 and position_match >= 80 and team_match >= 80: 
                    # Update the matched record in the database
                    print(f'Match with team on {json_player} and {db_player}')
                    match_found = True
                     # UPDATE the all_players table
                    self.cursor.execute("UPDATE all_players SET ffcalc_id = %s, draft_position = %s WHERE player_id = %s", (json_player['ffcalc_id'], json_player['draft_position'], db_player[3]))
                    # add the sleeper id to the json_data 
                    json_player['sleeper_id'] = sleeper_id
                    break

                elif name_match >= 78 and position_match >= 80:
                    # Update the matched record in the database
                    print(f'Match with no team on {json_player} and {db_player}')
                    match_found = True
                     # UPDATE DB
                    # self.cursor.execute("UPDATE all_players SET ffcalc_id = %s, draft_position = %s WHERE player_id = %s", (json_player['ffcalc_id'], json_player['draft_position'], db_player[3]))
                    # add the sleeper id to the json_data 
                    json_player['sleeper_id'] = sleeper_id
                    break

                elif json_player['position'] == 'DEF':
                    print('Defense found.')
                    # FIND DEFENSES in DB
                   
                    match_found = True
                    # UPDATE DB
                    # self.cursor.execute("UPDATE all_players SET ffcalc_id = %s, draft_position = %s WHERE player_id = %s", 
                    #                     (json_player['ffcalc_id'], json_player['draft_position'], json_player['position']))
                    json_player['sleeper_id'] = json_player['team']
                    break
         
            if not match_found:
                unmatched_players.append(json_player)
                

        print(unmatched_players)
        return json_data

    def update_adp_from_json(self):
        """
        Original method attempting to load ADP data into the database.  
        Now I'm using it as a springboard to create the django fixture in create_adp_fixture.
        """
        
        # Load the JSON data
        with open ('data/adp.json') as file:
            adp_data = json.load(file)
        # Load the database matching data
        db_data = self.select_db_for_matching()
        cols = self.get_all_columns()

        # Check if desired columns exist in all_players table and add if not
        if 'ffcalc_id' not in cols:
            # Add ffcalc_id column to the table
            self.cursor.execute("ALTER TABLE all_players ADD COLUMN ffcalc_id CHAR(10)")
        else:
            print('ffcalc in COLS')

        for index, player in enumerate(adp_data['players']):
            player['draft_position'] = index + 1
            player['ffcalc_id'] = player.pop('player_id')
            if player['team'] == 'JAX':
                player['team'] = 'JAC'
            if player['name'] == 'Gabriel Davis':
                player['name'] = 'Gabe Davis'
        matches = self.fuzzy_match_sources(json_data=adp_data['players'], db_data=db_data)
        # print(matches)
        return adp_data['players']
    
    def create_adp_json_to_fixture(self):
        data = self.update_adp_from_json()
        fixture_data = []

        for player in data:
            fixture_data.append({
                "model": "api.adp",
                "fields": {
                    "player_id": player["sleeper_id"],
                    "name": player["name"],
                    "position": player["position"],
                    "team": player["team"],
                    "adp": player["adp"],
                    "bye": player["bye"],
                    "draft_position": player["draft_position"],
                    "ffcalc_id": player["ffcalc_id"],
                    "adp_formatted": player["adp_formatted"],
                    "times_drafted": player["times_drafted"],
                    "high": player["high"],
                    "low": player["low"],
                    "stdev": player["stdev"],
                }
            })
        fixture_file = "WeezDraftboardWeb/api/fixtures/adp_fixtures.json"
        with open(fixture_file, "w") as f:
            json.dump(fixture_data, f, indent=4)
        pass

"""
####################
# GET DATAFRAME and JSON
####################
"""
ff = FFDBManager()
# ff.create_all_players_table()
# ff.insert_all_players_records()
#all_players_postgres = ff.see_relevant_players()
ff.create_adp_json_to_fixture()
print(player_list)
players = Players()
df = players.get_players_df()
all_players = players.all_players

