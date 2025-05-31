from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dbms123',  # Replace with your DB password
        database='society_finance',
        port=3305
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/expenses')
def expenses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM expenses ORDER BY id DESC')
    expenses = cursor.fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM income ORDER BY id DESC')
    income_data = cursor.fetchall()

    cursor.execute('SELECT SUM(amount) AS total_expense FROM expenses')
    total_expense = cursor.fetchone()['total_expense']

    cursor.execute('SELECT SUM(amount) AS total_income FROM income')
    total_income = cursor.fetchone()['total_income']

    conn.close()
    return render_template('dashboard.html', income_data=income_data, total_expense=total_expense, total_income=total_income)

@app.route('/income')
def income():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM income ORDER BY id DESC')
    income = cursor.fetchall()
    conn.close()
    return render_template('income.html', income=income)

@app.route('/members')
def members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM members ORDER BY id DESC')
    members = cursor.fetchall()
    conn.close()
    return render_template('members.html', members=members)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if request.method == 'POST':
        purpose = request.form['purpose']
        amount = request.form['amount']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (purpose, amount) VALUES (%s, %s)', (purpose, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('expenses'))

@app.route('/add_income', methods=['POST'])
def add_income():
    if request.method == 'POST':
        source = request.form['source']
        amount = request.form['amount']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO income (source, amount) VALUES (%s, %s)', (source, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('income'))

@app.route('/add_member', methods=['POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO members (name, contact) VALUES (%s, %s)', (name, contact))
        conn.commit()
        conn.close()
        return redirect(url_for('members'))

if __name__ == '__main__':
    app.run(debug=True)
