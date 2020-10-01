from Casa.ConnettoreWeb import cucinaZuppa

# Insert the further data
def DatiAvanzati(immobile):

    # Construct the lxml
    soup = cucinaZuppa(immobile.getURL())

    # Search of different further infos (Check Seleziona Info)
    testoPagina = soup.find('div', class_='characteristics')
    for info in testoPagina.div.ul.find_all('li'):
        immobile = SelezionaInfo(info.text, immobile)

    # Setting Energetic Class
    if soup.find('div', class_='energy-rating').div.div is not None:
        classeEnergetica = soup.find('div', class_='energy-rating').div.div.span.text
        immobile.setClasseEnergetica(classeEnergetica)

    # Exctract latitude and longitude
    if soup.find('div', class_='ad-map') is not None:
        coordinate = soup.find('div', class_='ad-map')
        i = 0
        infoCoordinate = None
        for coo in coordinate.div.ul.find_all('li'):
            if i == 1:
                infoCoordinate = coo.a['href']
                break
            i = i+1

        latitudine  = infoCoordinate.split('cbll=')[1].split(',')[0]
        longitudine = infoCoordinate.split(',')[1].split('&')[0]

        # Setting of latitude and longitude
        immobile.setLatitudine(float(latitudine))
        immobile.setLongitudine(float(longitudine))

    try:
        codicecasa = soup.find('div', class_='contact-reccomended')
        codicecasa = codicecasa.find('div', class_='code-rif')
        for testo in codicecasa.ul.find_all('li'):
            pass
        codicecasa = testo.b.text
        if len(codicecasa) < 250:
            immobile.setCodiceCasa(codicecasa)
    except:
        pass

    # Even infos on locals
    UniformaInfo(immobile)

    # Return building update
    return immobile

# Exctract some further infos
def SelezionaInfo(info, immobile):
    if info.split(':')[0]   == 'Bagni':
        immobile.setBagni(info.split(':')[1])
    elif info.split(':')[0] == 'Piano':
        immobile.setPiano(info.split(':')[1])
    elif info.split(':')[0] == 'Anno di costruzione':
        immobile.setAnnodiCostruzione(info.split(':')[1])
    elif info.split(':')[0] == 'Condizioni':
        immobile.setStato(info.split(':')[1])
    elif info.split(':')[0] == 'Riscaldamento':
        immobile.setRiscaldamento(info.split(':')[1])
    elif info.split(':')[0] == 'Tipologia':
        immobile.setTipologia(info.split(':')[1])

    # Return building update
    return immobile

def UniformaInfo(immobile):
    # Even infos on locals
    locali = immobile.getLocali()
    if locali is not None and len(locali)>1:
        locali=locali[0]
    try:
        locali = int(locali)
    except:
        locali = None
    immobile.setLocali(locali)

    # Even infos on baths
    bagni = immobile.getBagni()
    try:
        bagni = int(bagni[0])
    except:
        bagni = None
    immobile.setBagni(bagni)

    # Even infos on box
    box = immobile.getBoxPostoAuto()
    try:
        box = int(box[0])
    except:
        if box == 'box auto' or box == '1 posto auto':
            box = 1
        elif box == 'box 2 auto' or box == '2 posti auto':
            box = 2
        elif box == 'box 3 auto' or box == '3 posti auto':
            box = 3
        elif box == 'box 4 auto' or box == '4 posti auto':
            box = 4
    try:
        immobile.setBoxPostoAuto(box)
    except:
        immobile.setBoxPostoAuto(None)

    # Even infos on conditions
    stato = immobile.getStato()
    # 1: da ristrutturare, 2: abitabile
    # 3: ristrutturato, 4: nuovo oppure in costruzione
    if stato == 'da ristrutturare' or stato == 'Da ristrutturare':
        stato = 1
    elif stato ==  'abitabile' or stato == 'Buono / Abitabile':
        stato = 2
    elif stato == 'ristrutturato' or stato == 'Ottimo / Ristrutturato':
        stato = 3
    elif stato == 'in costruzione' or stato == 'nuovo' or stato == 'Nuovo / In costruzione':
        stato = 4
    try:
        immobile.setStato(stato)
    except:
        immobile.setStato(None)

    return immobile