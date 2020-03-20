import mysql.connector
import random


def collaborative(gebruiker, cursor, product):
    """"Deze functie is de main loop voor de collaborative filteren"""
    profid = """select distinct profid from sessions where segment = (%s)"""
    cursor.execute(profid, (segment(cursor, gebruiker),))
    profiles = cursor.fetchall() # Profielen die hetzelfde segment hebben als de gebruiker

    osgebruikers = os(cursor, gebruiker, profiles) # Profielen die ook nog ongeveer hetzelfde os systeem gebruiken

    zelfdegeslacht = allegeslachten(cursor, gebruiker, osgebruikers) # Profielen die ook nog waarschijnlijk van hetzelfde geslacht zijn

    prodid = """select prodid from profiles_previously_viewed where profid = (%s)"""
    cursor.executemany(prodid, zelfdegeslacht)
    prod = cursor.fetchall() # Alle producten die de profielen bij elkaar hebben gekocht

    eenvanelke = []

    for i in prod:
        if i not in eenvanelke:
            eenvanelke.append(i) # We stoppen één van elk product in 'eenvanelke'

    GP = gebprod(cursor, gebruiker)
    LGP = []

    for i in GP:
        LGP.append(i[0])

    for i in eenvanelke: # Hier haal ik alle producten weg die de gebruiker al gekocht heeft
        if i in LGP:
            eenvanelke.remove(i)

    recommendations = []
    if len(eenvanelke) >= 4: # Als we al genoeg materiaal hebben voor recommendations
        hoeveelelke = []

        for i in eenvanelke:
            hoeveelelke.append(prod.count(i))  # We kijken hoe vaak een product voorkomt

        tel = 4
        while tel != 0: # We stopen de producten die door de meeste mensen werden gekocht in de recommendations
            maxi = max(hoeveelelke)
            welke = hoeveelelke.index(maxi)
            recommendations.append(eenvanelke[welke])
            tel -= 1
    else: # Als we niet genoeg materiaal hebben voor recommendations
        for i in eenvanelke:
            recommendations.append(i)
        extrarecom(recommendations, cursor, product) # Hiermee vullen we 'recommendations' aan tot we vier recommendations hebben
    return recommendations


def content(product, cursor, categorie):
    """Deze functie is de main loop voor de content filteren"""
    eenlijst = anderen(cursor, product) # Welke producten kochten anderen die dit ook kochten
    p = sorteren(eenlijst) # Sorteert de lijst op meest gekochte producten

    recommendations = []

    if len(eenlijst) >= 4 or product[0][0] != 'null': # Als we al genoeg materiaal hebben pakken we de meest gekochte producten
        for i in range(1, 5):
            recommendations.append((p[-i])[0]) # Pakt de meest gekochte producten
    else:
        recommendaties = categorien(product, categorie[0][0], categorie[0][1], cursor) # Kijkt welke producten in dezelfde
        # subcategorie maar niet in dezelfde subsubcategorie zitten

        if (len(recommendations) + len(eenlijst)) >= 4: # Als er te veel recommendaties zijn
            for i in range(0, (4 - len(eenlijst))):
                eenlijst.append(random.choice(recommendations)) # Pakt een paar random recommendations
            return eenlijst

        elif categorie[0][0] != 'null': # Als er wel een categorie is
            extrarecom(recommendaties, cursor, product) # Pakt een paar andere recommendations
            return recommendaties

        else:
            extrarecom(recommendations, cursor, product)
    return recommendations


def gebprod(cursor, gebruiker):
    """Pakt alle product.id'en die een gebruiker heeft gekocht"""
    cat = """select prodid from profiles_previously_viewed where profid = (%s)"""
    cursor.execute(cat, gebruiker)
    prod = cursor.fetchall()
    products = []

    for j in prod:
        splt = j[0].split('\r')[0]
        products.append((int(splt),))
    return products


def watbenik(lst):
    """Kijkt welk element uit een lijst het vaakst voorkomt"""
    veel = []
    for i in lst:
        veel.append(lst[i])

    welke = max(veel)

    for i in lst:
        if lst[i] == welke:
            antwoord = i
    return antwoord


