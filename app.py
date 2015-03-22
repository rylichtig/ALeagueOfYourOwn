from flask import Flask, render_template, g

import MySQLdb

app = Flask(__name__)

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
	
	return render_template("index.html", users=users, results=query_results)

@app.route('/ryan')
def ryan():
	return "Personal page"

@app.route('/create_account')
def create_account():
	return render_template("create_account.html")

if __name__ == '__main__':
    app.run(debug = True)

