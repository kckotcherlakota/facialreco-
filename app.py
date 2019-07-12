from flask import Flask, render_template
from flask import send_file
from flask import send_from_directory
import pandas as pd
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash,g
from functools import wraps
import sqlite3

from flask import request,redirect, url_for
app = Flask(__name__)

# config
app.secret_key = 'my precious'
app.database = "sample.db"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = []

    for row in cur.fetchall():

      posts.append(dict(title=row[0],description=row[1]))


    print ("\nfor loop:\n{}\n".format(posts))

    g.db.close()
    return render_template('index.html',posts=posts)  # render a template
    # return "Hello, World!"  # return a string
#
#def downloadFile ():
#    path = "/home/krishna/Desktop/fa1/attta.xlsx"
#    return send_file(path, as_attachment=True)
#@app.route('/down', methods=['GET'])
#def download():
#    url = request.args['url']
#    filename = request.args.get('filename', 'atta.xlsx')
#    r = requests.get(url)
#    strIO = StringIO.StringIO(r.content)
#    return send_file(strIO, as_attachment=True, attachment_filename=filename)

# route for handling the login page logic
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

def connect_db():
    return sqlite3.connect(app.database)

@app.route("/downn")
def process():
#    df=pd.read_excel("/home/krishna/Desktop/fa1/attta.xlsx")
    df=pd.read_excel("attta.xlsx")
    return df.to_html()

@app.route('/exec')
def parse(name=None):
    import face_recog
    print("done")
    return render_template('index.html',name=name) 


@app.route('/exec2')
def parse1(name=None):
	import face_recog
	print("done")
	return render_template('index.html',name=name)

if __name__ == '__main__':
    app.run()
   