def allegeslachten(cursor, gebruiker, profiles):
    """Gokt welk geslacht de gebruiker is aan de hand van de producten die hij heeft gekocht en kijkt dan welke andere
    gebruikers ook dit geslacht hebben"""
    geslachten = [['Vrouwen', 'Vrouw', 'Zwangere vrouw', "Baby's", 'Baby'], ['Man', 'Mannen', 'Kantoor', 'kantoor'],
                  ['Kinderen', 'Meisje', 'Jongen'], ['Volwassenen', '50+', '65+', 'volwassene'],
                  ['Unisex', 'Mannen/vrouwen', 'Grootverpakking']]

    sekse = geslacht(cursor, gebruiker, geslachten) # Waarschijnlijk geslacht gebruiker
    if sekse == 'null': # Als de gebruiker vooral producten heeft gekeken die geen geslacht als specificatie hebben
                        # Kunnen we niet makkelijk zijn geslacht raden dus returnen we alle profielen
        return profiles
    else:
        rest = []

        for i in profiles: # Bekijkt geslacht van elk profiel. En als die overeenkomt met de gebruiker slaan we m op.
            if geslacht(cursor, i, geslachten) == sekse:
                rest.append(i)
        return rest


def geslacht(cursor, gebruiker, geslachten):
    """"In deze functie gokken we aan de hand van de gekochte producten van de gebruiker wat zijn of haar geslacht is.
    Of tenminste wat de targetaudience is."""
    prod = gebprod(cursor, gebruiker)
    geslacht = """select targetaudience from products where id = (%s)"""
    sekse = []

    for i in range(0, len(prod)):
        cursor.execute(geslacht, prod[i])
        sekse.append(cursor.fetchall()[0][0]) # Geslacht van een product van de gebruiker

    lst = {
        'Vrouwen': 0, 'Mannen': 0, 'Kinderen': 0, 'Volwassenen': 0, 'null': 0, 'Unisex': 0
    }

    for i in sekse: # Kijkt hoeveel producten van de gebruiker vallen onder de categorien in lst
        if i in geslachten[0]:
            lst['Vrouwen'] += 1
        elif i in geslachten[1]:
            lst['Mannen'] += 1
        elif i in geslachten[2]:
            lst['Kinderen'] += 1
        elif i in geslachten[3]:
            lst['Unisex'] += 1
        elif i == 'null':
            lst['null'] += 1
        elif i in geslachten[4]:
            lst['Volwassenen'] += 1
    return watbenik(lst) # Returned het gegokte geslacht


def os(cursor, gebruiker, profiles):
    """Bekijkt welke os de gebruiker gebruikt en welke andere gebruikers ook dit os gebruiken"""
    os = gebruikeros(cursor, gebruiker) # Os van gebruiker
    derest = []

    for i in profiles:
        if gebruikeros(cursor, i) == os:
            derest.append(i)
    derest.remove(gebruiker)
    return derest # Returned alle andere gebruikers met hetzelfde os


def gebruikeros(cursor, gebruiker):
    """Kijkt welk os de gebruiker het vaakst gebruikt"""
    category = """select os from sessions where profid = (%s)"""
    cursor.execute(category, gebruiker)
    os = cursor.fetchall() # Alle os systemen die de gebruiker in vorige sessies heeft gebruikt
    ossplt = []

    for i in os: # Er waren teveel categorien dus ik heb ervoor gekozen om alleen het eerste woordje te pakken zodat
                 # (bijvoorbeeld) Windows 7 en Windows 10 allebei onder Windows vallen.
        ossplt.append(i[0].split(' ')[0])

    lst = {
        'Windows': 0, 'Android': 0, 'iOS': 0, 'Chrome': 0, 'Mac': 0, 'Linux': 0, 'Ubuntu': 0, 'Tizen': 0,
        'Other': 0, 'Fedora': 0, 'Blackberry': 0, 'Firefox': 0, 'FreeBSD': 0, 'OpenBSD': 0, 'Solaris': 0
    }

    for i in ossplt:
        for j in lst:
            if i == j:
                lst[j] += 1
    return watbenik(lst) # Kijkt welk os het vaakst voorkomt


def segment(cursor, gebruiker):
    """Kijkt welk segment het vaakst aan de gebruiker gekoppeld wordt"""
    segment = """select segment from sessions where profid = (%s)"""
    cursor.execute(segment, gebruiker)
    segments = cursor.fetchall() # Alle segments van de gebruiker zijn vorige sessies

    lst = {
        'BOUNCER': 0, 'BROWSER': 0, 'COMPARER': 0, 'BUYER': 0, 'LEAVER': 0, 'FUN_SHOPPER': 0,
        'null': 0, 'JUDGER': 0
    }

    for i in segments:
        for j in lst:
            if i[0] == j:
                lst[j] += 1
    return watbenik(lst) # Returned de segment waaraan de gebruiker het vaakst gekoppeld wordt


