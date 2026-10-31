from flask import Flask, render_template, request, jsonify, session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)  

app.secret_key = 'super_secret_key_123' 
bcrypt = Bcrypt(app)


def connect():
    cnx = mysql.connector.connect(
            host="185.114.247.43",
            port=3306,
            database="sch688_vvedenie",
            user="sch688_vvedenie",
            password="Qwerty123")
    return cnx

def get_user(id):
    cnx = connect()
    cur = cnx.cursor()
    cur.execute('SELECT * FROM users WHERE id=%s', (id,))
    user = cur.fetchone()
    cnx.close()
    if user:
        return {'result':True, 'user':user}
    else:
        return {'result': False}

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
        cur.execute('INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
        cnx.commit()
        user_id = cur.lastrowid
        cnx.close()
        return {'result': True, 'id': user_id} 
    except Exception as e:
        print(e) 
        return {'result': False}

@app.route('/user_autorization', methods=['POST'])
def user_autorization():
    req = request.get_json()
    cnx = connect()
    login = req['email']
    password = req['password']
    
    cur = cnx.cursor()
    try:

        cur.execute('SELECT id, password_hash FROM users WHERE email=%s', (login,))
        user = cur.fetchone()
        

        if user:
            user_id = user[0]
            db_password_hash = user[1]
            
            if bcrypt.check_password_hash(db_password_hash, password):
                session['user_id'] = user_id
                cnx.close()
                return {'result': True} 
            else:
                cnx.close()
                return {'result': False, 'error': 'Wrong password'}
        else:
            cnx.close()
            return {'result': False, 'error': 'User not found'}
            
    except Exception as e:
        print(e)
        return {'result': False}

@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/lk")
def lk():
    if 'user_id' in session:
        user_data = get_user(session['user_id'])
        return render_template('lk.html', user=user_data.get('user'))
    else:
        return 'Пошел отсюда'

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return '''
    <div style="text-align: center; margin-top: 50px; font-family: Arial;">
        <h2>Вы вышли из системы</h2>
        <a href="/login" style="color: #007bff; font-size: 18px;">Войти снова</a>
    </div>
    '''

if __name__ == '__main__':
    app.run(debug=True)