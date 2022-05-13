from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import re
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.secret_key = 'secret_key'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'harry'
app.config['MYSQL_DATABASE_PASSWORD'] = 'H4rru5i3k!'
app.config['MYSQL_DATABASE_DB'] = 'projekt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://harry:H4rru5i3k!@localhost:3306/projekt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
mysql.init_app(app)

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

#Check is request.form is float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False



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
# ///INFORMACJE PODSTAWOWE///
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

# BasicForm CRUD
# http://127.0.0.1:5000/basic/update
@app.route('/basic/update', methods=['GET', 'POST'])
def BasicUpdate():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg1 = ''

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM user WHERE account_id = %s', (session['id']))
        row = cursor.fetchone()

        if request.method == 'POST' and 'wiek' in request.form and 'waga' in request.form and 'wzrost' in request.form and 'plec' in request.form and 'papierosy' in request.form and 'alkohol' in request.form and 'aktywnosc' in request.form:
            wiek = request.form['wiek']
            waga = request.form['waga']
            wzrost = request.form['wzrost']
            plec = request.form['plec']
            papierosy = request.form['papierosy']
            alkohol = request.form['alkohol']
            aktywnosc = request.form['aktywnosc']

            if not isfloat(wiek) or not isfloat(waga) or not isfloat(wzrost):
                msg1 = "Podano błędnie dane lub nie wprowadzono zmian!"
                msg2 = "(Proszę, sprawdź jeszcze raz, czy podałeś liczbę.)"
                return render_template("forms/basicform.html", msg=msg1, msg2=msg2, user=row)

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
                msg1 = 'Formularz zedytowano pomyślnie!'
                return render_template("forms/basicform.html", msg=msg1, user=row)
            else:
                account_id = session['id']
                cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (account_id, wiek, waga, wzrost, plec, papierosy, alkohol, aktywnosc))
                conn.commit()
                msg1 = 'Formularz uzupełniono pomyślnie!'
                return render_template("forms/basicform.html", msg=msg1, user=row)

        elif request.method == 'POST':
            msg1 = "Wszystkie pola formularza muszą zostać wypełnione!"
        return render_template("forms/basicform.html", msg=msg1, user=row)
    else:
        return redirect(url_for('login'))

# http://127.0.0.1:5000/basic/delete/ redirect
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


# ///////////////////////// ZAKŁADKI
# //GROUP INSERT
@app.route('/analyze', methods=['GET', 'POST'])
def insert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        account = cursor.fetchone()

        if account:
            InsertVacc()
            InsertCheck()
            InsertPrev()
            msg = 'Sprawdź stronę główną!'
            return render_template("forms/basicform.html", msg=msg, user=account)
        else:
            msg = 'Bez wypełnienia formularza analiza jest niemożliwa!'
            return render_template("forms/basicform.html", msg=msg, user=account)
    else:
        return redirect(url_for('login'))

# SZCZEPIENIA
@app.route('/analyze', methods=['GET', 'POST'])
def InsertVacc():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    current = 0
    todo = 1

    if 'loggedin' in session:
        id_user = session['id']

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        wn = cursor.fetchone()

        # Kleszczowe zapalenie mózgu
        if wn['wiek'] >= 1.5:
            nazwa = 'Kleszczowemu zapaleniu mózgu'
            typ = 'Zalecane'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            kleszcz = cursor.fetchone()
            if not kleszcz:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
                conn.commit()

        # Meningokoki
        if wn['wiek'] >= 0.5:
            nazwa = 'Meningokokom'
            typ = 'Zalecane'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            gruzlica = cursor.fetchone()
            if not gruzlica:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
                conn.commit()

        # Ludzki wirus brodawczaka
        if wn['wiek'] > 12:
            nazwa = 'Ludzkiemu wirusowi brodawczaka'
            typ = 'Zalecane'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            hpv = cursor.fetchone()
            if not hpv:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
                conn.commit()

        # Ospa wietrzna
        if wn['wiek'] > 1.5:
            nazwa = 'Na ospę wietrzną'
            typ = 'Zalecane'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            vzv = cursor.fetchone()
            if not vzv:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
                conn.commit()

        # Błonica
        if wn['wiek'] > 6:
            nazwa = 'Na błonicę'
            typ = 'Przypominające obowiązkowe'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            dtp = cursor.fetchone()
            if not dtp:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, typ, current, todo, nazwa))
                conn.commit()

        # Krzstusiec
        if wn['wiek'] > 6:
            nazwa = 'Na krztusiec'
            typ = 'Przypominające obowiązkowe'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            pert = cursor.fetchone()
            if not pert:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)',
                               (id_user, typ, current, todo, nazwa))
                conn.commit()

        # Świnka
        if wn['wiek'] > 6:
            nazwa = 'Na świnkę'
            typ = 'Przypominające obowiązkowe'
            cursor.execute('SELECT * FROM vacc WHERE nazwa = %s', nazwa)
            pig = cursor.fetchone()
            if not pig:
                cursor.execute('INSERT INTO vacc VALUES (NULL, %s, %s, %s, %s, %s)',
                               (id_user, typ, current, todo, nazwa))
                conn.commit()

        return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# http://localhost:5000/vaccines
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

