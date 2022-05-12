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


# mapping
Acc = db.Table('accounts', db.metadata, autoload=True, autoload_with=db.engine)
acc_res = db.session.query(Acc).all()

User = db.Table('user', db.metadata, autoload=True, autoload_with=db.engine)
user_res = db.session.query(User).all()

Chck = db.Table('check_ups', db.metadata, autoload=True, autoload_with=db.engine)
check_res = db.session.query(Chck).all()

Prev = db.Table('prevention', db.metadata, autoload=True, autoload_with=db.engine)
prev_res = db.session.query(Prev).all()

Vacc = db.Table('vacc', db.metadata, autoload=True, autoload_with=db.engine)
vacc_res = db.session.query(Vacc).all()

Base = automap_base()
Base.prepare(db.engine, reflect=True)

acc = Base.classes.accounts
user = Base.classes.user
chck = Base.classes.check_ups
prev = Base.classes.prevention
vacc = Base.classes.vacc


# /////////////////// FUNKCJONALNOSC PODSTAWOWA - REJESTRACJA, LOGOWANIE, STRONA GŁÓWNA
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
            msg = 'Podano błędne hasło/nazwę użytkownika'
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
            msg = 'Konto o podanych danych już istnieje'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Użyj formatu adresu mailowego'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Nie używaj znaków specjanych'
        elif not username or not password or not email:
            msg = 'Wszystkie pola muszą zostać wypełnione'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email))
            conn.commit()
            msg = 'Konto założone pomyślnie!'
    elif request.method == 'POST':
        msg = 'Wszystkie pola muszą zostać wypełnione'
    return render_template('register.html', msg=msg)

# http://localhost:5000
@app.route('/', methods=['GET', 'POST'])
def home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM vacc WHERE id_user = %s', [session['id']])
        vacc = cursor.fetchall()
        cursor.execute('SELECT * FROM check_ups WHERE id_user = %s', [session['id']])
        check = cursor.fetchall()
        cursor.execute('SELECT * FROM prevention WHERE id_user = %s', [session['id']])
        prev = cursor.fetchall()
        return render_template('home.html', username=session['username'], vacc=vacc, check=check, prev=prev)
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


#/////////////////////////////// ZAKLADKI
# //GROUP INSERT
@app.route('/analyze', methods=['GET', 'POST'])
def insert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        account = cursor.fetchone()

        if account is not None:
            InsertVacc()
            InsertCheck()
            InsertPrev()
            msg = 'Sprawdź stronę główną.'

            return render_template("forms/basicform.html", msg=msg, user=account)
        else:
            msg = 'Bez wypełnienia formularza analiza jest niemożliwa!'
            return render_template("forms/basicform.html", msg=msg, user=account)
    else:
        return redirect(url_for('login'))

# ///INFORMACJE PODSTAWOWE///
# Wyswietlanie
# http://127.0.0.1:5000/basic
@app.route('/basic', methods=['GET', 'POST'])
def Basic():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template("forms/basicform.html", user=account)

    else:
        return redirect(url_for('login'))

# Dodawanie/zmienianie
# http://127.0.0.1:5000/basic/update redirect -> /basic
@app.route('/basic/update', methods=['GET', 'POST'])
def BasicUpdate():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM user WHERE id = %s', (session['id']))

        if request.method == 'POST':
            my_data = db.session.query(user).get(request.form.get('id'))

            if my_data is not None:
                my_data.wiek = request.form['wiek']
                my_data.waga = request.form['waga']
                my_data.wzrost = request.form['wzrost']
                my_data.plec = request.form['plec']
                my_data.papierosy = request.form['papierosy']
                my_data.alkohol = request.form['alkohol']
                my_data.aktywnosc = request.form['aktywnosc']
                db.session.commit()

                insert()

                return redirect(url_for('Basic'))
            else:
                account_id = session['id']
                wiek = request.form['wiek']
                waga = request.form['waga']
                wzrost = request.form['wzrost']
                plec = request.form['plec']
                papierosy = request.form['papierosy']
                alkohol = request.form['alkohol']
                aktywnosc = request.form['aktywnosc']
                cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (account_id, wiek, waga, wzrost, plec, papierosy, alkohol, aktywnosc))
                conn.commit()

                insert()

                return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# Usuwanie. Czyszczenie rzędu z rekordu.
