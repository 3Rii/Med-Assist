from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired


app = Flask(__name__)

app.secret_key = 'secret_key'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'harry'
app.config['MYSQL_DATABASE_PASSWORD'] = 'H4rru5i3k!'
app.config['MYSQL_DATABASE_DB'] = 'projekt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# http://localhost:5000/login/
@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


# http://localhost:5000/register
@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

# http://localhost:5000/
@app.route('/', methods=['GET', 'POST'])
def home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
        username = cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('homepage/home.html', username=session['username'], account=account)
    return redirect(url_for('login'))


# http://localhost:5000/basic
@app.route('/basic/update', methods=['GET', 'POST'])
def basicform_update():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
    #         cursor.execute('SELECT * FROM user_u WHERE id IN (SELECT id FROM accounts WHERE id = %s)', [session['id']])
    #         account = cursor.fetchone()
    #         if not cursor:
    #             msg = "ormularz pusty"
    #         return render_template('homepage/basicform_view.html', account=account, msg=msg)
    # else:
    #     return redirect(url_for('login'))

        if request.method == 'POST':
            cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])

            age = request.form['age']
            weight = request.form['weight']
            height = request.form['height']
            # radio bool
            sex = request.form.get("sex")
            smoke = request.form.get("smoke")
            drink = request.form.get("drink")
            move = request.form.get("move")

            if not age.isnumeric():
                msg = 'Age must be a number!'
            elif not weight.isnumeric():
                msg = 'Weight must be a number!'
            elif not height.isnumeric():
                msg = 'Height must be a number!'
            else:
                cursor.execute('INSERT INTO user_u VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               ([session['id']], age, weight, height, sex, smoke, drink, move))
                conn.commit()
                msg = 'Form completed!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('homepage/basicform_put.html', msg=msg)

@app.route('/basic', methods=['GET', 'POST'])
def basicform_view():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
        cursor.execute('alter table user_u alter column id set default %s', [session['id']])
        inserted = 'ok'
        print('ok')

        if inserted == 'ok':
            cursor.execute('SELECT * FROM user_u WHERE id IN (SELECT id FROM accounts WHERE id = %s)', [session['id']])
            account = cursor.fetchone()
        return render_template('homepage/basicform_view.html', msg=msg, account=account)
    else:
        return redirect(url_for('login'))

# http://localhost:5000/logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# http://localhost:5000/profile
@app.route('/profile')
def profile():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])

        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