def anderen(cursor, product):
    """In deze functie kijken we naar een product. Vervolgens kijken naar welke andere gebruikers ook dit product
     hebben gekocht. En dan kijken we welke producten zij allemaal hebben gekocht. Als andere gebruikers veel dezelfde
     producten hebben gekocht, kan het product relaties hebben met deze andere producten."""
    categorie = """select profid from profiles_previously_viewed where prodid = (%s)"""
    cursor.execute(categorie, product)
    gebruikers = cursor.fetchall() # Welke profielen hebben hetzelfde product gekocht?
    producten = []

    for i in gebruikers:
        for j in i:
            producten.append(j[0])

    nieuw = []
    aantal = []

    for i in producten: # Neemt van elk product één
        if i not in nieuw:
            nieuw.append(i)

    nieuw.remove(str(product[0])) # Haalt het product zelf weg (anders zou de engine het product aanraden waar je op klikt)

    for i in nieuw: # Als het product vaker dan twee keer langs komt slaan we het op (dit kan makkelijk aangepast worden)
        hoeveel = producten.count(i)
        if hoeveel > 2:
            aantal.append([i, hoeveel])
    return aantal # Returned een lijst met product.id's en hoe vaak deze voorkomen


def categorien(product, cate, subcate, cursor):
    """Deze functie kijkt welke producten in dezelfde subcategorie vallen maar niet in dezelfde subsubcategorie zitten"""
    lst = []
    categorie = """select id, subcategory, subsubcategory from products"""
    cursor.execute(categorie)
    records = cursor.fetchall() # Alle id's, subcategorien en subsubcategorien

    for i in records:
        if i[0] == product:
            continue
        elif i[1] == cate and i[2] != subcate:
            lst.append(i[0])
    return lst


def sorteren(lst):
    """Bekijkt welke producten het vaakst voorkomen en sorteert daarop"""
    tellen = 0
    while True:
        getal = 0
        for i in range(0, len(lst) - 1):
            tellen += 1
            if lst[i][1] > lst[i + 1][1]:
                getal += 1
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
        if getal == 0:
            break
    return lst


def extrarecom(recommendations, cursor, product):
    """Deze functie is een laatste resort. Ik kijk wat het product.id is en pak de volgende. Ik merkte op dat
    sommige soortgelijke producten vaak naast elkaar staan dus zo heb je nog een kans om een gerelateerd product te pakken"""
    hoelang = 4 - len(recommendations)
    prodid = """select id from products"""
    cursor.execute(prodid)
    record = cursor.fetchall()
    waar = record.index(product)

    for i in range(0, hoelang):
        recommendations.append(record[waar + i])


def begin():
    """Zoals de naam doet vermoeden begint hier het hele proces"""
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='Voer hier je wachtwoord in',
        database="Voer hier je database in"
    )

    cursor = database.cursor()

    while 1:
        welke = input('Wil je de collaborative of de content recommendations?: ')
        if welke == collaborative or welke == content:
            if welke == 'collaborative' or welke == 'content':
                if welke == 'collaborative': # Filtert collaborative
                    gebruikers = """select id from profielen"""
                    cursor.execute(gebruikers)
                    allegebruikers = cursor.fetchall()

                    for gebruiker in allegebruikers: # Voor alle gebruikers
                        recommend = collaborative(gebruiker, cursor, product)
                        inzetten = """insert into collaborative (product_id, product_1, product_2, product_3, product_4) values (%s, %s, %s, %s, %s)"""
                        values = (gebruiker[0], recommend[0], recommend[1], recommend[2], recommend[3])
                        cursor.execute(inzetten, values)
                        database.commit()
                        break
                else:
                    products = """select id from products"""
                    cursor.execute(products)
                    alleproducts = cursor.fetchall()

                    for product in alleproducts: # Voor alle producten
                        category = """select subcategory, subsubcategory from products where id = (%s)"""
                        cursor.execute(category, product)
                        categorie = cursor.fetchall()

                        recommend = content(product, cursor, categorie)

                        inzetten = """insert into content (product_id, product_1, product_2, product_3, product_4) values (%s, %s, %s, %s, %s)"""
                        values = (product[0], recommend[0], recommend[1], recommend[2], recommend[3])
                        cursor.execute(inzetten, values)
                        database.commit()
                        break
