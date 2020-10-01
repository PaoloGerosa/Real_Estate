# Import Standard libraries
from Credenziali import inserisciCredenzialiDatabase
import datetime
global STDDATABASE
from Logging import Log
import logging

# Connect to logger
Log()
logger=logging.getLogger()

STDDATABASE = ' (ID varchar(50), Ora varchar(50), Sito varchar(50),' \
              'Localita varchar(50), Headline varchar(150), URL varchar(150), Prezzo int, ' \
              'Locali int, Superficie int, Bagni int, Ratio float(4), ' \
              'BoxPostoAuto int, Piano varchar(50), AnnodiCostruzione varchar(150), ' \
              'Stato int, Riscaldamento varchar(150), ClasseEnergetica varchar(150), ' \
              'Via varchar(150), Lat float(4), Lon float(4), CodiceCasa varchar(250))'

# Create the table in the Database
def creaDatabase():

    mydb = inserisciCredenzialiDatabase()
    mycursor = mydb.cursor()
    mycursor.execute('CREATE TABLE immobili2' + STDDATABASE)

    # It prints into the logging file
    oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
    logger.info("Database Creato")


# Funzione per Resettare il Database
def resetDatabase():

    mydb = inserisciCredenzialiDatabase()
    mycursor = mydb.cursor()
    try:
        mycursor.execute('DROP TABLE immobili2')
    except:
        logger.info("Nessun Database Cancellato")
    mycursor.execute('CREATE TABLE immobili2' + STDDATABASE)

    # It prints into the logging file
    oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
    logger.info("Database Azzerato")


# Drop the table
def cancellaDatabase():
    mydb = inserisciCredenzialiDatabase()
    mycursor = mydb.cursor()
    mycursor.execute('DROP TABLE immobili2')
    # Stampa Resoconto a Terminale
    oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
    logger.info("Database Azzerato")

# Create the duplicate_table
def tabellaDuplicati():
    mydb = inserisciCredenzialiDatabase()
    mycursor = mydb.cursor()
    try:
        mycursor.execute('DROP TABLE duplicato_immobili')
    except:
        pass
    mycursor.execute('CREATE TABLE duplicato_immobili ' + STDDATABASE)

def rimozioneDuplicati():
    mydb = inserisciCredenzialiDatabase()
    mycursor = mydb.cursor()
    # Put all the duplicates in the duplicate_table
    mycursor.execute('INSERT INTO duplicato_immobili select '
                     '* from immobili2 as I '
                     'where I.sito = "Immobiliare.it" '
                     'and (I.Prezzo, I.Superficie, I.Locali) in '
                     '(select Prezzo, Superficie, Locali from immobili2 as C where C.sito = "Casa.it")')
    mydb.commit()
    # Remove all the duplicates from the original table
    mycursor.execute('DELETE immobili2 from immobili2 '
                     'WHERE (Prezzo, Superficie, Locali) IN '
                     '(SELECT Prezzo, Superficie, Locali FROM duplicato_immobili)')
    mydb.commit()
    # Update the original table
    mycursor.execute('INSERT INTO immobili2 '
                     'select * '
                     'from duplicato_immobili')
    mydb.commit()
    # Drop the duplicate_table
    mycursor.execute('drop table duplicato_immobili')

    tabellaDuplicati()
    mycursor.execute('INSERT INTO duplicato_immobili select '
                     '* from immobili2 as I '
                     'where I.sito = "Immobiliare.it" '
                     'and (I.CodiceCasa) in '
                     '(select CodiceCasa from immobili2 as C where C.sito = "Casa.it")')
    mydb.commit()
    # Remove all the duplicates from the original table
    mycursor.execute('DELETE immobili2 from immobili2 '
                     'WHERE CodiceCasa IN '
                     '(SELECT CodiceCasa FROM duplicato_immobili)')
    mydb.commit()
    # Update the original table
    mycursor.execute('INSERT INTO immobili2 '
                     'select * '
                     'from duplicato_immobili')
    mydb.commit()
    # Drop the duplicate_table
    mycursor.execute('drop table duplicato_immobili')


# CODE EXECUTED
# Remember to use your credentials
# Interface to use preferred options
def main():
    while True:
        scelta = input("\nScegli la Funzione:\n"
                        "(1) Crea il Database\n"
                        "(2) Cancella il Database\n"
                        "(3) Resetta il Database\n"
                        "(0) Esci\n"
                        "Numero Scelto -> ")

        # Convert String -> Number
        numero = int(scelta)

        # Select
        if numero == 0: break
        if numero == 1: creaDatabase()
        if numero == 2: cancellaDatabase()
        if numero == 3: resetDatabase()


# Option if called as a File Main
if __name__ == '__main__':
    main()
