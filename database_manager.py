from sleeper_wrapper import Players
import psycopg2
import psycopg2.sql
from psycopg2.extras import Json, execute_values
from psycopg2.extensions import AsIs, adapt
import json


class FFDBManager(Players):
    def __init__(self):
        # init the Players class
        super().__init__()
        # Connect to PostgreSQL server
        # add pw to env
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="docker", host="localhost",
                                     port="5432")
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        # Check DB Schema# Create database "weez_fantasy_nfl" if it doesn't exist
        self.check_db_schema()
        
        # Insert/update for adding player records
        self.insert_all_players_records()
    def check_db_schema(self):
        self.cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'weez_fantasy_nfl'")
        exists = self.cursor.fetchone()
        if not exists:
            print('Creating weez_fantasy_nfl database')
            self.cursor.execute("CREATE DATABASE weez_fantasy_nfl")
        else:
            print('weez_fantasy_nfl database exists, connecting now')
        # Connect to "weez_fantasy_nfl" database
        self.conn = psycopg2.connect(database="weez_fantasy_nfl", user="postgres", password="docker",
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
        # make db connection
        conn = psycopg2.connect(
            database='weez_fantasy_nfl',
            user='postgres',
            password='docker',
            port='5432',
            host='localhost')
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

        # with conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute(create_table_stmt)
        #         print(cursor.mogrify(create_table_stmt))
        return create_table_stmt

    def select_wrs(self):
        # make wr search
        pass
    
    def see_all_players(self):
        # view all ff relevant players
        pass

    def insert_all_players_records(self):
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


"""
####################
# GET DATAFRAME and JSON
####################
"""
ff = FFDBManager()
# ff.create_all_players_table()
# ff.insert_all_players_records()
ff.select_wrs()

players = Players()
df = players.get_players_df()
all_players = players.all_players


"""# Create temporary table in Postgres
cursor.execute("CREATE TEMPORARY TABLE temp_all_players (LIKE all_players)")

# Write df to CSV
csv_file = 'temp.csv'
# fix df nulls
df.fillna('None', inplace=True)
# allowed_positions = ['QB', 'TE', 'RB', 'WR', 'DEF', 'K']
# filtered_df = df[df['fantasy_positions'].apply(lambda x: all(pos in allowed_positions for pos in x))]
# write df to csv
df.to_csv(csv_file, index=False)

# Copy the data from the CSV file into the temporary table
with open(csv_file, 'r') as f:
    cursor.copy_from(f, 'temp_all_players', sep=',')

# Insert the data from the temporary table into the main table
cursor.execute("INSERT INTO all_players SELECT * FROM temp_all_players ON CONFLICT DO NOTHING")

# Commit the changes and close the cursor and connection


# query to SELECT from a database
sql = ''' SELECT * from all_players  ''';
# need sql query to create the table if it doesn't exist and add the players to it


# executing above query
cursor.execute(sql)
rows = cursor.fetchall()

# print the results
for row in rows:
    print(row)

print("Database has been created successfully !!");

# Closing the connection
conn.close()

"""# postgres_string = 'postgres://postgres:postgrespw@localhost:32768'
# docker_string = 'docker run --name fantasy-postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres'
