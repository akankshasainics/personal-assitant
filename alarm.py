import sqlite3
import sys
import time
import os
import datetime  
import pytz
from sqlite3 import Error
import requests, json

# PAPERQUOTES_API_ENDPOINT = 'http://api.paperquotes.com/apiv1/quotes?tags=love&limit=5'
# TOKEN = '{8b708edeb611b9589a5ae1b9b12f92d3b5038968}'
# response = requests.get(PAPERQUOTES_API_ENDPOINT, headers={'Authorization': 'TOKEN {}'.format(TOKEN)})

# if response.ok:

#     quotes = json.loads(response.text).get('results')

#     for quote in quotes:
#         print(quote.get('quote'))
#         print(quote.get('author'))
#         break
#         # print quote.get('tags')

x = sys.argv
def processing_alarm(conn, t, val):
    cur = conn.cursor()
    while t:
        cur.execute("SELECT is_active FROM alarms WHERE id =? AND is_active NOT IN (0)", (val,))
        row = cur.fetchall()
        if row == []:
            break
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(60)
        t -= 1
    if not t:
        os.system("gnome-terminal -e 'bash -c \" xeyes ; exec bash\"'")
        sys.stdout.write("Time's up\n")

def disable_alarm(conn, alarm):
    sql = ''' UPDATE alarms
              SET is_active = ? 
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, alarm)
    cur.close()
    conn.commit()
   
def sql_fetch(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM alarms')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
    cursorObj.close()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, isolation_level = None)
    except Error as e:
        print(e)
    conn.execute('pragma journal_mode=wal;')
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_alarm(conn, alarm):
    sql = ''' INSERT INTO alarms(duration, is_active)
           VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, alarm)
    cur.close()
    return cur.lastrowid

def main():
    alarm_table = """ CREATE TABLE IF NOT EXISTS alarms (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    duration text NOT NULL
                ); """

    conn = create_connection(r"pythonsqlite.db")
    if conn is not None:
        create_table(conn, alarm_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        if x[2] == "all":
            sql_fetch(conn)
        elif x[2] == "disable":
            disable_alarm(conn, (0, int(x[3])))
        else:
            alarm = (x[2], 1)
            val = create_alarm(conn, alarm)
            h,m = x[2].split(':')
            h = int(h)
            m = int(m)
            curr = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            hour = curr.hour
            minute = curr.minute
            if h > hour or (hour == h and m >= minute):
                t = 60*(int(h)) + int(m) - (60*(hour) + minute)
            else:
                t = (24-hour)*60 - minute + 60*h + m
            processing_alarm(conn, t, val)
            

if __name__ == '__main__':
    main()
