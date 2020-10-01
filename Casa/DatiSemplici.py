# It inserts the first data in the realestate
def DatiSemplici(immobile, data):

    # Exctract the text
    corpoTesto = data.find('div', class_='infos')
    paragrafo = 0

    # Setting of the road
    immobile.setVia(corpoTesto.div.p.a.text)

    # Inner research
    for info in corpoTesto.div.find_all('p'):
        if paragrafo == 0:
            # Setting title
            if (len(info.a['title']))<150:
                immobile.setHeadline(info.a['title'])
        paragrafo = paragrafo + 1

    # URL setting
    immobile.setURL('https://www.casa.it' + corpoTesto.div.p.a['href'])
    ps = corpoTesto.find('div', class_='features')


    # Exctract price
    prezzo = ps.p.text
    if prezzo != 'Trattativa riservata':
        if len(prezzo.split('T')) > 1:
            prezzo = prezzo.split('T')[0].split('€')[1]
            prezzo = int(prezzo.replace('.', ''))
            # Setting price
            immobile.setPrezzo(prezzo)

    # Interior of the house
    for info in ps.ul.find_all('li'):
        if info.span is not None:
            if info.span.text == 'mq':
                superficie = info.text
                if len(superficie.split(' ')) == 2:

                    # Setting surface (Case 1)
                    superficie = int(superficie.split('m')[0])
                    immobile.setSuperficie(superficie)

                    # Check if the price is available
                    # Ratio: price/surface
                    try:
                        immobile.setRatio(int(float(prezzo) / superficie))
                    except:
                        immobile.setRatio(None)

                else:

                    # Setting surface (Case 2)
                    try:
                        superficie = int(superficie.split('m')[0])
                        immobile.setSuperficie(superficie)
                    except:
                        pass

            # Setting locals
            elif info.span.text == 'locali':
                locali = info.text
                immobile.setLocali(locali.split(' ')[0])

    # Search box
    if ps.ul.find('li', class_='box') is not None:
        postoAuto = ps.ul.find('li', class_='box').text
        # Setting box
        immobile.setBoxPostoAuto(postoAuto)

    # It returns the update building
    return immobile
