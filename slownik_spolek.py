import requests
import mysql.connector
import string
from DBCon import DBCon

lista_spolek = []
lista_omitted = []
dbconfig = {'host' : 'localhost',
            'user' : 'root',
            'password' : 'kzc1@3',
            'database' : 'notowania'}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()
sql_om = "select nazwa from notowania.notowania_omitted"
sql_spolki = "select skrot from notowania.dict_spolki"
cursor.execute(sql_om)

for row, in cursor.fetchall():
    lista_omitted.append(row)

cursor.execute(sql_spolki)

for row, in cursor.fetchall():
    lista_spolek.append(row)    
 
lista_biezaca = []
strona = requests.get("http://bossa.pl/pub/newconnect/mstock/sesjancn/sesjancn.prn").text + requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text
strona_rozbicie = strona.split("\n")
for i in strona_rozbicie:
    spolka = i[0:i.find(",")]
    if spolka != "":
        if spolka not in lista_omitted:
            lista_biezaca.append(spolka)
        else:
            pass
    else:
        pass
# skrot spolka rynek
lista = [item for item in lista_biezaca if item not in lista_spolek]

link_bankier = "https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=" #dodac skrot spolki
sql_insert = "insert into notowania.dict_spolki (skrot, spolka, rynek) values"
for i in lista:
    if i == "ABCDATA":
        pobranie = requests.get(link_bankier + i).text
        cala_nazwa = pobranie[pobranie.find("<title>")+7:pobranie.find(" (")]
        a = pobranie.find("""<td>Rynek notowań:</td>""")+85
        rynek = pobranie[a:pobranie.find("</td>",a,a+80)]
        print(a)
        
        
        
        




spolki_gpw = requests.get("https://www.bankier.pl/gielda/notowania/akcje").text


  
    
