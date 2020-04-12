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
import pdb

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
db_cursor.execute("select * from phrases where id<13")

all_phrases = db_cursor.fetchall() #(98, 'Sein Geist', None, 0)
phrases_counter = 1          #tracks how many phrases left, set on 1 because of excel start position on 2
anti_repeat = False          #prevents yes/no button spamming

yes_score = 0
no_score = 0

def pick_a_phrase(self):
    global all_phrases, phrases_counter, anti_repeat
    unformatted_now = datetime.datetime.now()
    
    now_str = str(unformatted_now).split(".")[0]
    now_datetime = datetime.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
    anti_repeat = False
    
    for index, phrase in enumerate(all_phrases):        
        phrase_id = str(phrase[0])
        phrase_text = phrase[1]
        phrase_date = phrase[2]
        phrase_frequency = phrase[3]
        print(f"{phrase_text} :init: {phrase_id}")

        if phrase_text is not None:        
            if not phrase_date:
                sql = "update phrases set date = %s, frequency=1 where id = %s"
                val = (now_str, phrase_id)

                # db_cursor.execute(sql, val)  #if the cell doesnt have any date puts today's date
                # db.commit()

                phrases_counter += 1
                print(f"{phrase_text} :not Date: {phrase_id}")
            else:
                date_difference = now_datetime - phrase_date
                days_difference = date_difference.days #count how many days passed from the last practise

                phrases_counter += 1
                if days_difference >= phrase_frequency:  #checks frequency of practising the phrase
                    sql = "update phrases set date = %s where id = %s"
                    val = (now_str, phrase_id)

                    # db_cursor.execute(sql, val)  #updates date of phrase practising(now)
                    # db.commit()

                    phrases_counter += 1
                    print(f"{phrase_text} :have date and frequency time to practise: {phrase_id}")
                    pass     #pass to the next stage
                else:
                    print(f"{phrase_text} :have date and frequency but no exercise today: {phrase_id}")
                    all_phrases.pop(index)  
                    continue #start next iterate
            # pdb.set_trace()
            print(f"{phrase_text} :main_loop: {phrase_id}")
            GermanGame.pick_phrase_gui(self, phrase_text, phrase_id, phrase_frequency, yes_button, no_button, yes_score, no_score)

            all_phrases.pop(index)  
            break

        else:
            print(f"{phrase_text} :phrase is None: {phrase_id}")
            all_phrases.pop(index)
            phrases_counter += 1
            continue
    
    if all_phrases:
        return print(all_phrases)
    return print("Finished")


def yes_button(phrase_id, phrase_frequency):
    global anti_repeat, yes_score

    if anti_repeat is False:      #prevents YES button spamming with anti_repeat Boolean
        anti_repeat = True
        yes_score += 1

        sql = "update phrases set frequency=%s where id=%s"
        val = (phrase_frequency*2, phrase_id)
        db_cursor.execute(sql, val)
        db.commit()

def no_button(phrase_id, phrase_frequency):
    global anti_repeat, no_score
    if anti_repeat == False:
        anti_repeat = True
        no_score += 1

        if phrase_frequency >= 2:
            sql = "update phrases set frequency=%s where id=%s"
            val = (phrase_frequency/2, phrase_id)
            db_cursor.execute(sql, val)
            db.commit()


root = tk.Tk()

GermanGame(root, pick_a_phrase)

root.mainloop()

##################################################
#ONLY TESTING
db_cursor = db.cursor()

#get max id in the table
db_cursor.execute("select max(id) from phrases")
max_id = db_cursor.fetchall()[0][0] #to fetch data and be able to retrieve them -> ([98, ]) -> [0][0] -> 98

#get all phrases
db_cursor.execute("select * from phrases")
all_phrases = db_cursor.fetchall()

#if not id -> false (empty array)
db_cursor.execute("select * from phrases where id=3")
not_id = db_cursor.fetchall()

#if not information -> None
db_cursor.execute("select * from phrases where id=4")
not_phrase = db_cursor.fetchall()

#retrieve date
#date gets passed from sql database as datetime.datetime
db_cursor.execute("select * from phrases where id=5")
date = db_cursor.fetchall()[0][2]
# print(date)
# print(type(date))

#in case its different format change with this to datetime
cur_date = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
# print(cur_date)
# print(type(cur_date))

#pass date
unformatted_now = datetime.datetime.now()
now_str = str(unformatted_now).split(".")[0]
now_datetime = datetime.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")

# sql = "update phrases set date = %s, frequency = 1 where id = %s"
# val = (now_str, 9)

# db_cursor.execute(sql, val)  #if the cell doesnt have any date puts today's date


