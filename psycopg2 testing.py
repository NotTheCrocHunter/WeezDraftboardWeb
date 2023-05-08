import psycopg2
from psycopg2.extras import execute_values

# ...

projects = [
{'name': 'project alpha', 'code': 12, 'active': True},
{'name': 'project beta', 'code': 25, 'active': True},
{'name': 'project charlie', 'code': 46, 'active': False}
]

columns = projects[0].keys()
query = "INSERT INTO projects ({}) VALUES %s".format(','.join(columns))

# convert projects values to list of lists
values = [[value for value in project.values()] for project in projects]


conn = psycopg2.connect(
    database='players',
    user='postgres',
    password='docker',
    port='5432',
    host='localhost')

# Create database
with conn:
    with conn.cursor() as curs:
        create_db_sql = """ CREATE database testing""";
        curs.execute(create_db_sql)

with conn:
    with conn.cursor() as curs:
        execute_values(curs, query, values)
        conn.commit()
