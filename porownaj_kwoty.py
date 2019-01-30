import csv
import os
from os import listdir
from os.path import isfile, join
import datetime

csv_obj_kwoty = open("tabela.txt", "r")
lista_kwot = []
reader_obj_kwot = csv_obj_kwoty.read()
lista_kwot = reader_obj_kwot.split("\n")
csv_obj_kwoty.close()
dict_kwoty = {}
for row in lista_kwot:
    dict_kwoty[str(row)[0:12]] = str(row)[str(row).find(";")+1:]
    
row_str = ""
ilosc_bledow_01 = 0
ciag_bledy_01 = ""
ilosc_bledow_kwot = 0
ciag_bledy_kwot = ""
ilosc_bledow_dat_g = 0
ciag_blady_dat_g = ""

ccc = 0
pliki = 0
mypath = os.getcwd()
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
data_graniczna_1 = datetime.datetime.strptime("10-12-2018","%d-%m-%Y")
data_graniczna_2 = datetime.datetime.strptime("09-01-2019","%d-%m-%Y")
for file1 in onlyfiles:
    pliki += 1
    reader_obj_zest1 = []        
    if file1[0:6] == 'PADCLN':
        read_1_file = open(file1,"r") #otwiera tylko pliki PADCLN i ładuje rekordy w listę
        for l in read_1_file:
            reader_obj_zest1.append(l)

        for row in reader_obj_zest1:

            row_str = str(row)
           
            if row_str[0:3] == "15#" and row_str[3:29] == row_str[30:56]: #weryfikacja kwot
                ccc+=1
                umowa = row_str[13:25]
                kwota_dict = dict_kwoty.get(umowa,"z")
                kwota_zest = ""
                if kwota_dict != "z":
                    indeks = 0
                    indeks1 = 0
                    indeks2 = 0
                    krzyzyk = 0
                    for i in row_str:
                        indeks1 += 1
                        indeks2 += 1
                        if i == "#":
                            krzyzyk += 1
                        if krzyzyk == 4:
                            indeks1 -= 1
                        if krzyzyk == 5:
                            break
                        
                        
                    kwota_zest = row_str[indeks1:indeks2-1]
                    kwota_zest = kwota_zest.replace(".",",")
                    if kwota_zest[0:1] == ",":
                        kwota_zest = "0" + kwota_zest
                    
                    if str(kwota_dict) != kwota_zest:
                        ilosc_bledow_kwot += 1
                        ciag_bledy_kwot += file1 + " " + umowa + " " + kwota_dict + " " + kwota_zest + "\n"
                    

            if row_str[0:3] == "01#": #weryfikacja dat
                row_str = row_str.strip()
                dzien_koniec = row_str[row_str.rfind("#")+1:]
                indeks = 0
                krzyzyk = 0
                for i in row_str:
                    indeks += 1
                    if i == "#":
                        krzyzyk += 1
                    if krzyzyk == 5:
                        break

                dzien_srodek = row_str[indeks:indeks+2]

                if dzien_koniec != dzien_srodek:
                    ilosc_bledow_01 += 1
                    ciag_bledy_01 += file1 + " " + umowa + " " + dzien_srodek + " " + dzien_koniec + "\n"

                data_wyciagu = datetime.datetime.strptime(row_str[indeks:indeks+10],"%d-%m-%Y")
                if data_wyciagu < data_graniczna_1 or data_wyciagu > data_graniczna_2:
                    ilosc_bledow_dat_g += 1
                    ciag_bledy_dat_g += file1 + " " + umowa + " " + data_wyciagu + "\n"
                

Output = "Sprawdzono plików: " + str(len(onlyfiles)) + "\n"
Output += "Zweryfikowano rekordów: " + str(ccc) + "\n"
Output += "Ilosc bledow dla weryfikacji dat koncowych: " + str(ilosc_bledow_01) + "\n"
Output += "Ilosc bledow dla weryfikacji kwot: " + str(ilosc_bledow_kwot) + "\n"
Output += "Ilosc bledow dla weryfikacji dat granicznych: " + str(ilosc_bledow_dat_g) + "\n"
if ilosc_bledow_01 != 0:
    Output += "Błędne rekordy dla dat koncowych: \n" + ciag_bledy_01
if ilosc_bledow_kwot != 0:
    Output += "Błędne rekordy dla kwot: \n" + ciag_bledy_kwot
if ilosc_bledow_dat_g != 0:
    Output += "Błędne rekordy dla dat granicznych: \n" + ciag_bledy_dat_g

newFile = open("Weryfikacja_"+str(datetime.datetime.now()).replace(".","_").replace(" ","_").replace(":","_")+".txt","w")
newFile.write(Output)
newFile.close()


print("Gotowe!")
