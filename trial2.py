from PIL import ImageTk, Image           #ALL LIBRARIES
import tkinter as tk
import datetime, random
import openpyxl as op
import requests
from io import BytesIO
import mysql.connector
import os
from dotenv import load_dotenv
import gui


load_dotenv()
"""
main functionality in SQL
1.
"""

USERNAME = os.getenv("USER_NAME")
PASSWD = os.getenv("PASSWD")
DATABASE = os.getenv("DATABASE")

db = mysql.connector.connect(
    host="localhost",
    user=USERNAME,
    passwd=PASSWD,
    database=DATABASE
)

db_cursor = db.cursor()


db_cursor.execute("select max(id) from phrases")
max_id = db_cursor.fetchall()[0][0] #to fetch data and be able to retrieve them -> ([98, ]) -> [0][0] -> 98

db_cursor.execute("select * from phrases")
all_phrases = db_cursor.fetchall()

#if not id -> false (empty array)
db_cursor.execute("select * from phrases where id=3")
not_id = db_cursor.fetchall()

#if not information -> None
db_cursor.execute("select * from phrases where id=4")
not_phrase = db_cursor.fetchall()

db_cursor.execute("select * from phrases")
all_phrases = db_cursor.fetchall() #(98, 'Sein Geist', None, 0)

used_phrase_id = []          #used to prevent in repeating the same phrases
phrases_counter = 1          #tracks how many phrases left, set on 1 because of excel start position on 2
anti_repeat = False          #prevents yes/no button spamming
###########################################################
db_cursor.execute("select date from phrases where id=4")
date = db_cursor.fetchall()[0][0]

expt = datetime.datetime.now()
now = str(expt.now()).split(".")[0]

cur_date = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

db_cursor.execute(f"update phrases set date='2020-04-12 01:11:14' where id=5")
db_cursor.execute("select * from phrases where id=5")

print(db_cursor.fetchone())