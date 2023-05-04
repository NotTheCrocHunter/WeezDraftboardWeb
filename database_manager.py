from sleeper_wrapper import Players
import psycopg2
 
# connection establishment
conn = psycopg2.connect(
   database="postgres",
    user='postgres',
    password='postgrespw',
    host='localhost',
    port= '32768'
)
 
conn.autocommit = True
postgres_string = 'postgres://postgres:postgrespw@localhost:32768' 
# Creating a cursor object
cursor = conn.cursor()
 
# query to create a database
sql = ''' CREATE database products ''';
 
# executing above query
cursor.execute(sql)
print("Database has been created successfully !!");
 
# Closing the connection
conn.close()

# players = Players()
# df = players.get_players_df()
# print(df[df['status'] == 'Active'])