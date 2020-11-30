import requests
import pandas as pd
import psycopg2
from psycopg2 import Error

store_name=[]
latitude=[]
longitude=[]
address=[]
store_url=[]
postal_code=[]
subrb=[]
city=[]
country=[]
residential=[]
data1=[]
records=[]

res=requests.get('https://client.lifterlocator.com/maps/handlebarsGet/kingofknives-com-au.myshopify.com?storeName'
                 '=kingofknives-com-au.myshopify.com&mapId=1148')

data = pd.read_json(res.text)
#print(data["Record"].values)

for i in data["Record"].values:
    store_name.append(i["name"])
    latitude.append(i["lat"])
    longitude.append(i["lng"])
    address.append(i["address"])
    store_url.append(i["website"])

for i in address:
    im=i.split(",")
    country.append(im[-1])
    postal_code.append(im[-2])
    city.append(im[-4])
    subrb.append(im[-3])

try:
    connection = psycopg2.connect(user="postgres",
                                  password="pragati05",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres"
                                  )

    cur = connection.cursor()

    create_table_query = '''CREATE TABLE storage (store_name TEXT,latitude TEXT,longitude TEXT,
          postal_code TEXT,subrb TEXT,city TEXT,country TEXT
          ,store_url TEXT) '''
    cur.execute(create_table_query)
    print("Table created sucessfully")
    for i in range(len(store_name)):
        insert_statement="INSERT INTO storage (store_name ,latitude ,longitude ,postal_code ,subrb ,city ,country,store_url ) VALUES ('"+store_name[i] +"','"+latitude[i]+"','"+longitude[i]+"','"+postal_code[i]+"','"+subrb[i]+"','"+city[i]+"','"+country[i]+"','"+store_url[i]+"')"
        #print(insert_statement)
        cur.execute(insert_statement)
        records.append((store_name[i], latitude[i], longitude[i], postal_code[i], subrb[i], city[i],
                        country[i], store_url[i]))

    df = pd.DataFrame(records, columns=['store name', 'latitude', 'longitude', 'postal code', 'subrb',
                                        'city', 'country', 'store url'])
    df.to_csv('store_details_back.csv', index=False, encoding='utf-8')

    connection.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while creating PostgreSQL table", error)
finally:
    if (connection):
        cur.close()
        connection.close()
        print("PostgreSQL connection is closed")
