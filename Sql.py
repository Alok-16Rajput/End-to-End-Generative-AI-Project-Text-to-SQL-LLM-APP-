import sqlite3
##Connect to sqlite
connection=sqlite3.connect("student.db")

## Create a cursor object to insert record,create table,retrieve
cursor=connection.cursor()

## create table
table_info="""
Create table STUDENT(Name Varchar(25),class Varchar(25),Section Varchar(25),marks INT);

"""
cursor.execute(table_info)

## Insert some more records
cursor.execute('''Insert into STUDENT values('Alok','Data Science','A',90)''')
cursor.execute('''Insert into STUDENT values('krish','Data Science','A',94)''')
cursor.execute('''Insert into STUDENT values('Amit','WEBDEVELOPMENT','A',86)''')
cursor.execute('''Insert into STUDENT values('sudhanshu','Data Science','B',55)''')
cursor.execute('''Insert into STUDENT values('yogesh','DEVOPS','B',35)''')

## Display all the records
print("The inserted records are")

data=cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)
    
## Close the connection
connection.commit()
connection.close()