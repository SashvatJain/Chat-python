from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import psycopg2
from psycopg2 import extras

hostname='localhost'
database='postgres'
username='postgres'
pwd='admin'
port_id=5432

app=Flask(__name__)
# CORS(app,origins=["http://localhost:3000"])
# app.config['SECRET_KEY'] = 'your_secret_key'  # Required for SocketIO
socketio = SocketIO(app,cors_allowed_origins="*")
connection = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)
# cursor = connection.cursor()

# @app.post('/getItems')
# def add_new_customer(first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address):
#     cursor.execute(
#         "INSERT INTO customers (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#         (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address)
#     ) 
#     connection.commit()


@socketio.on('send_message')
def handle_connect(data):
    print(f'data recieved from Client:{data}')
    socketio.emit('recieve_message', {'message': data})

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app) 


@app.get('/getCustomers')
def get_all_customer():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
            # for customer in customers:
                # print(customer)
    return {'customers':customers}

@app.get('/getCustomersList')
def get_customers_list():
    with connection:
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute("SELECT customer_id, first_name, last_name, email FROM customers")
            customers = cursor.fetchall()
            # for customer in customers:
                # print(customer)
    return {'customers':customers}

@app.post('/addCustomer')
def add_customer():
    data=request.get_json()
    first_name=data['fName']
    last_name=data['lName']
    email=data['email']
    date_of_birth=data['dob']
    is_active=data['isActive']
    registration_date=data['registrationDate']
    phone_number=data['phoneNumber']
    address=data['address']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO customers (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                 (first_name, last_name, email, date_of_birth, is_active, registration_date, phone_number, address)
            )
    return {'message': 'Customer added'},201


@app.get('/getCustomer/<string:fname>')
def get_customer(fName):
    with connection:
        with connection.cursor() as cursor:
             cursor.execute("SELECT * FROM customers WHERE first_name = %s", (fName,))
             customer=cursor.fetchone()
    return {'customer': customer},200

@app.get('/getCustomer')
def get_customer_args():
    customerId= request.args.get('customerId')
    fName= request.args.get('fName')
    lName= request.args.get('lName')
    email= request.args.get('email')
    phoneNumber= request.args.get('phoneNumber')
    print(phoneNumber)
    with connection:
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            if customerId is not None:
                cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customerId,))
            elif (fName is not None) & (lName is not None):
                cursor.execute("SELECT * FROM customers WHERE first_name = %s AND last_name = %s", (fName,lName))
            elif email is not None:
                cursor.execute("SELECT * FROM customers WHERE email = %s", (email,)) 
            elif phoneNumber is not None:
                cursor.execute("SELECT * FROM customers WHERE phone_number = %s", (phoneNumber,)) 
            customer=cursor.fetchone()
    return {'customer': customer},200



# connection.commit()
# connection.close()
# cursor.close()
