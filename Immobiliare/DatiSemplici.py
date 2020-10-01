# It inserts the first data in the realestate
def DatiSemplici(immobile, data):

    # Exctract the text
    corpoTesto = data.find('div', class_='listing-item_body')
    paragrafo = 0

    # Setting title
    immobile.setHeadline(corpoTesto.div.p.a['title'])
    # Setting URL
    immobile.setURL(corpoTesto.div.p.a['href'])
    # Setting price
    prezzo = corpoTesto.div.ul.li.text
    # if price is not available no price
    if prezzo == 'PREZZO SU RICHIESTA':
        immobile.setPrezzo(None)
    else:
        # Cleaning up
        prezzo = prezzo.replace('€', '')
        prezzo = prezzo.replace(' ', '')
        prezzo = prezzo.replace('\n', '')
        try:
            prezzo = int(prezzo.replace('.', ''))
        except:
            prezzo = None
        immobile.setPrezzo(prezzo)

    # # Setting Local, Surface and baths
    for info in corpoTesto.div.ul.find_all('li', class_='lif__item'):
        if info.find('div', class_='lif__text lif--muted') is not None:
            testo = info.find('div', class_='lif__text lif--muted').text
            if len(testo.split(' ')) > 1:
                testo = testo.split(' ')[20]
                testo = testo.split('\n')[0]
        else:
            testo=None
        if testo == 'locali':
            immobile.setLocali(info.div.text)
        if testo == 'superficie':
            superficie=info.div.text
            if len(info.div.text.split('.')) == 2:
                superficie=superficie.replace('.', '')
            try:
                superficie=int(superficie.split('m')[0])
            except:
                superficie=None
            immobile.setSuperficie(superficie)
        if testo == 'bagni':
            immobile.setBagni(info.div.text)

    # If price and surface available then it sets the ratio
    try:
        immobile.setRatio(int(float(prezzo / superficie)))
    except:
        immobile.setRatio(None)

    # It returns the update building
    return immobile

