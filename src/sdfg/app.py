from flask import Flask, render_template, request, jsonify, session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)  
bcrypt = Bcrypt(app)

def  get_user(id):
    cnx = connect()
    cur = cnx.cursor()
    row = cur.execute('SELECT * FROM users WHERE id=%s', (id,))
    user = cur.fetchone()
    if user:
        return {'result':True, 'user':user}
    else:
        return {'result': False}

def connect():
    cnx = mysql.connector.connect(
            host="185.114.247.43",
            port=3306,
            database="sch688_vvedenie",
            user="sch688_vvedenie",
            password="Qwerty123")
    
@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json()
    cnx = connect()
    name = req['name']
    login = req['email']
    password = req['password']
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    date = (name, login, hashed)
    cur = cnx.cursor()
    try:
        rows = cur.execute('INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
    except:
        return {'result': False}
    cnx.commit()
    cnx.close()

    return {'result': True, 'id': cur.lastrowid}

@app.route('/user_autorization', methods=['POST'])
def user_autorization():
    req = request.get_json()
    cnx = connect()
    name = req['name']
    login = req['email']
    password = req['password']
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    date = (name, login, hashed)
    cur = cnx.cursor()
    try:
        rows = cur.execute('SELECT * FROM users WHERE email=%s AND password_hash=%s', date)
        user = cur.fetchone()
        session['user_id'] = user[0]
        print(user)
        if user:
            {'result': True}
        else:
            {'result': False}
    except:
        return {'result': False}
    cnx.commit()
    cnx.close()
    
# # Fetch one result
# row = cur.fetchone()
# print("Current date is: {0}".format(row[0]))

# # Close connection
# cnx.close()

@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/lk")
def lk():
    if 'user_id' in session:
        user = get_user(sesstion['user_id'])
        return render_template('lk.html',)
    else:
        return 'Пошел отсюда'

@app.route("/login")
def login():
    return render_template('login.html')

app.run()

