# Import Standard libraries
from mysql import connector
from Credenziali import inserisciCredenzialiDatabase

# update Database
def aggiornaDatabase(lista):

    # Credentials to access your database
    mydb = inserisciCredenzialiDatabase()

    # Initialize cursor
    mycursor = mydb.cursor()
    sqlFormula = 'INSERT INTO immobili2 (ID, Ora, Sito, Localita,' \
                 'Headline, URL, Prezzo, Locali, Superficie, ' \
                 'Bagni, Ratio, BoxPostoAuto, Piano, ' \
                 'AnnodiCostruzione, Stato, Riscaldamento, ClasseEnergetica, ' \
                 'Via, Lat, Lon, CodiceCasa) ' \
                 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


    # Database update cicle
    for elem in lista:

        # Vector to insert in the database
        vet = [elem.ID, elem.Ora, elem.Sito, elem.Localita, elem.Headline, elem.URL, elem.Prezzo, elem.Locali, elem.Superficie,
               elem.Bagni, elem.Ratio, elem.BoxPostoAuto, elem.Piano,
               elem.AnnodiCostruzione, elem.Stato, elem.Riscaldamento, elem.ClasseEnergetica,
               elem.Via, elem.Latitudine, elem.Longitudine, elem.CodiceCasa]

        # Execute and commit
        mycursor.execute(sqlFormula, vet)
        mydb.commit()
