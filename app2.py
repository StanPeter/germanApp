from PIL import ImageTk, Image           #ALL LIBRARIES
import tkinter as tk
import datetime, random
import openpyxl as op
import requests
from io import BytesIO
import mysql.connector
import os
from dotenv import load_dotenv
from gui import GermanGame

load_dotenv()

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
db_cursor.execute("select * from phrases")

all_phrases = db_cursor.fetchall() #(98, 'Sein Geist', None, 0)
phrases_counter = 1          #tracks how many phrases left, set on 1 because of excel start position on 2
anti_repeat = False          #prevents yes/no button spamming


def pick_a_phrase(self):
    global all_phrases, phrases_counter, anti_repeat
    unformatted_now = datetime.datetime.now()
    
    now_str = str(unformatted_now).split(".")[0]
    now_datetime = datetime.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
    
    for index, phrase in enumerate(all_phrases):
        phrase_id = phrase[0]
        phrase_text = phrase[1]
        phrase_date = phrase[2]
        phrase_frequency = phrase[3]

        if phrase_text:        
            if not phrase_date:
                sql = "update phrases set date = %s and frequency=1 where id = %s"
                val = (now_str, phrase_id)

                #db_cursor.execute(sql, val)  #if the cell doesnt have any date puts today's date
                phrases_counter += 1
            else:
                date_difference = now_datetime - phrase_date
                # #retrieve date
                # #date gets passed from sql database as int()
                # db_cursor.execute("select date from phrases where id=4")
                # date = db_cursor.fetchall()[0][0]
                # #this change it to datetime.datetime class
                # cur_date = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")

                days_difference = date_difference.days #count how many days passed from the last practise

                phrases_counter += 1
                if days_difference >= phrase_frequency:  #checks frequency of practising the phrase
                    sql = "update phrases set date = %s where id = %s"
                    val = (now, phrase_id)

                    phrase("check here ELSE")
                    # db_cursor.execute(sql, val)  #if the cell doesnt have any date puts today's date
                    phrases_counter += 1
                    print('pass' + str(phrase_id))
                    pass     #pass to the next stage
                else:
                    print('continue' + str(phrase_id))
                    continue

            GermanGame.pick_phrase_gui(self, phrase_text, yes_funct, no_funct)

            all_phrases.pop(index)
            break

        else:
            print(f"skipped {phrase_id}")
            phrases_counter += 1
            continue

def yes_funct():
    print("works")

def no_funct():
    print("works2")

root = tk.Tk()

GermanGame(root, pick_a_phrase)

root.mainloop()


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

#retrieve date
#date gets passed from sql database as int()
db_cursor.execute("select date from phrases where id=4")
date = db_cursor.fetchall()[0][0]
#this change it to datetime.datetime class
cur_date = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")

#pass date
unformatted_now = datetime.date.today()
now = unformatted_now.strftime('%Y-%m-%d %H:%M:%S')

sql = "UPDATE phrases SET date = %s WHERE id = %s"
val = (now, 5)

db_cursor.execute(sql, val)
db_cursor.execute("select date from phrases where id=5")