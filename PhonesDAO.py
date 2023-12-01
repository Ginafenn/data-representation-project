import mysql.connector
import dbconfig as cfg

# Using the variables from dbconfig.py
db = mysql.connector.connect(
    host=cfg.host,
    user=cfg.user,
    password=cfg.password,
    database=cfg.database
)

cursor = db.cursor()

sql="insert into phone (Make, Model, Price) values (%s,%s,%s)"
values = ("iPhone","11",1050)

cursor.execute(sql, values)

db.commit()
print("1 record inserted, ID:", cursor.lastrowid)

cursor.close()
db.close()
