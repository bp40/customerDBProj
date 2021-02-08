from flask import Flask, render_template
import mysql.connector
import os
app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = os.environ.get('DB_PASS'),
    database = "games"
)

query = ("SELECT * FROM customer")

myCursor = mydb.cursor(buffered=True)

@app.route("/")
def home():
    
    myCursor.execute(query)
    customers = myCursor.fetchall()
    
    class Customer:
        def __init__(self, id, name, address):
            self.id = id
            self.name = name
            self.address = address
    
    customerList = []
    for customer in customers:
        currentCustomer = Customer(customer[0], customer[1], customer[2])
        customerList.append(currentCustomer)
        
    return render_template("home.html", customerList=customerList)

if __name__ == "__main__":
    app.run(debug=True)