# http://127.0.0.1:5000/basic/delete/ redirect -> /basic
@app.route('/basic/delete/', methods=['GET', 'POST'])
def BasicDelete():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:

            cursor.execute('DELETE FROM user WHERE account_id = %s', (session['id']))
            conn.commit()
            return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# todo//////////////////////////////nowe///////////////////////////////////////////////

# SZCZEPIENIA
#//// dodawanie po uzupełnieniu formularza basic - dziala, todo dodac wiecej
@app.route('/analyze', methods=['GET', 'POST'])
def InsertVacc():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    nazwa = 'def'
    typ = 'def'
    current = 0
    todo = 1

    if 'loggedin' in session:
        id_user = session['id']

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        wn = cursor.fetchone()


        # Różyczka
        if wn['plec'] == 1 and wn['wiek'] > 1:
            nazwa = "Przeciwko Różyczce"
            typ = "Obowiązkowe"
            print('liczyl')

            cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
            conn.commit()

        # Gruźlica
        if wn['wiek'] > 1:
            nazwa = "Przeciwko Gruźlicy"
            typ = "Obowiązkowe"

            cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
            conn.commit()
        return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# http://localhost:5000/vaccines - done
@app.route('/vaccines', methods=['GET', 'POST'])
def Vacc():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM vacc WHERE id_user = %s', [session['id']])
        account = cursor.fetchall()
        return render_template("forms/vaccines.html", vacc=account)
    else:
        return redirect(url_for('login'))

