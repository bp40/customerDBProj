import mysql.connector
import os
import sys

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = os.environ.get('DB_PASS'),
    database = "games"
)

myCursor = mydb.cursor(buffered=True)


def createTable():
    myCursor.execute('CREATE TABLE IF NOT EXISTS customer (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))')
    
def addCustomer(name, address):
    query = 'INSERT INTO customer (name, address) VALUES (%s, %s)'
    values = (name, address)
    myCursor.execute(query, values)
    
    mydb.commit()
    print(myCursor.rowcount, 'rows affected')
    
def checkExisting(name, address):
    myCursor.execute(
        "SELECT name, COUNT(*) FROM customer WHERE name = %s AND address = %s GROUP BY Name",
        (name, address)
    )
    
    if myCursor.rowcount != 0:
        return False
    else:
        return True

def menu():
    print('==================================')
    print("Select an option")
    print(' 1) Add customer')
    print(' 2) Update customer')
    print(' 3) Remove customer')
    print(' 4) Quit')
    choice = input("Enter a number : ")
    if choice == '1':
        customerAddHandler()
    elif choice == '2':
        updateCustomer()
    elif choice == '3':
        removeCustomer()  
    elif choice == '4':
        sys.exit("Goodbye!")
    
def customerAddHandler():
    print('==================================')
    print('type none to cancel')
    nameIn = input("Enter name : ")
    addressIn = input("Enter Address : ")
    
    if nameIn != 'none' or addressIn != 'none':
        if checkExisting(nameIn, addressIn):
            addCustomer(nameIn, addressIn)
        else:
            print("Already Exist")
    else:
        print('===Cancelled===')
        menu()
    customerAddHandler()
    
def showCustomer(customerID):
    try:
        myCursor.execute(
                'SELECT * FROM customer WHERE id = %s' % customerID
                ) 
        results = myCursor.fetchall()
        print('Name : ' + results[0][1])
        print('Address : ' + results[0][2])
    except:
        print("!! Customer ID Error !!")
        menu()
        
def updateCustomer():
    print('==================================')
    customerID = input("Enter ID of customer (0 to cancel) : ")
    
    if customerID != '0':
        showCustomer(customerID)
        
        newName = input("Enter new name : ")
        newAddress = input("Enter new address : ")
        if newName == '0' or newAddress == '0':
            print('===Cancelled===')
            menu()
        else:
            try:
                query ='UPDATE customer SET name = %s, Address = %s WHERE id = %s'
                values = (newName, newAddress, customerID)
                
                myCursor.execute(query, values)
                
                mydb.commit()
                print(myCursor.rowcount, 'rows affected')
            except:
                print('Error')
        updateCustomer()              
    else:
        print('===Cancelled===')
        menu() 
       
def removeCustomer():
    print('==================================')
    customerID = input("Enter ID of customer (0 to cancel) : ")
    if customerID != '0':
        showCustomer(customerID)
        
        confirm = input("Confirm delete? y/n : ")
        if confirm == 'y':
            
            try:
                query = 'DELETE from customer where id = %s' % customerID
                myCursor.execute(query)
                
                mydb.commit()
                print(myCursor.rowcount, 'rows affected')
                removeCustomer()
            except:
                print('Error')
                removeCustomer()
            
        else:
            print('===Cancelled===')
            menu()
        
    else:
        print('===Cancelled===')
        menu()
        
menu()



    