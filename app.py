from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import re
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import insert

app = Flask(__name__)
app.secret_key = 'secret_key'

# 1 polacznie
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'harry'
app.config['MYSQL_DATABASE_PASSWORD'] = 'H4rru5i3k!'
app.config['MYSQL_DATABASE_DB'] = 'projekt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#2 polaczenie
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://harry:H4rru5i3k!@localhost:3306/projekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#reflection
Base = db.Table('Date', db.metadata, autoload=True, autoload_with=db.engine)
results = db.session.query(Base).all()
#auto-map
Base = automap_base()
Base.prepare(db.engine, reflect=True)
user = Base.classes.user

@app.route('/basic_info', methods=['GET', 'POST'])
def BasicInfo():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

        # reflection
        Base = db.Table('user', db.metadata, autoload=True, autoload_with=db.engine)
        results = db.session.query(user).all()
        # auto-map
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        all_data = results

#        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
#        user = cursor.fetchone()

        return render_template("homepage/basicform.html", all_data=all_data)
    else:
        return redirect(url_for('login'))

@app.route('/basic_info/insert', methods=['GET', 'POST'])
def BasicInfoInsert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        if request.method == 'POST':
            account_id = session['id']
            wiek = request.form['age']
            waga = request.form['weight']
            wzrost = request.form['height']
            plec = request.form['sex']
            papierosy = request.form['smoke']
            alkohol = request.form['drink']
            aktywnosc = request.form['move']
            cursor.execute('INSERT INTO user(account_id, wiek, waga, wzrost, plec, papierosy, alkohol, aktywnosc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (account_id, wiek, waga, wzrost, plec, papierosy, alkohol, aktywnosc))
            conn.commit()
            return redirect(url_for('BasicInfo'))
    else:
        return redirect(url_for('login'))

@app.route('/basic_info/delete/<id>', methods=['GET', 'POST'])
def BasicInfoDelete(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
            #my_data = db.session.query(user).get(id)
            #db.session.delete(my_data)
            #db.session.commit()

            cursor.execute('DELETE FROM user WHERE id = %s', (id))
            conn.commit()

            return redirect(url_for('BasicInfo'))
    else:
        return redirect(url_for('login'))

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
@app.route('/basic', methods=['GET', 'POST'])
def basicform():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    if 'loggedin' in session:
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
        return render_template('homepage/basicform.html', msg=msg)
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
