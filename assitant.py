import sqlite3
import sys
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_note(conn, note):
    sql = ''' INSERT INTO notes(name)
           VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, notes)
    return cur.lastrowid


def main():
    note_table = """ CREATE TABLE IF NOT EXISTS notes (
                    id integer PRIMARY KEY,
                    name text NOT NULL
                ); """

    conn = create_connection(r"pythonsqlite.db")
    if conn is not None:
        create_table(conn, note_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        note = ('write book')


if __name__ == '__main__':
    main()
