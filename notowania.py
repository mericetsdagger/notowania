import requests
 #git test
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
    a_1 = ""
    a_data = ""
    a_otwarcie = 0
    a_maks = 0
    a_min = 0
    a_zamkniecie = 0

    for i in lista:          
            
    
        
# notowania glowne

notowania = requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text

 
#część odpowiadająca za zaciągnięcie do bazy danych z giełd światowych
strona_zagranica = requests.get("http://bossa.pl/pub/indzagr/mstock/sesjazgr/sesjazgr.prn").text
split_przecinki(strona_zagranica) 
lista_zagranica = strona_zagranica.split("\n")
 
a_gielda = ""
a_data = ""
a_otwarcie = 0
a_maks = 0
a_min = 0
a_zamkniecie = 0
 
a_insert_zagranica = "insert into notowania.swiat (GIELDA, DATA_KURSU, OTWARCIE, MAKSIMUM, MINIMUM, ZAMKNIECIE) values "
 
for i in lista_zagranica:
    przecinek = i.find(",")
    a_gielda = i[0:przecinek]
    przecinek = i.find(",",przecinek)
    a_data = i[przecinek+1:len(a_gielda)+9]
    przecinek = i.find(",",przecinek+1)
    a_otwarcie = i[przecinek+1:i.find(",",przecinek+1)]
    przecinek = i.find(",",przecinek+1)
    a_maks = i[przecinek+1:i.find(",",przecinek+1)]
    przecinek = i.find(",",przecinek+1)
    a_min = i[przecinek+1:i.find(",",przecinek+1)]
    przecinek = i.find(",",przecinek+1)
    a_zamkniecie = i[przecinek+1:i.find(",",przecinek+1)]
 
    a_insert_zagranica = a_insert_zagranica + ("\n ('{}',to_date('{}','YYYYMMDD'), {}, {}, {}, {})").format(a_gielda,
                                                                                       a_data,
                                                                                       a_otwarcie,
                                                                                       a_maks,
                                                                                       a_min,
                                                                                       a_zamkniecie)
    if i != lista_zagranica[-1]:
        a_insert_zagranica = a_insert_zagranica + ","
 
#część odpowiadająca za zaciągnięcie do bazy danych walut
        
strona_waluty = requests.get("http://bossa.pl/pub/waluty/mstock/sesjanbp/sesjanbp.prn").text
lista_walut = strona_waluty.split("\n")
del lista_walut[-1] #ostatni wiersz pusty
 
a_waluta = ""
a_insert_waluty = "insert into notowania.waluty (WALUTA, DATA_KURSU, KURS) values "
 
for i in lista_walut:
    a_waluta = i[0:3]
    a_data = i[4:12]
    a_zamkniecie = i[34:40]
 
    a_insert_waluty = a_insert_waluty + ("\n('{}',to_date('{}','YYYYMMDD'),{})").format(a_waluta,a_data,a_zamkniecie)
 
    if i != lista_walut[-1]:
        a_insert_waluty = a_insert_waluty + ","
      
a_insert_waluty = not_allowed(a_insert_waluty)
