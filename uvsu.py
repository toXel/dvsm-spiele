#!/usr/bin/env python2.7

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_pyfile('config.py')

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def all_scores():
	cur = g.db.execute('select gameid, gametitle, gameurl, user1score, user2score, (user1score > user2score and higherisbetter) or (user1score < user2score and not higherisbetter), (user2score > user1score and higherisbetter) or (user2score < user1score and not higherisbetter), unit, higherisbetter, sort from scores order by sort')
	#((abs(user1score-user2score))/(user1score+user2score))
	scores = [dict(gameid=row[0], gametitle=row[1], gameurl=row[2], user1score=row[3], user2score=row[4], user1gewinnt=row[5], user2gewinnt=row[6], unit=row[7], higherisbetter=row[8], sort=row[9]) for row in cur.fetchall()]
	return render_template('scores.html', scores=scores)

@app.route('/add', methods=['POST'])
def new_game():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST' and request.form['gametitle']:
		g.db.execute('insert into scores (gametitle, gameurl, user2score, user1score, higherisbetter, unit) values (?, ?, 0, 0, ?, ?)', [request.form['gametitle'], request.form['gameurl'], request.form['higherisbetter'], request.form['unit']])
		g.db.commit()
		flash('Spiel hinzugefuegt.')
		return redirect(url_for('all_scores'))
	else:
		flash('Kein Titel eingegeben.')
		return redirect(url_for('all_scores'))


@app.route('/update', methods=['POST'])
def update_score():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST' and request.form['game'] != "none":
		user1score = 0
		user2score = 0
		gameid = request.form['game']
		if request.form['user1score']:
			user1score = int(request.form['user1score'])
		if request.form['user2score']:
			user2score = int(request.form['user2score'])
		if user1score:
			g.db.execute('update scores set user1score=? where gameid=?', [user1score, gameid])
		if user2score:
			g.db.execute('update scores set user2score=? where gameid=?', [user2score, gameid])
		g.db.commit()
		update_sort(request.form['game'])
		flash("Score aktualisiert.")
		return redirect(url_for('all_scores'))
	else:
		flash("Kein Spiel ausgewaehlt.")
		return redirect(url_for('all_scores'))

@app.route('/delete', methods=['POST'])
def remove_game():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST' and request.form['game'] != "none":
		g.db.execute('delete from scores where gameid=?',[request.form['game']])
		g.db.commit()
		flash("Spiel entfernt.")
		return redirect(url_for('all_scores'))
	else:
		flash("Kein Spiel ausgewaehlt.")
		return redirect(url_for('all_scores'))

@app.route('/edit', methods=['POST'])
def edit_game():
	if not session.get('logged_in'):
		abort(401)
	if request.method == 'POST' and request.form['game'] != "none":
		if (not request.form['gametitle'] and not request.form['gameurl'] and not request.form['higherisbetter'] and not request.form['unit']) or not request.form['game']:
			flash('Nichts geaendert.')
			return redirect(url_for('all_scores'))
		if request.form.get('edit_gametitle'):
			g.db.execute('update scores set gametitle=? where gameid=?', [request.form['gametitle'], request.form['game']])
			g.db.commit()
		if request.form.get('edit_gameurl'):
			g.db.execute('update scores set gameurl=? where gameid=?', [request.form['gameurl'], request.form['game']])
			g.db.commit()
		if request.form.get('edit_higherisbetter'):
			g.db.execute('update scores set higherisbetter=? where gameid=?', [request.form['higherisbetter'], request.form['game']])
			g.db.commit()
		if request.form.get('edit_unit'):
			g.db.execute('update scores set unit=? where gameid=?', [request.form['unit'], request.form['game']])
			g.db.commit()
		update_sort(request.form['game'])
		flash('Spiel bearbeitet.')
		return redirect(url_for('all_scores'))


def update_sort(gameid):
	cur = g.db.execute('select gameid, gametitle, gameurl, user1score, user2score, (user1score > user2score and higherisbetter) or (user1score < user2score and not higherisbetter), (user2score > user1score and higherisbetter) or (user2score < user1score and not higherisbetter), unit, higherisbetter, sort from scores where gameid=?', [gameid])
	scores = [dict(gameid=row[0], gametitle=row[1], gameurl=row[2], user1score=row[3], user2score=row[4], user1gewinnt=row[5], user2gewinnt=row[6], unit=row[7], higherisbetter=row[8], sort=row[9]) for row in cur.fetchall()]
	for score in scores:
<<<<<<<<< saved version
		sortvalue = 100.0*(max(score['user1score'],score['user2score'])) / (score['user2score']+score['user1score'])
=========
		sortvalue = 100.0*(max(score['user1score'],score['user2score'])) / (score['user2score']+score['user1score'])
>>>>>>>>> local version
		if not score['higherisbetter']:
			sortvalue = 100-sortvalue
		g.db.execute('update scores set sort = ? where gameid=?', [sortvalue, score['gameid']])
		g.db.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME_1'] and request.form['username'] != app.config['USERNAME_2']:
			error = 'invalid username'
		elif request.form['password'] != app.config['PASSWORD_1'] and request.form['password'] != app.config['PASSWORD_2']:
			error = 'invalid password'
		else:
			session ['logged_in'] = True
			flash('Eingeloggt.')
			return redirect(url_for('all_scores'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Ausgeloggt.')
	return redirect(url_for('all_scores'))

if __name__ == '__main__':
	app.run(host='0.0.0.0')