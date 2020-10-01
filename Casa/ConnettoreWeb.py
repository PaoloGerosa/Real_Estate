# Import standard libraries
import requests
from bs4 import BeautifulSoup

# It returns the text of the page
def estrattoreDatiPagineSito(localita, pagina, mod):

    # It builds the link of the selected page
    link = costruttoreLinkPaginaSito(localita, pagina)
    # Exctract text
    soup = cucinaZuppa(link)

    # Return text
    # mod = True: return normal page for search
    # mod = False: return number oh houses available (for streamlit App)
    if mod:
        testoPagina = soup.find('div', class_='list')
    else:
        # It exctracts and cleans the number of houses on the website
        testoPagina = soup.find('div', class_='heading').text
        testoPagina = testoPagina.lstrip()
        testoPagina = testoPagina.split(' ')[0]
        testoPagina = int(testoPagina.replace('.',''))
        # In Casa.it the maximum number of houses returned is 600 (30 pages)
        if testoPagina > 600:
            testoPagina = 600
    return testoPagina


# It builds the link of the selected page
def costruttoreLinkPaginaSito(localita, pagina):

    if pagina == 1:
        link = f'https://www.casa.it/vendita/residenziale/{localita}'
    else:
        link = f'https://www.casa.it/vendita/residenziale/{localita}/?page={pagina}'
    return link

# It builds the link of the selected page
def costruttoreLinkPaginaImmobile(localita, pagina):

    if pagina == 1:
        link = f'https://www.casa.it/vendita/residenziale/{localita}'
    else:
        link = f'https://www.casa.it/vendita/residenziale/{localita}/?page={pagina}'
    return link

# Exctract lxml
def cucinaZuppa(URL):

    source = requests.get(URL).text
    soup = BeautifulSoup(source, 'lxml')
    return soup

