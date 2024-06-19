from flask import Flask, render_template
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/hello')
def home():
    return "Hello world"

@app.route('/about')
def about():
    return "page is loading...."
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Seema@8827',
        database='users'
    )
    return connection

@app.route('/users')
def users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('users.html', users=users)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, email,role) VALUES (%s, %s,%s)', (name, email,role))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('users'))
    return render_template('new_user.html')

@app.route('/users/<int:id>')
def user_detail(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user is None:
         abort(404)
    return render_template('user_detail.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)

