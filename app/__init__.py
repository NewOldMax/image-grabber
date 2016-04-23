import sqlalchemy

DATABASE = 'image-grabber'
PASSWORD = 'gvj179qhw98R'
USER = 'root'
HOSTNAME = 'mysqlserver'

engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db