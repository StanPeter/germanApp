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

now = datetime.date.today()

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

#retrieve date
#date gets passed from sql database as int()
db_cursor.execute("select date from phrases where id=4")
date = db_cursor.fetchall()[0][0]
#this change it to datetime.datetime class
cur_date = datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")

#pass date
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

sql = "UPDATE phrases SET date = %s WHERE id = %s"
val = (formatted_date, 5)

db_cursor.execute(sql, val)
db_cursor.execute("select date from phrases where id=5")
#########################################################

# print(a)

# cur_date = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S")

# db_cursor.execute(f"update phrases set date=' where id=5")
# db_cursor.execute("select * from phrases where id=5"





# def pick_a_phrase(none):
#     global anti_repeat, phrases_counter

#     for index, phrase in enumerate(all_phrases):
#         phrase_id = phrase[0]
#         phrase_text = phrase[1]
#         phrase_date = phrase[2]
#         phrase_frequency = phrase[3]

#         if phrase_text:        
#             if phrase_date None:
#                 db_cursor.execute("update phrases set frequency=1 where id={}".format(phrase_id))
#                 work_sheet.cell(row=n, column=3).value = now  #if the cell doesnt have any date puts today's date
#                 phrases_counter += 1
#             else:
#                 datum_counter_minor = now - datetime.datetime.date(work_sheet.cell(row=n, column=3).value)
#                 datum_counter_major = datum_counter_minor.days
#                 phrases_counter += 1
#                 if datum_counter_major >= work_sheet.cell(row=n, column=5).value:  #checks frequency of practising the phrase
#                     work_sheet.cell(row=n, column=3).value = now
#                     print('pass' + str(n))
#                     pass
#                 else:
#                     print('continue' + str(n))
#                     continue

#             wb.save(file_name)
#             break
#         else:
#             print(f"skipped {phrase_id}")
#             phrases_counter += 1
#             continue

# root = tk.Tk()

# App = gui.GermanGame(root, current_phrase)


# root.mainloop()
