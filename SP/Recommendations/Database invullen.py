from pymongo import MongoClient
import csv
import psycopg2
import mysql.connector

client = MongoClient('localhost', 27017)
db = client["huwebshop"]

c = psycopg2.connect("dbname=HUwebshop user=postgres password=Tomaat221")
cursor = c.cursor()


def insertproducts(cursor):
    with open('producten.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'naam', 'verkoopprijs', 'aanbieding', 'target_audienceid', 'merkid', 'categorieid',
                      'sub_categorieid', 'sub_sub_categorieid', 'typeid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        for product in db.products.find():
            kwaliteiten = []

            dingen = ["product['properties']['doelgroep']", "product['brand']", "product['category']",
                      "product['sub_category']", "product['sub_sub_category']", "product['properties']['type']"]

            for i in dingen:
                try:
                    x = eval(i)
                    if x == None:
                        x = 'None'
                    kwaliteiten.append(x)
                except:
                    kwaliteiten.append('None')

            foreignkeys = []

            if kwaliteiten[2] == ['Make-up & geuren', 'Make-up', 'Nagellak']:
                continue

            cursor.execute("""select id from target_audience where audience = (%s)""", (kwaliteiten[0],))
            ids = cursor.fetchall()
            foreignkeys.append(ids[0][0])

            cursor.execute("""select id from merk where naam = (%s)""", (kwaliteiten[1],))
            ids = cursor.fetchall()
            foreignkeys.append(ids[0][0])

            cursor.execute("""select id from categorie where naam = (%s)""", (kwaliteiten[2],))
            ids = cursor.fetchall()
            foreignkeys.append(ids[0][0])

            cursor.execute("""select id from sub_categorie where naam = (%s)""", (kwaliteiten[3],))
            ids = cursor.fetchall()
            foreignkeys.append(ids[0][0])

            cursor.execute("""select id from sub_sub_categorie where naam = (%s)""", (kwaliteiten[4],))
            ids = cursor.fetchall()
            foreignkeys.append(ids[0][0])

            cursor.execute("""select id from type where type = (%s)""", (kwaliteiten[5],))
            ids = cursor.fetchall()
            foreignkeys.append(ids[0][0])


            try:
                writer.writerow({'id': product.get("_id"),
                                 'naam': product.get("name", 'None'),
                                 'verkoopprijs': int(product['price'].get("selling_price", 'None')),
                                 'aanbieding': product['properties'].get("discount", 'None'),
                                 'target_audienceid': int(foreignkeys[0]),
                                 'merkid': int(foreignkeys[1]),
                                 'categorieid': int(foreignkeys[2]),
                                 'sub_categorieid': int(foreignkeys[3]),
                                 'sub_sub_categorieid': int(foreignkeys[4]),
                                 'typeid': int(foreignkeys[5])
                                 })

            except:
                continue
    print("Finished creating the sessies database contents.")


def insertprofielen(cursor):
    with open('profielen.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'count', 'segmentid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        goed = 0
        fout = 0
        for profile in db.profiles.find():
            try:
                x = (profile['recommendations']['segment']).lower()

                cursor.execute("""select id from segment where naam = (%s)""", (x,))
                ids = cursor.fetchall()
                goed += 1
                #print('goed 1')
            except:
                ids = [(2, )]
                fout += 1
                #print('fout 1')
            try:
                z = profile['order'].get("count", 'None')
                if z == 'None':
                    z = 0
            except:
                z = 0
            try:
                writer.writerow({'id': profile["_id"],
                                 'count': z,
                                 'segmentid': ids[0][0]
                                 })
            except:
                print('help')
                continue
    print("Finished creating the sessies database contents.")


def csvbuids():
    with open('buids.csv', 'w', newline='') as csvout:
        fieldnames = ['profielen_id', 'buid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        for profile in db.profiles.find():
            try:
                buid = profile['buids']
            except:
                buid = 'None'
            if buid == []:
                buid = 'None'
            writer.writerow({'profielen_id': profile["_id"],
                            'buid': buid,
                            })


def devicetype(session):
    try:
        types = [session["user_agent"]['flags']['is_mobile'], session["user_agent"]['flags']['is_pc'],
                 session["user_agent"]['flags']['is_tablet']]
        for i in range(0, len(types)):
            if types[0] is True:
                return 'mobile'
            elif types[1] is True:
                return 'pc'
            elif types[2] is True:
                return 'tablet'
            else:
                return 'other'
    except:
        return 'other'



def prof(sessie):
    for profile in db.profiles.find():
        try:
            x = profile['buids']
            for j in x:
                if j == sessie:
                    return profile['_id']
        except:
            continue


def insertsessies(curs, cursor):
    with open('sessies.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'device_type', 'os', 'duur', 'profielen_id', 'segmentid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()


        for session in db.sessions.find():
            id1 = session['_id']
            duur = (session['session_end'] - session['session_start']).total_seconds()
            type = devicetype(session)
            try:
                seg = session['segment']
            except:
                seg = 'None'
            cursor.execute("""select id from segment where naam = (%s)""", (seg.lower(),))
            segment = cursor.fetchall()

            prodid = """select profid from sessions where id = (%s)"""
            curs.execute(prodid, (id1,))
            profiel = curs.fetchall()

            try:
                writer.writerow({'id': session["_id"],
                                 'device_type': type,
                                 'os': session['user_agent']['os'].get("familiy", None),
                                 'duur': duur,
                                 'profielen_id': profiel[0][0],
                                 'segmentid': segment[0][0]
                                 })
            except:
                writer.writerow({'id': session["_id"],
                                 'device_type': type,
                                 'os': session['user_agent']['os'].get("familiy", None),
                                 'duur': duur,
                                 'profielen_id': 'None',
                                 'segmentid': segment[0][0]
                                 })

database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='Voer hier je wachtwoord in',
        database="Voer hier je database in"
    )

cu = database.cursor()
insertsessies(cu, cursor)


def insertsegment():
    with open('segment.csv', 'w', newline='') as csvout:
        fieldnames = ['segment']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        segments = []

        for profile in db.profiles.find():
            try:
                if profile['recommendations']['segment'] not in segments:
                    segments.append(profile['recommendations']['segment'])
            except:
                continue

        for i in segments:
            try:
                writer.writerow({'segment': i})
            except:
                continue
    print("Finished creating the segment database contents.")


def insertcategorie():
    with open('category.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'naam']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        categorien = []

        y = 1

        for product in db.products.find():
            try:
                x = product['category']

                if x not in categorien:
                    if len(x[0]) > 1:
                        continue
                    else:
                        categorien.append(x)

            except:
                continue

        for i in categorien:
            try:
                writer.writerow({'id': y, 'naam': i})
                y += 1
            except:
                continue
        writer.writerow({'naam': 'None'})
    print("Finished creating the categorie database contents.")


def brand():
    x = set()
    with open('merk.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'brand']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        for product in db.products.find():
            x.add(product.get("brand", None))

        y = 1

        for i in x:
            if i == None:
                i = 'None'
            try:
                writer.writerow({
                    'id': y,
                    'brand': i})
                y += 1

            except:
                continue
    print("Finished creating the product database contents.")


def type():
    x = set()
    with open('type.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'type']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        for product in db.products.find():
            try:
                prop = product["properties"].get("type", None)
                x.add(prop)
            except:
                continue

        y = 1
        for i in x:
            if i == None:
                i = 'None'
            try:
                writer.writerow({
                    'id': y,
                    'type': i})
                y += 1

            except:
                continue
    print("Finished creating the product database contents.")


def inserttarget():
    with open('target.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'audience']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        geslachten = []

        for product in db.products.find():
            try:
                if product['properties']['doelgroep'] not in geslachten:
                    geslachten.append(product['properties']['doelgroep'])
            except:
                continue

        y = 1

        for i in geslachten:
            try:
                if i == None:
                    i = 'None'
                writer.writerow({'id': y,
                                 'audience': i})
                y += 1
            except:
                continue
    print("Finished creating the categorie database contents.")


def subcat(cursor):
    with open('sub_categorie.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'naam', 'categorieid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        catego = []

        for product in db.products.find():
            try:
                x = [product['category'], product['sub_category']]
                if x[1] == None:
                    x[1] = 'None'
                if x not in catego:
                    catego.append(x)
            except:
                continue

        y = 1

        for i in catego:
            cursor.execute("""select id from categorie where naam = (%s)""", (i[0],))
            ids = cursor.fetchall()

            try:
                writer.writerow({'id': y,
                                 'naam': i[1],
                                 'categorieid': ids[0][0]})
                y += 1
            except:
                continue
    print("Finished creating the categorie database contents.")


def subsubcat(cursor):
    with open('sub_sub_categorie.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'naam', 'sub_categorieid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        catego = []

        for product in db.products.find():
            try:
                x = [product['sub_category'], product['sub_sub_category']]
                if x[1] == None:
                    x[1] = 'None'
                if x not in catego:
                    catego.append(x)
            except:
                continue

        y = 1

        for i in catego:
            cursor.execute("""select id from sub_categorie where naam = (%s)""", (i[0],))
            ids = cursor.fetchall()

            try:
                writer.writerow({'id': y,
                                 'naam': i[1],
                                 'sub_categorieid': ids[0][0]})
                y += 1
            except:
                continue
    print("Finished creating the categorie database contents.")


def insertgekocht():
    with open('product_gekocht.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'sessies_id','producten_id']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        y = 1
        for sessie in db.sessions.find():
            try:
                id = sessie['order']['products']
            except:
                continue
            for i in id:
                writer.writerow({
                    'id': y,
                    'sessies_id': sessie['_id'],
                    'producten_id': i['id']})
                y += 1
    print("Finished creating the target database contents.")

insertgekocht()

def aangeraden():
    with open('eerder_aangeraden.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'profielenid', 'productenid']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        y = 1
        for prof in db.profiles.find():

            try:
                id = prof['previously_recommended']
                #print(prof['_id'], id)
            except:
                continue
            for i in id:
                if id != []:
                    writer.writerow({
                        'id': y,
                        'profielenid': prof['_id'],
                        'productenid': i})
                    y += 1
    print("Finished creating the target database contents.")


def bekeken():
    with open('eerder_bekeken.csv', 'w', newline='') as csvout:
        fieldnames = ['id', 'profielen_id', 'producten_id']

        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        y = 1
        for prof in db.profiles.find():

            try:
                id = prof['recommendations']['viewed_before']
            except:
                continue
            if id != []:
                for i in id:
                    try:
                        writer.writerow({
                            'id': y,
                            'profielen_id': prof['_id'],
                            'producten_id': i})
                        y += 1
                    except:
                        continue
    print("Finished creating the target database contents.")


def alles():
    pass

alles()


