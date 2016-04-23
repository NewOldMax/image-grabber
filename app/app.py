from flask import Flask, request, render_template, redirect, url_for
from model import RequestItem, Image, db
from forms import GrabberForm
import simplejson as json
from sqlalchemy.exc import IntegrityError
from grab import Grab
import os
import urllib
import random
import logging

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

downloader = urllib.URLopener()

# initate flask app
app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    db.session.rollback()
    form = GrabberForm()
    if form.validate_on_submit():
        g = Grab()
        g.setup(log_file='log.html', connect_timeout=5, timeout=5)
        g.go(form.site_url.data)
        status = 'inprogress'
        title = g.doc.select('//title').text()
        request_item = RequestItem(
            form.site_url.data,
            form.image_count.data,
            title,
            status)
        db.session.add(request_item)
        index = 0
        for image in g.doc.select('//img'):
            if (index >= form.image_count.data):
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
        db.session.commit()
    return render_template('form.html', 
        form = form,
        requests = RequestItem.query.all())

@app.route('/<int:request_id>', methods=['GET'])
def get_request_item(request_id):
    return render_template('request_item.html', 
        item = RequestItem.query.get(request_id))

@app.route('/createtbl')
def createUserTable():
	try:
		db.create_all()
		return json.dumps({'status':True})
	except IntegrityError:
		return json.dumps({'status':False})

if __name__ == "__main__":
	app.config['SECRET_KEY'] = 'dkfj273hf784h1dj98q'
	app.run(host="0.0.0.0", port=8082, debug=True)

