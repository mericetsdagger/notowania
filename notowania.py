import requests
import pymysql

def not_allowed(insert_statement):
    not_allowed_list = ['SELECT','DROP','DELETE','UPDATE']
    for i in not_allowed_list:
        if i in insert_statement:
            insert_statement = ""
    return insert_statement        
     
def split_txt_to_insert(podaj_wyciag, tabela, a1nazwa):
    lista = podaj_wyciag.split("\n")
    if lista[-1] == "":
      del lista[-1]
    liczba_przecinkow = lista[0].count(",")
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
    del omitted[-1]

    for i in lista:
        
        przecinek = i.find(",")
        a_1 = i[0:przecinek]
        if a_1 in omitted:
            lista.remove(i)
        else:    
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

            a_insert = a_insert + ("\n ('{}',str_to_date('{}','%Y%m%d'), {}, {}, {}, {})").format(a_1,
                                                                                            a_data,
                                                                                            a_otwarcie,
                                                                                            a_maks,
                                                                                            a_min,
                                                                                            a_zamkniecie)
            if i != lista[-1]:
                a_insert = a_insert + ","

        
    if a_insert[-1] == ",":
        a_insert = a_insert[:-1]
    return a_insert
        
#część odpowiadająca za pobranie danych z polskiej gieldy i przerobienie na sql
notowania = requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text
######### dodać podział na indeksy i spółki
sql_notowania = split_txt_to_insert(notowania, "NOTOWANIA", "SPOLKA")

#część odpowiadająca za pobranie danych z giełd światowych i przerobienie na sql
strona_zagranica = requests.get("http://bossa.pl/pub/indzagr/mstock/sesjazgr/sesjazgr.prn").text
sql_zagranica = split_txt_to_insert(strona_zagranica, "GIELDY", "GIELDA")

#część odpowiadająca za zaciągnięcie do bazy danych walut        
strona_waluty = requests.get("http://bossa.pl/pub/waluty/mstock/sesjanbp/sesjanbp.prn").text
sql_waluty = split_txt_to_insert(strona_waluty, "WALUTY", "WALUTA")
'''
#pakowanie do bazy
connection = pymysql.connect(host = "host",
                             user = "user",
                             passwd = "passwd",
                             db = "mysql",
                             charset = "utf8mb4",
                             cursorclass = pymysql.cursors.DictCursor)

cur = connection.cursor()
cc = cur.execute(sql_notowania)
print(cc)
for row in cur:
    print(1)
connection.commit()    
cur.close()
connection.close()
'''
