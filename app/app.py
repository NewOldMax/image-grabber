import simplejson as json
import logging
import urllib
import eventlet
import os
import random

from flask import Flask, request, render_template, redirect, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit
from model import RequestItem, Image, db
from forms import GrabberForm
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from grab import Grab
from spider import Spider


logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


downloader = urllib.URLopener()

# initate flask app
app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True, log_output=True)


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

@socketio.on('grab_crawler', namespace='/main')
def grab_crawler(data):
    bot = Spider()
    bot.initial_urls = [data['site_url']]
    bot.total = data['image_count']
    bot.result_status = 'inprogress'
    bot.run()

@socketio.on('grab_single', namespace='/main')
def grab_single(data):
    g = Grab()
    g.setup(log_file='log.html')
    g.go(data['site_url'])
    total = data['image_count']
    status = 'inprogress'
    title = g.doc.select('//title').text()
    request_item = RequestItem(
       data['site_url'],
       total,
       title,
       status)
    db.session.add(request_item)
    index = 0
    info = 'All images grabbed'
    for image in g.doc.select('//img'):
        try:
            if (index >= total):
                status = 'success'
                break
            src = image.attr('src')
            hash = os.urandom(16).encode('hex')
            filename = hash + src.split('/')[-1]
            downloader.retrieve(src, 'app/static/images/' + filename)
            image_item = Image(
                request_item,
                src,
                filename)
            db.session.add(image_item)
            index += 1
            emit('grabed_count', index, namespace='/main')
            eventlet.sleep(0)
        except Exception as e:
            continue
    if (index != total):
        status = 'error'
        info = 'Not of all images grabbed'
    request_item.status = status
    request_item.info = info
    db.session.commit()
    db.session.expire(request_item)
    emit('finish', 'saving', namespace='/main')
    eventlet.sleep(0)

def after_commit_listener(mapper, connection, target):
    emit('finish', 'finish', namespace='/main')

event.listen(RequestItem, 'after_insert', after_commit_listener)

if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'dkfj273hf784h1dj98q'
    socketio.run(app, host="0.0.0.0", port=8082, debug=True)
