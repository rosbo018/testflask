from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import Form, StringField, validators
from secrets import SystemRandom
from authy.api import AuthyApiClient



rand = SystemRandom()
def generateCode(length):
    code = [chr(rand.randrange(65, 90)) for i in range(length)]
    code = "".join(code)
    return code


app = Flask(__name__)
app.secret_key = generateCode(5)

secureString1 = "test1"
secureString2 = "test2"

tempdb = {"Alice": "12345"}
phIdLst = []
print("start")


def getAuthyClient():
    return AuthyApiClient("ACa6afa063a01266953d8031f0cea5c1a5")


@app.route('/')
def index():
    return redirect(url_for('registerRoute'))


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
        print("pid = " + session['phone_id'])
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
    code = generateCode(4)
    session['phone_id'] = code
    msg = "\n " + code


    print("code = " + code)
    return True


@app.route('/return')
def ret():
    return "password: " + session['passwd'] + " , strings: " + secureString1 + " : " + secureString2


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
