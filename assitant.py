import sqlite3
import sys
from sqlite3 import Error
x = sys.argv
string = x[2]


def delete_note(conn, id):
    sql = 'DELETE FROM notes WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM notes')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)


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
    cur.execute(sql, note)
    return cur.lastrowid


def main():
    note_table = """ CREATE TABLE IF NOT EXISTS notes (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name text NOT NULL
                ); """

    conn = create_connection(r"pythonsqlite.db")
    if conn is not None:
        create_table(conn, note_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        if x[2] == "all":
            sql_fetch(conn)
        elif x[2] == "delete":
            delete_note(conn, int(x[3]))
        else:
            note = (x[2],)
            create_note(conn, note)


if __name__ == '__main__':
    main()
