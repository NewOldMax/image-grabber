from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# Database Configurations
app = Flask(__name__)
DATABASE = 'image-grabber'
PASSWORD = 'gvj179qhw98R'
USER = 'root'
HOSTNAME = 'mysqlserver'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class RequestItem(db.Model):
	__tablename__ = 'request_item'
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(255))
	title = db.Column(db.String(255))
	status = db.Column(db.String(255))
	count = db.Column(db.String(255))
	images = db.relationship("Image", lazy='dynamic')
	info = db.Column(db.String(255))

	def __init__(self, url, count, title, status):
		self.url = url
		self.title = title
		self.status = status
		self.count = count

class Image(db.Model):
	__tablename__ = 'image_item'
	id = db.Column(db.Integer, primary_key=True)
	request_id = db.Column(db.Integer, db.ForeignKey('request_item.id'))
	request = db.relationship('RequestItem', foreign_keys=request_id)
	orig_url = db.Column(db.String(255))
	file_name = db.Column(db.String(255))

	def __init__(self, request, orig_url, file_name):
		self.request = request
		self.orig_url = orig_url
		self.file_name = file_name

if __name__ == '__main__':
    manager.run()