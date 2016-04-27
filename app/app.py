import simplejson as json
import logging

from flask import Flask, request, render_template, redirect, url_for, copy_current_request_context
from flask_socketio import SocketIO
from model import RequestItem, db
from forms import GrabberForm
from sqlalchemy.exc import IntegrityError
from grab import Grab
from spider import Spider


logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# initate flask app
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
    form = GrabberForm()    
    return render_template('form.html', 
        form = form,
        requests = list(reversed(RequestItem.query.all())))

@app.route('/<int:request_id>', methods=['GET'])
def get_request_item(request_id):
    return render_template('request_item.html', 
        item = RequestItem.query.get(request_id))

@app.route('/createtbl')
def createTable():
	try:
		db.create_all()
		return json.dumps({'status':True})
	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/droptbl')
def dropTable():
    try:
        db.drop_all()
        return json.dumps({'status':True})
    except IntegrityError:
        return json.dumps({'status':False})

@socketio.on('grab')
def grab(data):
    bot = Spider()
    bot.initial_urls = [data['site_url']]
    bot.total = data['image_count']
    bot.status = 'inprogress'
    bot.run()

if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'dkfj273hf784h1dj98q'
    socketio.run(app, host="0.0.0.0", port=8082, debug=True)
