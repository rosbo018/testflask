from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import Form, StringField, validators
from secrets import SystemRandom
rand = SystemRandom()
app = Flask(__name__)
app.secret_key = "asd"

secureString1 = "test1"
secureString2 = "test2"

tempdb = {"Alice": "12345"}
phIdLst = []


def test(a, b):
    return a + b


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/fail')
def fail():
    session['username'] = ""
    return render_template('fail.html')


@app.route('/session')
def retSession():
    return str(session.items())
@app.route('/clrsess')
def clearSession():
    session.clear()
    session["isvalid"] = False
    session["isLogin"] = False
    return redirect(url_for('retSession'))


class loginForm(Form):
    pid = StringField('pid',
                      [validators.DataRequired(),
                       validators.Length(min=1, max=25)])
    pwd = StringField('pwd',
                      [validators.DataRequired(),
                       validators.Length(min=1, max=25)])


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(session['isvalid'])
    form = loginForm(request.form)

    if (not session['isvalid']):
        return redirect(url_for('fail'))

    if request.method == 'POST':
        print("pid = " + session['pid'])
        phone_id = request.form['pid']
        password = request.form['pwd']
        print(phone_id, password)
        session['passwd'] = password

        if (phone_id == session['phone_id']):
            session['phone_id'] = ""
            session['isLogin'] = True
            return redirect(url_for('ret'))

        return redirect(url_for('fail'))
    return render_template('login.html', form=form)


def fa(name, phone_number):
    code = [chr(rand.randrange(65, 90)) for i in range(4)]
    code = "".join(code)
    session['phone_id'] = code
    print("code = " + code)
    return True

@app.route('/return')
def ret():
    return "password: " + session['passwd'] +'strings: ' + secureString1 + " : " + secureString2


class registerForm(Form):
    name = StringField('Name',
                       [validators.DataRequired(),
                        validators.Length(min=1, max=25)])
    # if tempdb[name]:
    #     fa(tempdb[name])
    # else:
    #     "no user of " + name


@app.route('/register', methods=['GET', 'POST'])
def registerRoute():
    form = registerForm(request.form)
    session['isvalid'] = False
    session['isLogin'] = False
    if request.method == 'POST':
        name = request.form['Name']
        session['username'] = name
        print("validated")
        print(name)

        if name in tempdb and fa(name, tempdb[name]):
            session['isvalid'] = True
            return redirect(url_for('login'))
        else:
            return redirect('/fail')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
