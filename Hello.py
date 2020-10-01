"""An example of showing geographic data."""
# Import libraries
import streamlit as st
import pandas as pd
from Credenziali import inserisciCredenzialiDatabase
from Casa.ConnettoreWeb import estrattoreDatiPagineSito as Casa
from Immobiliare.ConnettoreWeb import estrattoreDatiPagineSito as Immobiliare
from Main import main

global LOCPREDEFINITA
# title and explanation in the website
st.title("Real Estate in Italy")
st.markdown(
"""
This is a demo of a Streamlit app that shows the houses available in different Italian cities.
Use the slider to pick a specific location and look at how the charts change.
""")
# important function so that the app is dynamic
@st.cache(persist=True)

def load_data(location, columns, columns_aux):
    # It connects to the database
    mydb = inserisciCredenzialiDatabase()
    location = f'"{location}"'

    # Columns for the Raw data
    # Creation of the total columns (the standard ones plus the ones chosen by the user
    tot = ''
    for elem in columns:
        tot = tot + ',' + elem
    for elem in columns_aux:
        tot = tot + ',' + elem
    tot = tot[1:]

    # It exctracts from the database only the infos requested by the users
    data = pd.read_sql(f'SELECT {tot} FROM immobili2 Where lat is not Null and lon is not Null'
                       f' and Localita =' + location, con=mydb)
    data = data.replace('latitudine', 'lat')
    # Compulsory for the Geo data representation
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data

def house(location, stato):
    # It connects to the database
    mydb = inserisciCredenzialiDatabase()
    location = f'"{location}"'
    # It selects the best house associated to the location and status given by the user
    # To be improved
    data = pd.read_sql('SELECT URL, Prezzo '
                        'FROM immobili2 '
                        f'where Localita = {location} '
                        'and Ratio is not Null '
                        f'and Stato = {stato} '
                        'and Ratio <= all(select Ratio from immobili2 '
                        f'where Localita={location} and Ratio is not Null and Stato={stato})'
                        , con=mydb)
    return data

def locate():
    # It connects to the database
    mydb = inserisciCredenzialiDatabase()
    # It selects all the different locations available on the database
    data = pd.read_sql(f'SELECT distinct localita FROM immobili2 ', con=mydb)
    # Compulsory for the Geo data representation
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data

# locations is the variable of the different cities in the database
locations = locate()['localita']
# Formula exctracts a list of the locations available in the database
Formula = []
for nome in locations:
    Formula.append(nome)
# location Selectbox is the widget of the website that let the users choose the location
location = st.selectbox(
    'What location would you like to see?',
    (Formula)
)

# columns_aux is the multiselect widget that allows users to choose the data that they want to see
columns_aux = st.multiselect("Choose Data",("Sito", "Località",
                 "Headline", "URL", "Prezzo", "Locali", "Superficie",
                 "Bagni", "Ratio", "BoxPostoAuto", "Piano",
                 "AnnodiCostruzione", "Stato", "Riscaldamento", "ClasseEnergetica",
                 "Via", "CodiceCasa"))
columns = ['Headline', 'lat', 'lon']

# data is the total data selected from the database
# checkbox allows users to choose if they want to see the raw data or not
data = load_data(location, columns, columns_aux)
if st.checkbox("Show Raw data", False):
    st.subheader("Raw data" )
    st.write(data)

# these let users choose to see the Geo data of the location
if st.checkbox("Show Geo data", True):
    f'## Geo data of {location}'
    if st.button(f"Press to see Geo data of {location}"):
        st.map(data)

# Status of the house that users want
stato = st.selectbox(
    'Which status of the house would you like?',
    ('To be restructured', 'Habitable', 'Excellent / Restructured', 'New / In construction')
)
# Convertion to numbers
if stato == 'To be restructured':
    stato = 1
elif stato == 'Habitable':
    stato = 2
elif stato == 'Excellent / Restructured':
    stato = 3
elif stato == 'New / In construction':
    stato = 4
# Subtitle
st.subheader("This is the first house to buy")

# It export the best house based on location and status
house = house(location, stato)
URL = house['URL'][0]
URL

# Search toolbox to let users search the place that they want
firstlocation = st.text_input("Enter the location to search","Type here...")
# If button pressed then the search starts
if st.button("Submit"):
    result = firstlocation.title()
    st.success(f'Ricerca iniziata su {result.capitalize()}')
    result = result.replace(' ', '_')
    # pagine_casa and pagine_immobiliare are the total pages to search of the different websites
    pagine_casa = int(Casa(result, 1, 0))
    pagine_immobiliare = int(Immobiliare(result, 1, 0))
    tot_page = [int(pagine_casa/20) + (pagine_casa%20>0), int(pagine_immobiliare/25) + (pagine_immobiliare%25>0)]
    # It launches the main code
    main(0,result,tot_page)
    data = load_data(result, columns, [])
    'data', data