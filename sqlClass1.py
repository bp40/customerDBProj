import mysql.connector
import os

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = os.environ.get('DB_PASS'),
    database = "games"
)

platform = input("Enter a platform : ")

if platform == 'None':
    print("END")
else:
    myCursor = mydb.cursor()

    query = "SELECT score,platform,title FROM gamz WHERE platform = '" + platform + "' ORDER BY score DESC, title ASC LIMIT 5;"

    myCursor.execute(query)

    myResult = myCursor.fetchall()

    for i in myResult:
        print(i)


