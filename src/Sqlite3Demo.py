import sqlite3
import os

filename = 'test.db'
conn = sqlite3.connect(filename)  # 创建连接
c = conn.cursor()

cursor = c.execute('''SELECT name FROM Sqlite_master  WHERE type='table' ORDER BY name; ''')
AllTable = [row[0] for row in cursor]
if 'TPERSON' not in AllTable:
   # 创建表
   c.execute('''CREATE TABLE TPERSON
          (ID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          AGE            INT     NOT NULL,
          ADDRESS        CHAR(50),
          SALARY         REAL);''')
# 插入数据
# c.execute("INSERT INTO TPERSON (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'wang', 32, '杭州', 20000.00 )")
# 查询数据
cursor = c.execute("SELECT id, name, address, salary  from TPERSON")
for row in cursor:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("ADDRESS = ", row[2])
   print ("SALARY = ", row[3])
conn.commit()
conn.close()