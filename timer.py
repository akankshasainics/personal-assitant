import sqlite3
import sys
from sqlite3 import Error
import time
import os
x = sys.argv
def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM timers')
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

def create_timer(conn, timer):
    sql = ''' INSERT INTO timers(duration)
           VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, timer)
    return cur.lastrowid

def main():
    task_table = """ CREATE TABLE IF NOT EXISTS timers (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    duration integer NOT NULL
                ); """

    conn = create_connection(r"pythonsqlite.db")
    if conn is not None:
        create_table(conn, task_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        if x[2] == "all":
            sql_fetch(conn)
        elif x[2] == "delete":
            delete_task(conn, (int(x[3])))
        else:
            timer = (x[2],)
            create_timer(conn, timer)
            t = int(x[2])
            print("1")
            
            print("2")
            while t:
                mins, secs = divmod(t, 60)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                print(timeformat, end='\r')
                time.sleep(1)
                t -= 1
            # os.system("gnome-terminal -e 'sudo apt-get update' ")
            os.system('spd-say "Times up"')
            sys.stdout.write("Time's up\n")

if __name__ == '__main__':
    main()
