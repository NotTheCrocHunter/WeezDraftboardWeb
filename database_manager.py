from sleeper_wrapper import Players
import psycopg2
import psycopg2.sql
from psycopg2.extras import Json, execute_values
from psycopg2.extensions import AsIs, adapt
import json

class FFDBManager(Players):
    def __init__(self):
        super().__init__()

    def create_all_players_table(self):

        #####################################
        # BUILD THE CREATE TABLE statement
        #####################################
        # make db connection
        conn = psycopg2.connect(
            database='players',
            user='postgres',
            password='docker',
            port='5432',
            host='localhost')
        # Create the all_players table
        table_name = 'all_players_test'
        columns = []
        s = self.players_df.dtypes
        print(s)
        for column_name, dtype in s.items():
            print(dtype)
            if column_name == 'player_id':
                columns.append(f"{column_name} VARCHAR(255) PRIMARY KEY")
            elif column_name in ['rotoworld_id', 'pandascore_id']:
                columns.append(f"{column_name} VARCHAR(255) NULL")
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

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(create_table_stmt)
                # print(cursor.mogrify(create_table_stmt))
        return create_table_stmt

    def insert_all_players_records(self):
        error_count = 0
        success_count = 0
        conn = psycopg2.connect(
            database='players',
            user='postgres',
            password='docker',
            port='5432',
            host='localhost')
        with conn:
            with conn.cursor() as cursor:
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
                            update_values.append(f"{c} = '{p[c]}'")
                        elif p[c] is None:
                            values.append(None)
                            update_values.append(f"{c} = {None}")

                    # values = [Json(p[c]) if type(p[c]) is dict else p[c] if p[c] is not None else None for c in cols]
                    insert_statement = 'INSERT INTO all_players_test(%s) VALUES %s ' \
                                       'ON CONFLICT (player_id) DO UPDATE SET %s'
                    print(cursor.mogrify(insert_statement, (AsIs(", ".join(cols)), tuple(values), AsIs(", ".join(update_values)))))
                    cursor.execute(insert_statement, (AsIs(", ".join(cols)), tuple(values), AsIs(", ".join(update_values))))
                    cursor.execute(insert_statement, (AsIs(", ".join(cols)), tuple(values), tuple(update_values)))

                    try:
                        cursor.execute(insert_statement, (AsIs(", ".join(cols)), tuple(values)))
                        success_count += 1
                    except Exception as e:
                        print(f"error {e} on player {player}")
                        error_count += 1

                print(f"error count: {error_count}")
                print(f"Success count: {success_count}")


"""
####################
# GET DATAFRAME
####################
"""
ff = FFDBManager()
ff.create_all_players_table()
ff.insert_all_players_records()


players = Players()
all_players = players.all_players


"""
# Create temporary table in Postgres
cursor.execute("CREATE TEMPORARY TABLE temp_all_players (LIKE all_players)")



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


"""


# postgres_string = 'postgres://postgres:postgrespw@localhost:32768'
# docker_string = 'docker run --name fantasy-postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres'