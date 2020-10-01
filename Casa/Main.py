# Import useful functions
from Casa.ConnettoreWeb import *
from Casa.DatiSemplici import DatiSemplici
from Casa.DatiAvanzati import DatiAvanzati
from Casa.AggiornaDatabaseSQL import aggiornaDatabase
from Casa.Immobile import Immobile
from Logging import Log
import datetime
import logging
from SearchingLists import SearchingInDB
import streamlit as st

# Connect to logger
Log()
logger=logging.getLogger()

# Main code of the website
# if type is true the code is called from the local pc and it prints all the info in the logger
# if type is false the code is called from the website and you don't update the logger
def Main(localita, ora, ID, mod, type, tot_page):

    # Initialization of simple variables
    if type:
        logger.info("Casa.it")
    sito = "Casa.it"
    oraLunga = f'{ora.day}/{ora.month}/{ora.year}  {ora.hour}:{ora.minute}'
    if type:
        oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
        logger.info(f"Inizio della Ricerca di Immobili su {sito}")

    # Initialization variables to scroll the research
    listaImmobili = []
    numeroCase = 0
    pagina = 1
    testoIniziale = None

    # Initialization progress bar in the website (only if type is false)
    if not type:
        my_bar = st.progress(0)

    # Exctract the list of URL items (if the location has been called yet) from the database
    DBlist = SearchingInDB(localita)

    # Start research
    while True:

        # Select actual page
        paginaAttuale = estrattoreDatiPagineSito(localita, pagina, 1)

        # If it's the first page, we save it
        if testoIniziale is None:
            testoIniziale = paginaAttuale.find('article')
        # If we're not on the first page and the html is the same of the one in the first page
        # we exit the research
        # This happens because a link to a non existent page is the same of the first page
        elif paginaAttuale.find('article') == testoIniziale:
            break
        if pagina == 31:
            break

        # Logger update
        if type:
            oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
            logger.info(f"Pagina Numero {pagina}")

        # It scrolls all the buildings in the page
        # for cicle with iterative variable
        for data in paginaAttuale.find_all('article'):

            Link = 'https://www.casa.it' + data.find('div', class_='infos').div.p.a['href']
            if Link in DBlist:
                print ('yes')
            else:
                print('no')
            # Extract and create a single building
            if data != None :

                # Create the building through the class
                immobile = Immobile(ID, oraLunga, sito, localita)

                # Update building infos
                immobile = DatiSemplici(immobile, data)
                immobile = DatiAvanzati(immobile)

                # List of buildings
                numeroCase = numeroCase + 1
                if mod:
                    print("    Scheda Casa Numero", numeroCase, ":")
                    print(immobile.scheda())
                listaImmobili.append(immobile)

        if not type:
            my_bar.progress(pagina / (tot_page[0] + tot_page[1]))

        # Change page
        pagina = pagina + 1

    # End of research
    if type:
        print("La ricerca su", pagina-1, "pagine ha trovato", numeroCase, "immobili su", sito)
        logger.info(f"La ricerca su {pagina-1} pagine ha trovato {numeroCase} immobili su {sito}")

    # Update Database
    aggiornaDatabase(listaImmobili)

    # Update logging
    if type:
        oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
        logger.info("Database Aggiornato")
        logger.info(f"Fine della Ricerca di Immobili su {sito}")

    if not type:
        return(my_bar)
