from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import psycopg2
from psycopg2 import extras

hostname='localhost'
database='postgres'
username='postgres'
pwd='admin'
port_id=5432

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
connection = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    # senderName = message['sender']
    text = message['text']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO chat_messages (sender_email, message_text, receiver_email) VALUES  (%s, %s, %s)",
                 ("senderName", text, 'all')
            )
    socketio.emit('receive_message', message)  # Broadcast the message to all connected clients

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.get('/getMessages')
def get_all_messages():
    with connection:
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
             cursor.execute("SELECT * FROM chat_messages")
             allMessages=cursor.fetchall()
    return {'body': allMessages},200



@app.post('/addUser')
def handle_sign_up():
    data=request.get_json()
    print('data:',data)
    email=data['email']
    name=data['name']
    password=data['password']
    phNumber=data['phNumber']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email, phone_number, password) VALUES (%s, %s, %s, %s)",
                 (name, email, phNumber, password)
            )
    return {'body': 'User added'},201

@app.put('/updateUser')
def edit_User_status():
    data=request.get_json()
    print('data:',data)
    userId=data['id']
    status=data['status']
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET isVerified = {status} WHERE id = {userId}"
            )
    return {'body': 'User Updated'},201


@app.get('/usersList')
def fetch_all_users():
    with connection:
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
             cursor.execute("SELECT * FROM users WHERE isAdmin = false")
             userList=cursor.fetchall()
    return {'body': userList},200


@app.post('/login')
def login_user():
    try:
        data = request.get_json()
        print("data:", data)
        email = data['email']
        password = data['password']

        with connection:
            with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                # Use parameterized queries to prevent SQL injection
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user_data = cursor.fetchone()

                if user_data is not None:

                    if user_data['password'] == password:
                        if user_data['isverified'] == True:
                            return {
                                    "status": "success",
                                    "message": "Login successful",
                                    "data": {
                                        "user_id": user_data['id'],
                                        "name": user_data['name'],
                                        }
                                    }, 200
                        else:
                            return {
                                    "status": "error",
                                    "message": "User Not Verified!",
                                    "data": {}
                                    }, 200
                    else:
                        return {
                                "status": "error",
                                "message": "Invalid credentials",
                                "data": {}
                                }, 200
                    
                else:
                    return {
                            "status": "error",
                            "message": "User Not Found!",
                            "data": {}
                            }, 200

    except Exception as e:
        print(f"Error: {e}")
        return {
                "status": "error",
                "message": "Something went wrong!",
                "data": {}
                }, 500


if __name__ == '__main__':
    socketio.run(app, debug=True)

# connection.close()