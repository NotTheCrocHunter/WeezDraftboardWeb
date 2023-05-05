from sleeper_wrapper import Players
import psycopg2



####################
# GET DATAFRAME
####################

players = Players()
df = players.get_players_df()
print(df.head())

####################
# MAKE DB CONNECTION
####################

conn = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='docker',
    port='5432',
    host='localhost')

conn.autocommit = True

# Creating a cursor object
cursor = conn.cursor()

#####################################
# BUILD THE CREATE TABLE statement
#####################################

# Create the all_players table
table_name = 'all_players'
columns = []
s = df.dtypes
print(s)
for column_name, dtype in s.items():
    print(dtype)
    if column_name == 'player_id':
        columns.append(f"{column_name} VARCHAR(255) PRIMARY KEY")
    elif column_name in ['rotoworld_id', 'pandascore_id']:
        columns.append(f"{column_name} VARCHAR(255) NULL,")
    elif column_name == 'fantasy_positions':
        columns.append(f"{column_name} text[] NULL,")
    elif dtype == 'int64':
        columns.append(f"{column_name} INT NULL,")
    elif dtype == 'float64':
        columns.append(f"{column_name} VARCHAR(255) NULL,")
    elif dtype == 'datetime64[ns]':
        columns.append(f"{column_name} TIMESTAMP NULL,")

    else:
        columns.append(f"{column_name} VARCHAR(255) NULL,")

column_str = '\n'.join(columns)
create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str});"
print(create_table_stmt)
cursor.execute(create_table_stmt)


# Create temporary table in Postgres
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





# postgres_string = 'postgres://postgres:postgrespw@localhost:32768'
# docker_string = 'docker run --name fantasy-postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres'