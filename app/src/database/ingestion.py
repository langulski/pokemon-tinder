import psycopg2
def _read_sql_file(file_path:str):
    try:
        with open(file_path, 'r') as sql_file:
            sql_string = sql_file.read()
        return str(sql_string)
    except FileNotFoundError:
        return None


if __name__ =='__main__':
    pg_connection_dict = {
        'dbname': "postgres",
        'user': "postgres",
        'password': "postgres",
        'port': 5432,
        'host': "postgres"
    }
    try:
        tables =_read_sql_file('./migrations/migration_v0.sql')
        data =_read_sql_file('./fixtures/pokemons.sql')
        conn = psycopg2.connect(**pg_connection_dict)
        cursor = conn.cursor()
        cursor.execute(tables)
        conn.commit()
        cursor.execute("SELECT * FROM POKEMONS;")
        rows = cursor.fetchall()
        if len(rows) <=1:
            cursor.execute(data)
            conn.commit()
        cursor.close()
        conn.close()
    except:
        raise
