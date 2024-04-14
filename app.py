from flask import Flask, jsonify, render_template, request, url_for, session, redirect
from database import load_home, load_homes, add_apply, add_home, load_apply

app = Flask(__name__)

app.secret_key = '12345'
users = {'Udbhav': '1234', 'Aaditya': '12345678', 'Admin': 'admin'}


@app.route('/')
def hello_world():
  homes = load_homes()
  return render_template('home.html', homes=homes)


@app.route('/api/homes')
def list_homes():
  return jsonify(load_homes())


@app.route('/home/<id>')
def show_home(id):
  home = load_home(id)
  if not home:
    return "Home not found", 404
  return render_template('homepage.html', home=home)


@app.route('/api/home/<id>')
def show_homes(id):
  home = load_home(id)
  return jsonify(home)


@app.route('/home/<id>/apply', methods=['post'])
def apply_home(id):
  data = request.form
  home = load_home(id)
  add_apply(id, data)
  return render_template("application_submit.html", apply=data, home=home)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
      session['username'] = username
      return redirect(url_for('admin'))

  return render_template('login.html')


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('hello_world'))


@app.route('/admin')
def admin():
  username = session.get('username')
  if 'username' in session:
    return render_template('admin.html', username=username)
  else:
    return redirect(url_for('login'))


@app.route('/home/add')
def add_homes():
  if 'username' in session:
    return render_template('add_home.html')
  else:
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
  apply = load_apply()
  if 'username' in session:
    return render_template('dashboard.html', apply=apply)
  else:
    return redirect(url_for('login'))


@app.route('/home/saved', methods=['post'])
def saved():
  data = request.form
  add_home(data)
  return render_template('saved.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