# http://localhost:5000/vaccines/update
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

# http://127.0.0.1:5000/vaccines/delete/
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

# ClearAll from vaccines
@app.route('/vaccines/clear', methods=['GET', 'POST'])
def ClearVacc():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

            cursor.execute('DELETE FROM vacc WHERE id_user = %s', (session['id']))
            conn.commit()
            return redirect(url_for('Vacc'))
    else:
        return redirect(url_for('login'))



# KONTROLNE
def InsertCheck():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    current = 0
    todo = 1

    if 'loggedin' in session:
        id_user = session['id']

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        wn = cursor.fetchone()

        # Badanie prostaty
        if wn['plec'] == 0 and wn['wiek'] > 40:
            nazwa = "Badanie Prostaty"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            prst = cursor.fetchone()
            if not prst:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # Lipidogram
        if (wn['papierosy'] == 1 or wn['alkohol'] == 1 or wn['aktywnosc'] == 0) and wn['wiek'] > 40:
            nazwa = "Lipidogram"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            lip = cursor.fetchone()
            if not lip:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # Próby wątrobowe
        if (wn['papierosy'] == 1 or wn['alkohol'] == 1 or wn['aktywnosc'] == 0) and wn['wiek'] > 30:
            nazwa = "Próby wątrobowe"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            prw = cursor.fetchone()
            if not prw:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # EKG
        if wn['aktywnosc'] == 0 and wn['wiek'] > 40:
            nazwa = "EKG"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            ekg = cursor.fetchone()
            if not ekg:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # Mammografia
        if wn['plec'] == 1 and wn['wiek'] > 15:
            nazwa = "Mammografia"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            mamm = cursor.fetchone()
            if not mamm:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # Cytologia
        if wn['plec'] == 1 and wn['wiek'] > 15:
            nazwa = "Cytologia"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            prst = cursor.fetchone()
            if not prst:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # Marker CA 15-3
        if wn['plec'] == 1 and wn['wiek'] > 20:
            nazwa = "Badanie markerem nowotworowym CA 15-3"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            ca15 = cursor.fetchone()
            if not ca15:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # test na antygen sterczowy PSA
        if wn['plec'] == 0 and wn['wiek'] > 50:
            nazwa = "Badanie PSA, test na swoisty antygen sterczowy"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            psa = cursor.fetchone()
            if not psa:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()

        # Platysmografia
        if wn['papierosy'] == 1:
            nazwa = "Platysmografia, badanie czynności płuc"

            cursor.execute('SELECT * FROM check_ups where nazwa = %s', nazwa)
            plat = cursor.fetchone()
            if not plat:
                cursor.execute('INSERT INTO check_ups VALUES (NULL, %s, %s, %s, %s)', (id_user, current, todo, nazwa))
                conn.commit()
        return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# http://localhost:5000/check_ups
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

# http://localhost:5000/check_ups/update
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

# http://127.0.0.1:5000/check_ups/delete/
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

