# Import all the main functions
from Database import resetDatabase
from Database import tabellaDuplicati
from Database import rimozioneDuplicati
from Casa.Main import Main as Casa
from Immobiliare.Main import Main as Immobiliare
from Logging import Log
import datetime
import logging

# Create log file and connect to it
Log()
logger = logging.getLogger()

# First of all go to mysql and create a new database called casadb, then positionate
# into the database by double-tap its name
# Modify the file Credential.py with your mysql credentials

def selezionaLocalita(richiesta, type):
    # If requests "True" it asks for a new search zone (Italian city)
    if type[0]:
        if richiesta:
            localita = input('Inserisci località da cercare: ')
            # Change spaces into dashes
            localita = localita.replace(' ', '_')

        # If requests "True" it uses the default location
        else:
            localita = LOCPREDEFINITA
            # Change spaces into dashes
            localita = localita.replace(' ', '_')
    else:
        localita = type[1]

    return localita.lower()

def impostazioniRicerca(richiesta, type):
    # It sets datetime and ID
    ora = datetime.datetime.now()
    ID = 1
    # It chooses the location
    localita = selezionaLocalita(richiesta, type)
    return [ora, ID, localita]

def lanciaRicerca(ra, loc, mod, reset, type, tot_page):
    # It resets the table in the database if requested
    if reset:
        logger.info("Inizializzazione Database")
        resetDatabase()

    # It collects the search parametres
    if type[0]:
        [ora, ID, localita] = impostazioniRicerca(loc, [type[0], None])
    else:
        [ora, ID, localita] = impostazioniRicerca(loc, [type[0], type[1]])

    # It prints into the logging file a starting-research message
    if type[0]:
        logger.info(f"Inizio della Ricerca di Immobili a {localita.title().replace('_', ' ')}")

    # It begins the research on the chosen websites
    if ra[0]:
        if not type[0]:
            my_bar = Casa(localita, ora, ID, mod, type[0], tot_page)
        else:
            Casa(localita, ora, ID, mod, type[0], tot_page)
    if ra[1]:
        if not type[0]:
            Immobiliare(localita, ora, ID, mod, type[0], tot_page, my_bar)
        else:
            Immobiliare(localita, ora, ID, mod, type[0], tot_page, None)

    # It prints into the logging file an ending-research message
    if type[0]:
        logger.info(f"Fine della Ricerca di Immobili a {localita.title().replace('_', ' ')}")

# CODE EXECUTED
# mod_st is the mode of the code:
# if mod_st is true then the search is a local search for the pc
# if mod_st is false it means that the main has been called from the website page (from a user)
# if mod_st is false loc_st is the location that the user wants (None if mod_st is false)
# tot_page is the total page of the location searched
# (it's important for the progressive bar in the website)

def main(mod_st, loc_st, tot_page):
    # Select Location type True/False
    # True  -> requested to the user;
    # False -> default location;
    sceltaLocalita = False

    # default location
    global LOCPREDEFINITA
    LOCPREDEFINITA = "Merone"

    # Select the active websites True/False
    # -> 0: Casa;
    # -> 1: Immobiliare;
    ricercheAttive = [True, True]

    # It print into the terminal the buildings info
    # True  -> It writes all the cards
    # False -> It only counts the number of buildings
    modalitaStampa = False

    # Reset the initial database
    # True  -> reset
    # False -> don't reset
    reset = False

    # It creates a duplicate table to allow to remove the duplicates
    tabellaDuplicati()

    # Flash the search
    lanciaRicerca(ricercheAttive, sceltaLocalita, modalitaStampa, reset, [mod_st,loc_st], tot_page)

    # Removes all the duplicates in the final table
    rimozioneDuplicati()

# Option if called as File Main
if __name__ == '__main__':
    main(1, None, None)
