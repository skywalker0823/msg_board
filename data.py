# import pymysql
# from dbutils.pooled_db import PooledDB
# from flask import request
# import os
# from dotenv import load_dotenv
# from datetime import datetime
# from dateutil.parser import parse


# load_dotenv()
# POOL = PooledDB(
#     creator=pymysql,  # Which DB module to use
#     # Allowed max connection, 0 and None means no limitations.
#     maxconnections=6,
#     mincached=2,  # Least connection when created, 0 means don't.
#     # Queue when there is no connection avaliable. True = wait；False = No waits, and report error.
#     blocking=True,
#     ping=0,  # Check if Mysql service is avaliable # if：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always

#     host='wehelp.cwyqtvro2bn0.us-east-1.rds.amazonaws.com',
#     port=3306,
#     user='admin',
#     password=os.getenv("DB_PASS"),
#     database='site',
#     charset='utf8',
#     cursorclass=pymysql.cursors.DictCursor
# )

# connection = POOL.connection()


# class Board:
#     def uploads(says,img_id):
#         try:
#             with connection.cursor() as cursor:
#                 result = cursor.execute(
#                     """INSERT INTO
#                     members(
#                         says,
#                         img_id
#                     )
#                     VALUES(%s,%s)
#                     """,(says,img_id)
#                 )
#             connection.commit()
#             return "ok"
#         except Exception as e:
#             print(e)
#             print("pay新增CREATE資料錯誤")
#             return "upload error"

#     def get_all():
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     """SELECT
#                     says,
#                     img_id
#                     FROM members
#                     """
#                 )
#             result = cursor.fetchall()
#             connection.commit()
#             return result
#         except Exception as e:
#             print(e)
#             print("pay新增CREATE資料錯誤")
#             return "upload error"
