from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


#Conexion a la base de datos
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'login'
)

#Ruta inicio
@app.route("/",methods=["GET", "POST"])
def home():
    return render_template('/index.html')

#Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            # Si el correo ya existe, redirigir al formulario de registro con un mensaje de error
            return render_template('index.html', error='Ya has sido registrado con este correo electrónico.')
        else:
            cursor.execute('INSERT INTO users (name, lastname, email, password) VALUES (%s, %s, %s, %s)', (name, lastname, email, password))
            db.commit()
            return render_template('index.html', success='Registro exitoso.')


#Ruta de login
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']

            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            account = cursor.fetchone()

            if account and password == account [4]:
                return render_template('home.html', welcome='Welcome to our website enoy it!')
            else:
                # Si el correo o la contraseña son incorrectos, redirigir al formulario de inicio de sesión con un mensaje de error
                return render_template('index.html', error='Correo electrónico o contraseña incorrectos.')


#Volver al login
@app.route('/index')
def index():
    return render_template('index.html')
























if __name__ == '__main__':
    app.run(debug=True)