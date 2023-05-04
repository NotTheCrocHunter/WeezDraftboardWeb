from sleeper_wrapper import Players
import psycopg2


""" 
# connection establishment version 1
conn = psycopg2.connect(
   database="postgres",
    user='postgres',
    password='postgrespw',
    host='localhost',
    port='32768'
)
 """

conn = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='docker',
    port='5432',
    host='localhost')

conn.autocommit = True
postgres_string = 'postgres://postgres:postgrespw@localhost:32768'
docker_string = 'docker run --name fantasy-postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres'
# Creating a cursor object
cursor = conn.cursor()
 
# query to create a database
sql = ''' CREATE database players ''';
# need sql query to create the table if it doesn't exist and add the players to it


# executing above query
cursor.execute(sql)
print("Database has been created successfully !!");
 
# Closing the connection
conn.close()

# players = Players()
# df = players.get_players_df()
# print(df[df['status'] == 'Active'])