# ClearAll from check_ups
@app.route('/check_ups/clear', methods=['GET', 'POST'])
def ClearCheck():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

            cursor.execute('DELETE FROM check_ups WHERE id_user = %s', (session['id']))
            conn.commit()
            return redirect(url_for('Check'))
    else:
        return redirect(url_for('login'))



# PROFILAKTYKA/PREVENTION
def InsertPrev():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    current = 0
    todo = 1

    if 'loggedin' in session:
        id_user = session['id']

        cursor.execute('SELECT * FROM user WHERE account_id = %s', [session['id']])
        wn = cursor.fetchone()

        # Profilaktyka udarów
        if wn['wiek'] > 40 and (wn['alkohol']==1 or wn['papierosy'==1]):
            nazwa = "Profilaktyka udarów"
            link = 'pacjent.gov.pl/programy-profilaktyczne/program-profilaktyki-udarow'

            cursor.execute('SELECT * FROM prevention where nazwa = %s', nazwa)
            udr = cursor.fetchone()
            if not udr:
                cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, link, current, todo, nazwa))
                conn.commit()

        # Profilaktyka nowotworów skóry
        if wn['wiek'] > 50:
            nazwa = "Profilaktyka nowotworów skóry"
            link = 'pacjent.gov.pl/programy-profilaktyczne/profilaktyka-nowotworow-skory'

            cursor.execute('SELECT * FROM prevention where nazwa = %s', nazwa)
            mel = cursor.fetchone()
            if not mel:
                cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, link, current, todo, nazwa))
                conn.commit()

        # Profilaktyka raka płuca
        if wn['wiek'] > 55 and wn['papierosy'==1]:
            nazwa = "Profilaktyka raka płuca"
            link = 'pacjent.gov.pl/programy-profilaktyczne/profilaktyka-raka-pluca'

            cursor.execute('SELECT * FROM prevention where nazwa = %s', nazwa)
            rakp = cursor.fetchone()
            if not rakp:
                cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, link, current, todo, nazwa))
                conn.commit()

        # Profilaktyka raka płuca
        if wn['wiek'] > 55 and wn['papierosy'==1]:
            nazwa = "Profilaktyka raka płuca"
            link = 'pacjent.gov.pl/programy-profilaktyczne/profilaktyka-raka-pluca'

            cursor.execute('SELECT * FROM prevention where nazwa = %s', nazwa)
            rakp = cursor.fetchone()
            if not rakp:
                cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, link, current, todo, nazwa))
                conn.commit()

        # Profilaktyka osteoporozy
        if wn['wiek'] > 50 and wn['plec'==1]:
            nazwa = "Profilaktyka osteoporozy"
            link = 'pacjent.gov.pl/programy-profilaktyczne/profilaktyka-osteoporozy'

            cursor.execute('SELECT * FROM prevention where nazwa = %s', nazwa)
            osteo = cursor.fetchone()
            if not osteo:
                cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)', (id_user, link, current, todo, nazwa))
                conn.commit()

        # Profilaktyka próchnicy u młodzieży
        if wn['wiek'] > 15 and wn['wiek'] < 19:
            nazwa = "Profilaktyka próchnicy u młodzieży"
            link = 'pacjent.gov.pl/program-profilaktyczny/program-profilaktyki-prochnicy-zebow-dla-mlodziezy'

            cursor.execute('SELECT * FROM prevention where nazwa = %s', nazwa)
            zab = cursor.fetchone()
            if not zab:
                cursor.execute('INSERT INTO prevention VALUES (NULL, %s, %s, %s, %s, %s)',
                               (id_user, link, current, todo, nazwa))
                conn.commit()

        return redirect(url_for('Basic'))
    else:
        return redirect(url_for('login'))

# http://localhost:5000/prevention
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

# http://localhost:5000/vaccines/update
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

# http://127.0.0.1:5000/prevention/delete/
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

#ClearAll from prevention
@app.route('/prevention/clear', methods=['GET', 'POST'])
def ClearPrev():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

            cursor.execute('DELETE FROM prevention WHERE id_user = %s', (session['id']))
            conn.commit()
            return redirect(url_for('Prev'))
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

