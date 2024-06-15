from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
        raise  # Raise the exception to indicate the failure
    return connection

def insert_user(connection, username, password_hash, email, role_id):
    insert_query = """
    INSERT INTO users (username, password_hash, email, role_id)
    VALUES (%s, %s, %s, %s);
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, (username, password_hash, email, role_id))
        connection.commit()
        print(f"User {username} inserted successfully")
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

def find_user_by_credentials(username, password):
    connection = create_connection("localhost", "root", "s@r@n1977", "Travel")
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
    cursor.execute(query, (username, password,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'message': 'No JSON data provided'}), 400
        
        username = data.get('username')  
        password_hash = data.get('password')
        email = data.get('email')
        role_id = 1
        print(data)
        connection = create_connection("localhost", "root", "s@r@n1977", "Travel")
        if connection:
            insert_user(connection, username, password_hash, email, role_id)
            connection.close()
            print("The connection is closed")
            return "User added successfully"
    return "Error adding user"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'message': 'Request body must be JSON'}), 400

        username = data.get('username')
        password = data.get('password')
        print(data)
        if not (username and password):
            return jsonify({'message': 'Username and password are required'}), 400

        user = find_user_by_credentials(username, password)
        if user:
            return jsonify({'message': 'Login successful', 'user_id': user }), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
        
@app.route('/cards', methods=['GET'])
def get_gen_cards():
    connection = create_connection("localhost", "root", "s@r@n1977", "Travel")
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT title, text, imgSrc FROM cards")
    card_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(card_data)

@app.route('/cardsForPackage', methods=['GET'])
def get_package_cards():
    connection = create_connection("localhost", "root", "s@r@n1977", "Travel")
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, title, imgSrc, details FROM package_cards")
    card_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(card_data)


if __name__ == '__main__':
    app.run(debug=True)
