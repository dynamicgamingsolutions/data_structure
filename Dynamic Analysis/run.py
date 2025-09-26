import os
import sys
import pymssql
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(dir_path, 'security'))
sys.path.insert(0, os.path.join(dir_path, 'sql'))
sys.path.insert(0, os.path.join(dir_path, 'static'))
from flask import Flask, request, jsonify, render_template, Blueprint, redirect, url_for, session
from revenue import revenue_bp

app = Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(revenue_bp, url_prefix='/revenue')

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.cache_control.proxy_revalidate = True
    response.cache_control.max_age = 0
    return response

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = pymssql.connect(server='192.168.1.195', user='paulc', password='092@290Mxx', database='analytics')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analytics.dbo.credentials WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return jsonify({'redirect': url_for('revenue.home')})
        else:
            return jsonify({'message': 'Login failed', 'loggedIn': False})

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)