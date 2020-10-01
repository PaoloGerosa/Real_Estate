# Import Standard libraries
from Credenziali import inserisciCredenzialiDatabase
from Logging import Log
import logging

# Connect to logger
Log()
logger=logging.getLogger()
import itertools

def SearchingInDB(location):

    mydb = inserisciCredenzialiDatabase()
    mycursor = mydb.cursor()
    location = f'"{location}"'
    mycursor.execute(f'select URL from Immobili2 where URL is not Null and localita =' + location)
    Lista_aux = mycursor.fetchall()
    Lista = list(itertools.chain(*Lista_aux))
    print(Lista)

    return Lista
    # It prints into the logging file