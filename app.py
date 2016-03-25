from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'queen'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

cursor = conn.cursor()

@app.route("/")
def main():
    return render_template('index.html')


@app.errorhandler(500)
def internal_server_error(e):
    return 'hello -500'


@app.route('/signup')
def showSignUp():
    return render_template('signup.html')


@app.route('/createuser', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    _hashed_password = generate_password_hash(_password)

    if _name and _email and _password:
        cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully'})
        else:
            return json.dump({'error': str(data[0])})

    else:
        return json.dumps({'html': '<span> Enter the required fields. <span>'})

if __name__ == "__main__":
    app.run()
