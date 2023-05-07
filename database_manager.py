from sleeper_wrapper import Players
import psycopg2
import psycopg2.sql
from psycopg2.extras import Json, execute_values
from psycopg2.extensions import AsIs, adapt




class FFDBManager(Players):
    def __init__(self):
        super().__init__()
        ####################
        # MAKE DB CONNECTION
        ####################



    def make_db_connection(self):
        pass

    def make_create_table_statement(self):

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
                print(cursor.mogrify(create_table_stmt))
        return create_table_stmt

                # cursor.execute(create_table_stmt)

        # return create_table_stmt

    def make_create_table_statement_json(self):

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
                print(cursor.mogrify(create_table_stmt))
        return create_table_stmt

                # cursor.execute(create_table_stmt)

        # return create_table_stmt
    def mogrify(self, statement):
        conn = psycopg2.connect(
            database='players',
            user='postgres',
            password='docker',
            port='5432',
            host='localhost')
        with conn:
            with conn.cursor() as cursor:
                print(cursor.mogrify(statement))
                return cursor.mogrify(statement)

    def build_insert_statement(self):
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
                    values = [Json(p[c]) if type(p[c]) is dict else p[c] if p[c] is not None else None for c in cols]
                    insert_statement = 'INSERT INTO all_players(%s) VALUES %s'  #  ON CONFLICT (player_id) DO UPDATE SET %s'

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
# GET DATAFRAME and JSON
####################
"""
ff = FFDBManager()
ff.make_create_table_statement()

players = Players()
df = players.get_players_df()
all_players = players.all_players

# print(df.head())


"""
conn = psycopg2.connect(
    database='players',
    user='postgres',
    password='docker',
    port='5432',
    host='localhost')
"""





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