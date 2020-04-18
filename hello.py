from flask import Flask, send_from_directory
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html')
	
@app.route('/start/')
def about():
    return render_template('start.html')
	
if __name__ == '__main__':
    app.run(debug=True)