# http://localhost:5000/vaccines/update - dziala ale nie do konca todo
@app.route('/vaccines/update/<id>', methods=['GET', 'POST'])
def VaccChoice(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        current = request.form.get('current_status')
        todo = request.form.get('todo_status')

        if request.method == 'POST':
            if current == 'on':
                cursor.execute(""" UPDATE vacc SET current_status=%s WHERE id=%s""", (1, id))
                conn.commit()
            else:
                cursor.execute(""" UPDATE vacc SET current_status=%s WHERE id=%s""", (0, id))
                conn.commit()

            if todo == 'on':
                cursor.execute(""" UPDATE vacc SET todo_status=%s WHERE id=%s""", (1, id))
                conn.commit()
            else:
                cursor.execute(""" UPDATE vacc SET todo_status=%s WHERE id=%s""", (0, id))
                conn.commit()

        return redirect(url_for('Vacc'))
    else:
        return redirect(url_for('login'))

# http://127.0.0.1:5000/vaccines/delete/ redirect -> /vaccines - done
@app.route('/vaccines/delete/<id>', methods=['GET', 'POST'])
def VaccClear(id):

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

            cursor.execute('DELETE FROM vacc WHERE id = %s', (id))
            conn.commit()
            return redirect(url_for('Vacc'))
    else:
        return redirect(url_for('login'))


# todo na wzor funkcji powyzej!
# KONTROLNE
#//// dodawanie po uzupełnieniu formularza basic todo
def InsertCheck():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    nazwa = 'def'
    current = 0
    todo = 1

    if 'loggedin' in session:
        id_user = session['id']

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        wn = cursor.fetchone()

        # Prostata
        if wn['plec'] == 0 and wn['wiek'] > 40:
            nazwa = "Na prostatę"

            cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
            conn.commit()

        # Lipidogram
        if (wn['papierosy'] == 1 or wn['alkohol'] == 1 or wn['aktywnosc'] == 0) and wn['wiek'] > 40:
            nazwa = "Lipidogram"

            cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
            conn.commit()

    return 0

# http://localhost:5000/check_ups - done
@app.route('/check_ups', methods=['GET', 'POST'])
def Check():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM check_ups WHERE id_user = %s', [session['id']])
        account = cursor.fetchall()
        return render_template("forms/check_ups.html", check=account)
    else:
        return redirect(url_for('login'))

# http://localhost:5000/check_ups/update - dziala ale nie do konca todo
@app.route('/check_ups/update/<id>', methods=['GET', 'POST'])
def CheckChoice(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        current = request.form.get('current_status')
        todo = request.form.get('todo_status')

        if request.method == 'POST':
            if current == 'on':
                cursor.execute(""" UPDATE check_ups SET current_status=%s WHERE id=%s""", (1, id))
                conn.commit()
            else:
                cursor.execute(""" UPDATE check_ups SET current_status=%s WHERE id=%s""", (0, id))
                conn.commit()

            if todo == 'on':
                cursor.execute(""" UPDATE check_ups SET todo_status=%s WHERE id=%s""", (1, id))
                conn.commit()
            else:
                cursor.execute(""" UPDATE check_ups SET todo_status=%s WHERE id=%s""", (0, id))
                conn.commit()

        return redirect(url_for('Check'))
    else:
        return redirect(url_for('login'))

# http://127.0.0.1:5000/check_ups/delete/ redirect -> /vaccines - dziala, todo html
@app.route('/check_ups/delete/<id>', methods=['GET', 'POST'])
def CheckClear(id):

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

            cursor.execute('DELETE FROM check_ups WHERE id = %s', (id))
            conn.commit()
            return redirect(url_for('Check'))
    else:
        return redirect(url_for('login'))


# PROFILAKTYKA
#//// dodawanie po uzupełnieniu formularza basic dziala, todo dodac wiecej
def InsertPrev():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    nazwa = 'def'
    link = 'def'
    current = 0
    todo = 1

    if 'loggedin' in session:
        id_user = session['id']

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        wn = cursor.fetchone()

        # Udar
        if wn['wiek'] > 40 and (wn['alkohol']==1 or wn['papierosy'==1]):
            nazwa = "Przeciwko udarowi"
            link = 'pacjent.gov.pl/programy-profilaktyczne/program-profilaktyki-udarow'

            cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, link, current, todo, nazwa))
            conn.commit()

    return 0

# http://localhost:5000/prevention - done
@app.route('/prevention', methods=['GET', 'POST'])
def Prev():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM prevention WHERE id_user = %s', [session['id']])
        account = cursor.fetchall()
        return render_template("forms/prevention.html", prev=account)
    else:
        return redirect(url_for('login'))

# http://localhost:5000/vaccines/update - dziala ale nie do konca todo
@app.route('/prevention/update/<id>', methods=['GET', 'POST'])
def PrevChoice(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        current = request.form.get('current_status')
        todo = request.form.get('todo_status')

        if request.method == 'POST':
            if current == 'on':
                cursor.execute(""" UPDATE prevention SET current_status=%s WHERE id=%s""", (1, id))
                conn.commit()
            else:
                cursor.execute(""" UPDATE prevention SET current_status=%s WHERE id=%s""", (0, id))
                conn.commit()

            if todo == 'on':
                cursor.execute(""" UPDATE prevention SET todo_status=%s WHERE id=%s""", (1, id))
                conn.commit()
            else:
                cursor.execute(""" UPDATE prevention SET todo_status=%s WHERE id=%s""", (0, id))
                conn.commit()

        return redirect(url_for('Prev'))
    else:
        return redirect(url_for('login'))

# http://127.0.0.1:5000/prevention/delete/ redirect -> /vaccines - dziala, todo html
@app.route('/prevention/delete/<id>', methods=['GET', 'POST'])
def PrevClear(id):

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

            cursor.execute('DELETE FROM prevention WHERE id = %s', (id))
            conn.commit()
            return redirect(url_for('Prev'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

