from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)

app.secret_key = 'your secret key'

 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'

id
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
   
    msg = ''
    
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE usuario = %s AND password = %s', (usuario, password,))
        
        account = cursor.fetchone()
        global id
        if account:
            
            id = account['id']
            session['loggedin'] = True
            session['id'] = account['id']
            session['usuario'] = account['usuario']
            session['nombre'] = account['nombre']
            session['apellido'] = account['apellido']
            
            return redirect(url_for('home'))       
        else:  
            msg = 'Usuario/password Incorrecto!'
    return render_template('index.html', msg=msg)
   

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
   return redirect(url_for('login'))

@app.route('/home/edit', methods=['GET', 'POST'])
def edit():
    global id
    if request.method == 'POST':
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        localidad = request.form['localidad']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        account = cursor.fetchone()
        cursor.execute("""
            UPDATE accounts
            SET nombre = %s,
                apellido = %s,
                localidad = %s,
                password = %s
            WHERE id = %s
        """, (nombre, apellido, localidad, password, account['id'],))
        mysql.connection.commit()
        return redirect(url_for('home'))
    return render_template('edit.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    
    if request.method == 'POST':
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
        else:                     
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)', (nombre, apellido, localidad, usuario, password,))
            mysql.connection.commit()
            msg = 'Usuario registrado correctamente!'
    elif request.method == 'POST':
        
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)   

@app.route('/home')
def home():
    
    if 'loggedin' in session:
        return render_template('home.html', nombre=session['nombre'], apellido=session['apellido'])
    
    return redirect(url_for('login'))  


if __name__ == "__main__":
    app.run(port=3000, debug=True)


    