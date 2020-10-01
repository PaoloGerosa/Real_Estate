from Immobiliare.ConnettoreWeb import cucinaZuppa

# Insert the further data
def DatiAvanzati(immobile):

    # Construct the lxml
    soup = cucinaZuppa(immobile.getURL())

    # Search of different further infos (Check Seleziona Info)
    if soup.find('section', class_='im-structure__mainContent') is not None:
        testoPagina = soup.find('section', class_='im-structure__mainContent')
        contatore=0
        if testoPagina.find('dl', class_='im-features__list') is not None:
            for info in testoPagina.find_all('dl', class_='im-features__list'):
                VettoreValori = []
                for ausiliario in testoPagina.find_all('dd'):
                    VettoreValori.append(ausiliario.text)
                for testo in info.find_all('dt'):
                    testo=testo.text
                    try:
                        valore = VettoreValori[contatore].replace('\n','')
                        valore = valore.strip()
                    except:
                        valore = None
                    immobile = SelezionaInfo(testo, valore, immobile)
                    contatore = contatore+1

    # Setting of the road
    try:
        info = soup.find('nd-map', class_='nd-ratio nd-ratio--wide im-map__mapInpage im-map__container')
        Via = None
        # Road is the last information in div.span
        for ausiliario in info.div.find_all('span'):
            Via=ausiliario.text
        immobile.setVia(Via.lower())
    except:
        immobile.setVia(None)

    # Exctract latitude and longitude
    try:
        Latitudine = float(str(soup).split('"latitude":')[1].split(',')[0])
        Longitudine = float(str(soup).split('"longitude":')[1].split(',')[0])
        immobile.setLatitudine(Latitudine)
        immobile.setLongitudine(Longitudine)
    except:
        pass

    # Even infos on locals
    UniformaInfo(immobile)

    # Return building update
    return immobile

# Exctract some further infos
def SelezionaInfo(testo, valore, immobile):
    if testo == 'box e posto auto':
        immobile.setBoxPostoAuto(valore.split(',')[0])
    elif testo == 'riferimento e Data annuncio':
        if len((valore.split(' -')[0]))<250:
            immobile.setCodiceCasa(valore.split(' -')[0])
    elif testo == 'piano':
        immobile.setPiano(valore.split(',')[0])
    elif testo == 'anno di costruzione':
        immobile.setAnnodiCostruzione(valore)
    elif testo == 'stato':
        immobile.setStato(valore)
    elif testo == 'riscaldamento':
        immobile.setRiscaldamento(valore)
    elif testo == 'Classe energetica':
        immobile.setClasseEnergetica(valore[0])

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
        box = int(box)
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
        box=int(box[0])
    except:
        pass
    try:
        immobile.setBoxPostoAuto(box)
    except:
        immobile.setBoxPostoAuto(0)

    # Even infos on conditions
    stato = immobile.getStato()
    # 1: da ristrutturare, 2: abitabile
    # 3: ristrutturato, 4: nuovo oppure in costruzione
    if stato == 'da ristrutturare' or stato == 'Da ristrutturare':
        stato = 1
    elif stato == 'abitabile' or stato == 'Buono / Abitabile':
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
