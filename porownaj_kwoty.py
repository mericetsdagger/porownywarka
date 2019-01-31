import csv
import os
from os import listdir
from os.path import isfile, join
import datetime
from tkinter import *
from tkinter.filedialog import askdirectory

class Application(Frame):
    nazwa_folderu = ""
    sciezka_folderu = ""
    tekst_od = ""
    tekst_do = ""
    tekst_do_num = 0
    wynik = ""
    radioVar = 0 # 1 to ciąg, 2 ilość znaków

    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        self.labelInfo = Label(self, text = "Wybierz folder z plikami PAD:")
        self.labelInfo.grid()
        self.button1 = Button(self, text = "Przeglądaj", command = self.fileopen)
        self.button1.grid()
        self.labelTekst = Label(self)
        self.labelTekst.grid()
        self.button2 = Button(self, text = "Weryfikuj", command = self.mainAct)
        self.button2.grid()
        self.labelStatus = Label(self, text = "Status: ")
        self.labelStatus.grid()
        self.labelStatusInfo = Label(self, text = "Czekam na rozpoczęcie działania")
        self.labelStatusInfo.grid()
        self.labelStatusMote = Label(self)
        self.labelStatusMote.grid(stick=E)

    def fileopen(self):
        Application.sciezka_folderu = askdirectory()
        Application.nazwa_folderu = Application.sciezka_folderu[Application.sciezka_folderu.rfind("/")+1:]
        self.labelTekst.config(text="Wybrano folder: " + Application.nazwa_folderu)

    def mainAct(self):
        self.labelStatusInfo.config(text="Rozpoczynam działanie")
        mypath = Application.sciezka_folderu
        csv_obj_kwoty = open(mypath+"/tabela.txt", "r")
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
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        data_graniczna_1 = datetime.datetime.strptime("10-12-2018","%d-%m-%Y")
        data_graniczna_2 = datetime.datetime.strptime("09-01-2019","%d-%m-%Y")
        for file1 in onlyfiles:
            
            reader_obj_zest1 = []        
            if file1[0:6] == 'PADCLN':
                read_1_file = open(mypath+"\\"+file1,"r") #otwiera tylko pliki PADCLN i ładuje rekordy w listę
                pliki += 1
                self.labelStatusInfo.config(text="Przerabiam plik nr "+str(pliki))
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
                            
        moteStatus = ""
        if ilosc_bledow_01 == 0 and ilosc_bledow_dat_g == 0 and ilosc_bledow_kwot:
            moteStatus = ":)"
        else:
            moteStatus = ":("
        self.labelStatusMote.config(text=moteStatus)
                
        self.labelStatusInfo.config(text="Gotowe!")
        Output = "Sprawdzono plików: " + str(pliki) + "\n"
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

  
root = Tk()
root.title("WZ")
root.geometry("180x180")

app = Application(root)
root.mainloop()
