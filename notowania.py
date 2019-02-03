import requests
import pymysql
from DBCon import DBCon
def not_allowed(insert_statement):
    not_allowed_list = ['SELECT','DROP','DELETE','UPDATE']
    for i in not_allowed_list:
        if i.upper() in insert_statement.upper():
            insert_statement = ""
    return insert_statement        
     
def split_txt_to_insert(podaj_wyciag, tabela, a1nazwa):
    lista = podaj_wyciag.split("\n")
    if lista[-1] == "":
      del lista[-1] 
    lista_fix = []
    liczba_przecinkow = lista[0].count(",")
    a_wyc = podaj_wyciag
    a_insert_into = tabela
    a_kolumna1 = a1nazwa
    a_1 = ""
    a_data = ""
    a_otwarcie = 0
    a_maks = 0
    a_min = 0
    a_zamkniecie = 0
    a_insert = "insert into notowania.{} ({}, DATA_KURSU, OTWARCIE, MAKSIMUM, MINIMUM, ZAMKNIECIE) values".format(a_insert_into, a_kolumna1)
 
    with open("notowania_omitted.txt","r") as f:
        o_text = f.read()
    omitted = o_text.split("\n")
  
    with open("lista_wig.txt","r") as e:
        l_text = e.read()
    wigi = l_text.split("\n")

    if a_wyc == notowania:
        if a_insert_into == "NOTOWANIA":
            for a in lista:
                if a[0:a.find(",")] not in omitted:
                    lista_fix.append(a)
           ### ogarnac indeksy wykluczone 
        elif tabela == "WIG":
            for a in lista:
                if a[0:a.find(",")] in wigi:
                    lista_fix.append(a)

    else:
        lista_fix = lista.copy()


    for i in lista_fix:
        przecinek = i.find(",")
        a_1 = i[0:przecinek]    
        przecinek = i.find(",",przecinek)
        a_data = i[przecinek+1:i.find(",",przecinek+1)]
        przecinek = i.find(",",przecinek+1)
        a_otwarcie = i[przecinek+1:i.find(",",przecinek+1)]
        przecinek = i.find(",",przecinek+1)
        a_maks = i[przecinek+1:i.find(",",przecinek+1)]
        przecinek = i.find(",",przecinek+1)
        a_min = i[przecinek+1:i.find(",",przecinek+1)]
        przecinek = i.find(",",przecinek+1)
        a_zamkniecie = i[przecinek+1:i.find(",",przecinek+1)]

        a_insert += ("\n ('{}',str_to_date('{}','%Y%m%d'), {}, {}, {}, {})").format(a_1,
                                                                                    a_data,
                                                                                    a_otwarcie,
                                                                                    a_maks,
                                                                                    a_min,
                                                                                    a_zamkniecie)
        if i != lista_fix[-1]:
            a_insert += ","

    a_insert = not_allowed(a_insert)
    
    return a_insert
        
#część odpowiadająca za pobranie danych z polskiej gieldy i przerobienie na sql
notowania = requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text
sql_notowania = split_txt_to_insert(notowania, "NOTOWANIA", "SPOLKA")
sql_wig = split_txt_to_insert(notowania,"WIG","INDEKS")
#część odpowiadająca za pobranie danych z giełd światowych i przerobienie na sql
strona_zagranica = requests.get("http://bossa.pl/pub/indzagr/mstock/sesjazgr/sesjazgr.prn").text
sql_zagranica = split_txt_to_insert(strona_zagranica, "GIELDY", "GIELDA")
#część odpowiadająca za zaciągnięcie do bazy danych walut        
strona_waluty = requests.get("http://bossa.pl/pub/waluty/mstock/sesjanbp/sesjanbp.prn").text
sql_waluty = split_txt_to_insert(strona_waluty, "WALUTY", "WALUTA")
#część odpowiadająca za zaciągnięcie do bazy danych NC
strona_nc = requests.get("http://bossa.pl/pub/newconnect/mstock/sesjancn/sesjancn.prn").text
sql_nc = split_txt_to_insert(strona_nc, "NC", "SPOLKA")

#pakowanie do bazy

dbcon_read = open("dbconfig.txt","r")
db_list = dbcon_read.read().split("\n")
dbconfig = {}
for i in db_list:
    dbconfig[str(i)[0:str(i).find(":")]] = str(i)[str(i).find(":")+1:]
    print(str(i)[0:str(i).find(":")])
    print(str(i)[str(i).find(":")+1:])

with DBCon(dbconfig) as cursor:
    cursor.execute(sql_notowania)
    cursor.execute(sql_wig)
    cursor.execute(sql_waluty)
    cursor.execute(sql_zagranica)
    cursor.execute(sql_nc)
