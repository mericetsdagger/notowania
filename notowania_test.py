import requests
import pymysql

def tworz_plik(lista):
    f = open("tessst.txt","w+")
    for a in lista:
        f.write("%s\n" % a)

notowania = requests.get("http://bossa.pl/pub/ciagle/omega/cgl/ndohlcv.txt").text
print(notowania)
lista = notowania.split("\n")

print(len(lista))
j = 1
for i in lista:
    if j < 4:
        print(i)
        przecinek1 = i.find(",")
        print(i[0:przecinek1])
        przecinek2= i.find(",",przecinek1+1)
        print(i[przecinek1+1:przecinek2])
        przecinek3 = i.find(",",przecinek2+1)
        print(i[przecinek2+1:przecinek3])
        przecinek4= i.find(",",przecinek3+1)
        print(i[przecinek3+1:przecinek4])
        przecinek5= i.find(",",przecinek4+1)
        print(i[przecinek4+1:przecinek5])
        przecinek6= i.find(",",przecinek5+1)
        print(i[przecinek5+1:przecinek6])
        przecinek7= i.find(",",przecinek6+1)
        print(i[przecinek6+1:przecinek7])
    j += 1        
    if j == 3:
        break
#tworz_plik(lista)


a_spolka = "testowa"
a_data_kursu = "20181221"
a_otwarcie = 20.20
a_maksimum = 21.05
a_minimum = 19.50
a_zamkniecie = 20.30
a_obrot = 30000

#conn = pymysql.connect(host='localhost', user='root', passwd='kzc1@3', db='mysql')
#cur = conn.cursor()
#cc = cur.execute("show columns notowania.notowania")
sqlPreString = "insert into notowania (SPOLKA, DATA_KURSU, OTWARCIE, MAKSIMUM, MINIMUM, ZAMKNIECIE, OBROT) values "
sqlString = "('" + a_spolka + "', to_date('" +a_data_kursu+"','YYYYMMDD'), " + str(a_otwarcie) + ", " + str(a_maksimum) + ", " + str(a_minimum) + ", " + str(a_zamkniecie) + ", " + str(a_obrot) + ")"  
# cc cur.execute(sqlString)
#print(cc)

#for r in cur:
#    print(r)
#cur.close()
#conn.close()

print(sqlPreString)
print(sqlString)
