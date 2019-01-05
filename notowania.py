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
        print(i)
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
        
    return a_insert
        
#część odpowiadająca za pobranie danych z polskiej gieldy i przerobienie na sql
notowania = requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text
#sql_notowania = split_txt_to_insert(notowania, "NOTOWANIA", "SPOLKA")
#sql_wig = split_txt_to_insert(notowania,"WIG","INDEX")
#część odpowiadająca za pobranie danych z giełd światowych i przerobienie na sql
strona_zagranica = requests.get("http://bossa.pl/pub/indzagr/mstock/sesjazgr/sesjazgr.prn").text
sql_zagranica = split_txt_to_insert(strona_zagranica, "GIELDY", "GIELDA")
print(sql_zagranica)
#część odpowiadająca za zaciągnięcie do bazy danych walut        
#strona_waluty = requests.get("http://bossa.pl/pub/waluty/mstock/sesjanbp/sesjanbp.prn").text
#sql_waluty = split_txt_to_insert(strona_waluty, "WALUTY", "WALUTA")
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
