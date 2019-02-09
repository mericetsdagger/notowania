import requests
import mysql.connector
import string
from DBCon import DBCon

lista_spolek = []
lista_omitted = []
dbcon_read = open("dbconfig.txt","r")
db_list = dbcon_read.read().split("\n")
dbconfig = {}
for i in db_list:
    dbconfig[str(i)[0:str(i).find(":")]] = str(i)[str(i).find(":")+1:]
    
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
conn.close() 
lista_biezaca = []
strona = requests.get("http://bossa.pl/pub/newconnect/mstock/sesjancn/sesjancn.prn").text + requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text
strona_rozbicie = strona.split("\n")
spolki_gpw = requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text.split("\n")
lista_gpw = []

for j in spolki_gpw:
    lista_gpw.append(j[0:j.find(",")])
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
counter = 0

for i in lista:
    counter += 1
    pobranie = requests.get(link_bankier + i).text
    cala_nazwa = pobranie[pobranie.find("<title>")+7:pobranie.find(" (")]
    if i in lista_gpw:
        rynek_notowan = "GPW"
    else:
        rynek_notowan = "NC"
    sql_insert = sql_insert + "\n('{}','{}','{}')".format(i, cala_nazwa, rynek_notowan)
    if counter != len(lista):
        sql_insert += ","

if sql_insert != "insert into notowania.dict_spolki (skrot, spolka, rynek) values":
    
    with DBCon(dbconfig) as cursor:
        cursor.execute(sql_insert)
