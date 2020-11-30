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
records=[]

res=requests.get('https://client.lifterlocator.com/maps/handlebarsGet/kingofknives-com-au.myshopify.com?storeName'
                 '=kingofknives-com-au.myshopify.com&mapId=1148')
print(res.text)
data = pd.read_json(res.text)
print(data["Record"].values)

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
    residential.extend([(im[0],im[1],im[2])])
    
for i in range(len(store_name)):
    records.append((store_name[i],latitude[i],longitude[i],residential[i],postal_code[i],subrb[i],city[i],country[i],store_url[i]))
df=pd.DataFrame(records,columns=['store name','latitude','longitude','residential address','postal code','subrb','city','country','store url'])
df.to_csv('store_details.csv',index=False,encoding='utf-8')



