from mysql import connector

# Insert credentials to use mysql database
def inserisciCredenzialiDatabase():

    mydb = connector.connect(
        host='localhost',     # if not changed: localhost
        user='root',          # if not changed: root
        passwd='',    # password mysql
        database='casadb')

    return mydb
