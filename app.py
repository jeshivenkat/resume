from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from config import db_config

app = Flask(__name__)
app.secret_key = 'secret123'

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, message))
            conn.commit()
            flash('Message submitted successfully!', 'success')
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect('/contact')

    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')


if __name__ == '__main__':
    app.run(debug=True)