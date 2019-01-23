import requests
from DBCon import DBCon
from datetime import datetime, timedelta

dzis = datetime.today().strftime('%Y-%m-%d').replace("-",".") 
wczoraj = (datetime.today()-timedelta(days=1)).strftime('%Y-%m-%d').replace("-",".")
przedwcz = (datetime.today()-timedelta(days=2)).strftime('%Y-%m-%d').replace("-",".")
wskaz_dzis = """<td colspan="2" class="dni">"""+dzis+"</td>"
wskaz_dzien = """<td colspan="2" class="dni">"""+wczoraj+"</td>"
wskaz_pwcz = """<td colspan="2" class="dni">"""+przedwcz+"</td>"
kom_list = []
a_sql = ""

for i in range(1,20):
    #wybranie do obslugi tylko stron zawierajacych:
    #1. Daty dzisiejszej - pomijamy
    #2. Daty wczorajszej - zczytujemy w listę
    #2. Daty wczorajszej i przedwczorajszej - zczytujemy do pojawienia się daty przedwczorajszej
    print(i)
    strona = ("http://biznes.pap.pl/pl/news/listings/{},").format(i)
    komunikat = requests.get(strona).text
    komunikat = komunikat[komunikat.find("""<b class="red">ZE SPÓŁEK</b>"""):]
    kom = ""
    if wskaz_dzien in komunikat:
        if wskaz_pwcz in komunikat:
            kom = komunikat[komunikat.find(wskaz_dzien):komunikat.find(wskaz_pwcz)]

        else:
            kom = komunikat[komunikat.find(wskaz_dzien):komunikat.find("""<div class="stronicowanie">""")]
        kom = kom.strip()    
        kom_list = kom_list + kom.split("""<td class="wdgodz">""")
    else:
        if wskaz_dzis in komunikat:
            pass
        else:
            break
    print(len(kom_list))
intt = 0
for i in kom_list:
    if i[0:28] != """<td colspan="2" class="dni">""":
        link = "www.biznes.pap.pl" + i[i.find("""/pl/news/listing"""):i.find('''"''',i.find("""/pl/news/listing""")+1)]
        tresc = i[i.find("""style="">""")+9:i.find("""</a>""")]
        czas_pub = wczoraj + " " + i[0:5]
        print(intt)
        print(kom_list[intt])
        intt = intt+1
    else:
        pass
