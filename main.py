from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
   
    msg = ''
    
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form:
        usuario = request.form['usuario']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE usuario = %s AND password = %s', (usuario, password,))
        
        account = cursor.fetchone()
        
        if account:
            
            session['loggedin'] = True
            session['id'] = account['id']
            session['usuario'] = account['usuario']
            
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
    
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'localidad' in request.form and 'usuario' in request.form and 'password' in request.form:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        localidad = request.form['localidad']
        usuario = request.form['usuario']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE usuario = %s', (usuario,))
        account = cursor.fetchone()
        
        if account:
            msg = 'El usuario ya existe!'
        elif not usuario or not password:
            msg = 'Please fill out the form!'
        else:
            
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)', (nombre, apellido, localidad, usuario, password,))
            mysql.connection.commit()
            msg = 'Usuario registrado correctamente!'
    elif request.method == 'POST':
        
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)   

@app.route('/pythonlogin/home')
def home():
    
    if 'loggedin' in session:
        return render_template('home.html', usuario=session['usuario'])
    
    return redirect(url_for('login'))  


if __name__ == "__main__":
    app.run(port=3306, debug=True)


    