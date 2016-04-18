import MySQLdb
from constants import *
def connect_db():
    global db
    db = MySQLdb.connect(host=hostname,user=user,passwd=password,db=dbname)

if __name__ == '__main__':
    # Testing stuff
    connect_db()
