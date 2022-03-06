# Real_Estate

These are the steps done in this project: 
- Web scraping to download and collect data available online about Houses sold in Italy (Python, HTML).
- Data cleaning to mantain a neat database of houses (SQL).
- Advanced statistical and machine learning methods to predict the prices (R, Python).
- Development of a model of prevision of prices in different areas with an average error of 150 e/m2.
Only the ones related to Python code, in particular to the Web scraping part, are presented in Github.

# Code

The user must put in input the name of the city in which he/she is interested.
In 'Immobiliare' and 'Casa' folders there are all the scripts related to the downloading of the HTML of two different popular Real Estate websites in Italy, Casa.it and Immobiliare.it.
From the HTML 'DatiSemplici.py' and 'DatiAvanzati.py' scrape the pages to save only the useful information of the different houses sold.
'Streamlit.py' is the script associated to the webapplication developed using the Python library Streamlit to present the data and to suggest in output different houses to buy according to the algorithm.
'Main.py' gathers information of the houses and saves them in a local Database using mysql connector.

## Authors
* [Matteo Tomasetto](https://github.com/MatteoTomasetto)
* [Paolo Gerosa](https://github.com/PaoloGerosa)
* [Francesco Romeo](https://github.com/fraromeo)
* [Luca Sosta](https://github.com/SostaLuca98)
