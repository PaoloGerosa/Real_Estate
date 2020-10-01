# Import standard libraries
import requests
from bs4 import BeautifulSoup
import time
from Logging import Log
import logging

# Connect to logger
Log()
logger=logging.getLogger()

# It returns the text of the page
def estrattoreDatiPagineSito(localita, pagina, mod):

    # It builds the link of the selected page
    link = costruttoreLinkPaginaSito(localita, pagina)
    # Exctract text
    soup = cucinaZuppa(link)
    # Return text
    # mod = 1: return normal page for search
    # mod = 0: return number oh houses available (for streamlit App)
    if mod:
        try:
            testoPagina = soup.find('ul', class_='annunci-list')
        except:
            testoPagina = None
    else:
        try:
            # It exctracts and cleans the number of houses on the website
            testoPagina = soup.find('div', class_='summary-row clearfix raleway left-side-listing').span.text
            testoPagina = testoPagina.lstrip()
            testoPagina = testoPagina.split(' ')[0]
            testoPagina = int(testoPagina.replace('.',''))
        except:
            testoPagina = None
    return testoPagina


# It builds the link of the selected page
def costruttoreLinkPaginaSito(localita, pagina):

    if pagina == 1:
        link = f'https://www.immobiliare.it/vendita-case/{localita}/?criterio=rilevanza&noAste=1'
    else:
        link = f'https://www.immobiliare.it/vendita-case/{localita}/?criterio=rilevanza&noAste=1&pag={pagina}'
    return link


# Exctract lxml
def cucinaZuppa(URL):
    # It may happen that, after a lot of researches in immobiliare.it the server blocks for a few seconds
    # the requests so we pause the program for 5 seconds and then we continue
    while True:
        try:
            source = requests.get(URL).text
            soup = BeautifulSoup(source, 'lxml')
            break
        except:
            logger.info("Connessione rifiutata dal server..")
            logger.info("Pausa di 5 secondi")
            logger.info("Zzzzzz...")
            time.sleep(5)
            logger.info("Finito il riposo, ora continuo...")
    return soup


