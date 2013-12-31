from flask import Flask,url_for,render_template
app = Flask(__name__)

@app.route('/')
def index(): pass

@app.route('/login',methods=['POST','GET'])
def login(): 
	error = None
	if request.method == 'POST':
		if valid_login(request.form['username'],
					   request.form['password']):
			return log_the_user_in(request.form['username'])
		else:
			error = 'Invalid username/password'
	return render_template('login.html', error = error)

@app.route('/user/<username>')
def profile(username): pass

@app.route('/hello/')
@app.route('/hello/<username>')
def hello_guy(username=None):
    return render_template('hello.html',username = username)

@app.route('/hello/<int:usernum>')
def the_usernum(usernum):
	return 'Your are the %sth person on the website!' % usernum

with app.test_request_context():
	print url_for('index')
	print url_for('login')
	print url_for('login',next='/')
	print url_for('profile', username = 'Cloud Wang')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
