# Import useful functions
from Immobiliare.ConnettoreWeb import *
from Immobiliare.DatiSemplici import DatiSemplici
from Immobiliare.DatiAvanzati import DatiAvanzati
from Immobiliare.AggiornaDatabaseSQL import aggiornaDatabase
from Immobiliare.Immobile import Immobile
from Logging import Log
import datetime
import logging
import streamlit as st

# Connect to logger
Log()
logger=logging.getLogger()

# Main code of the website
# if type is true the code is called from the local pc and it prints all the info in the logger
# if type is false the code is called from the website and you don't update the logger
def Main(localita, ora, ID, mod, type, tot_page, my_bar):

    # Initialization of simple variables
    if type:
        logger.info("Immobiliare.it")
    sito = "Immobiliare.it"
    oraLunga = f'{ora.day}/{ora.month}/{ora.year}  {ora.hour}:{ora.minute}'
    if type:
        oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
        logger.info(f"Inizio della Ricerca di Immobili su {sito}")

    # Initialization variables to scroll the research
    listaImmobili = []
    numeroCase = 0
    pagina = 1

    # Start research
    while True:

        # Select actual page
        paginaAttuale = estrattoreDatiPagineSito(localita, pagina, 1)
        # If the page does not exist then we end the research
        if paginaAttuale is None:
            break

        # Logger update
        if type:
            oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
            logger.info(f"Pagina Numero {pagina}")

        # It scrolls all the buildings in the page
        # for cicle with iterative variable
        nomi = [' listing-item--wide ', ' listing-item--small ', ' listing-item--tiny ',
                ' listing-item--medium ', ' ']
        for dettaglio in nomi:
            for data in paginaAttuale.find_all('li', class_=f'listing-item{dettaglio}js-row-detail'):

                # Extract and create a single building
                if data is not None:

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
            my_bar.progress((tot_page[0]+pagina)/(tot_page[0] + tot_page[1]))

        # Change page
        pagina = pagina + 1

    # Remove temporaly the progress bar in the website (only if type is false)
    if not type:
        my_bar.empty()

    # End of research
    if type:
        print("La ricerca su", pagina-1, "pagine ha trovato", numeroCase, "immobili su", sito)
        logger.info(f"La ricerca su {pagina - 1} pagine ha trovato {numeroCase} immobili su {sito}")

    # Update Database
    aggiornaDatabase(listaImmobili)

    # Update logging
    oraBreveAttuale = f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'
    if type:
        logger.info("Database Aggiornato")
        logger.info(f"Fine della Ricerca di Immobili su {sito}")



    
