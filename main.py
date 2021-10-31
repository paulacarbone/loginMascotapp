from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

# database connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
   
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form:
        usuario = request.form['usuario']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE usuario = %s AND password = %s', (usuario, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['usuario'] = account['usuario']
            # Redirect to home page
            return redirect(url_for('home'))       
        else:  
            msg = 'Usuario/password Incorrecto!'
    return render_template('index.html', msg=msg)
   

@app.route('/pythonlogin/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
 
   return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'localidad' in request.form and 'usuario' in request.form and 'password' in request.form:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        localidad = request.form['localidad']
        usuario = request.form['usuario']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE usuario = %s', (usuario,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'El usuario ya existe!'
        elif not usuario or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)', (nombre, apellido, localidad, usuario, password,))
            mysql.connection.commit()
            msg = 'Usuario registrado correctamente!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)   

@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('home.html', usuario=session['usuario'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  


if __name__ == "__main__":
    app.run(port=3000, debug=True)


    