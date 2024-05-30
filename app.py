from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
from supabase import create_client, Client

url: str = "https://qfvhmlzvghklouupxezm.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmdmhtbHp2Z2hrbG91dXB4ZXptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwMzQzNTEsImV4cCI6MjAzMjYxMDM1MX0.y3aQ072BHdHdnto0ynEblWURkRV__o9RGCsI055Q6z0"
supabase: Client = create_client(url, key)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    data, count = supabase.table('tasks').select("*").execute()
    print(data)
    return render_template('index.html', tasks=data[1], count=len(data[1]))

@app.route('/add-task', methods=['POST'])
def add_task():
    task = request.form['task']
    supabase.table('tasks').insert({"task": task}).execute()
    return redirect(url_for('index'))

@app.route('/delete-task/<id>', methods=['POST'])
def delete_task(id):
    supabase.table('tasks').delete().eq('id', id).execute()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    user, count = supabase.table('users').select("*").eq('email', email).eq('password', password).execute()
    if user[1]:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    email = request.form['email']
    password = request.form['password']
    supabase.table('users').insert({"email": email, "password": password}).execute()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)