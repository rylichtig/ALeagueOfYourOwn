from flask import Flask, render_template, g, request, redirect, url_for, session, flash

import MySQLdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key 111'

def get_db_connection():
	try:
		return (g.conn, g.cursor)
	except AttributeError:
		pass

	conn = MySQLdb.connect(host='107.170.238.89', user='root', passwd='daniel', db='leaguedb', charset='utf8')
	
	g.conn = conn
	g.cursor = conn.cursor()
	return (conn, g.cursor)
	

@app.route('/')
def home():
	
	(conn, cursor) = get_db_connection()
	
	cursor.execute('SELECT first_name, last_name, email FROM Users')
	query_results = cursor.fetchall()
	
	users = []
	for result in query_results:
		users.append({ 'first_name' : result[0], 
					   'last_name' : result[1],
					   'email' : result[2] })
					   
	session['some_key'] = 'some_value'
	
	return render_template("index.html", users=users, results=query_results)

@app.route('/ryan')
def ryan():
	session_value = session['some_key']
	return session_value

	return "Personal page"

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
	if request.method == 'POST':
		first_name = request.form['firstname']
		last_name = request.form['lastname']
		email = request.form['email']
		password = request.form['password']
		query = '''INSERT INTO Users (first_name, last_name, email, password)
				   VALUES (%s, %s, %s, %s)'''
				   
		(conn, cursor) = get_db_connection()		   
		cursor.execute(query, (first_name, last_name, email, password))		   
		conn.commit()
				   
		return redirect(url_for('home'))
	else:
		return render_template("create_account.html")
		
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		query = '''SELECT 1
				   FROM Users 
				   WHERE email = %s AND password = %s'''
		
		(conn, cursor) = get_db_connection()		   
		cursor.execute(query, (email, password))
		query_results = cursor.fetchall()
		
		if query_results:
			# Correct sign in
			flash('Signed in okkkkk')
			session['email'] = email
			return redirect(url_for('home'))
		else:
			# Flash an error message.
			flash('Email or Password incorrect')
			return redirect(url_for('sign_in')) 
				   
		
	else:
		# Render all flashed error messages.
		return render_template("sign_in.html")

if __name__ == '__main__':
    app.run(debug = True)

