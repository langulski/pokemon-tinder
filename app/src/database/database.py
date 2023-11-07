import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


PG_CONNECTION_DICT = {
    "dbname": os.getenv("DATABASE"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DBPORT"),
    "host": os.getenv("HOST"),
}


def fetch_data_paginated(
    sql_file: str, user_id: int, limit: int = 5, offset: int = 0
) -> list[dict]:
    query = _read_sql_file(sql_file).format(user_id=user_id, limit=limit, offset=offset)
    conn, cursor = pgcursor()
    cursor.execute(query)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data_list = [
        {column_name: value for column_name, value in zip(column_names, row)}
        for row in rows
    ]
    cursor.close()
    conn.close()

    return data_list


def retrive_saved_pokemons(sql_file: str, user_id: int, limit: int = 200) -> list[dict]:
    query = _read_sql_file(sql_file).format(
        user_id=user_id,
        limit=limit,
    )
    conn, cursor = pgcursor()
    cursor.execute(query)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data_list = [
        {column_name: value for column_name, value in zip(column_names, row)}
        for row in rows
    ]
    cursor.close()
    conn.close()

    return data_list


def save_selected_pokemons(
    sql_file: str, user_id: int, pokemon_id: int, love: bool
) -> None:
    try:
        query = _read_sql_file(sql_file).format(user_id, pokemon_id, love)
        conn, cursor = pgcursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        raise "Error while trying to update"


#######################
##Auxiliary Functions##
#######################


def _read_sql_file(file_path: str):
    try:
        with open(file_path, "r") as sql_file:
            sql_string = sql_file.read()
        return str(sql_string)
    except FileNotFoundError:
        return None


def pgcursor(connection=PG_CONNECTION_DICT):
    conn = psycopg2.connect(**connection)
    return conn, conn.cursor()
