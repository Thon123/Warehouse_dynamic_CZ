#!/usr/bin/python3

#OFICIÁLNÍ GC UPDATER
from settings import *
from email_sender import *

"""____________________________________[ NAČTENÍ KODU Z EXCELU ]"____________________________________"""

def doluj_excel():
    """Získá kody produktu z google sheets"""
    global sloupec_kody 
    global sheet #spíše se vyhnout
    sheet = client.open('sklad_gc_dynamic').sheet1 #otvíráme náš list     
    sloupec_kody = sheet.col_values(1)[1:] #slice o první řádek
    print(f"Data z excelu získána čas: {timer()}")

"""________________________________[ NAČTENÍ FEEDU A JEHO DOLOVANI ]"________________________________"""

def doluj_data_feed():
    """Získáme potřebná data z b2b feedu - kody a počty"""
    url_feed = "url_feed.html"
    response = requests.get(url_feed) 
    feed = BeautifulSoup(response.text, "html.parser") #parsujeme html
    feed_iterace = feed.find_all("o") 
    for prvek in feed_iterace:
        jmeno = prvek.find("a", {"name": "Kod_producenta"}).get_text() #získáváme jméno
        skladovost = int(prvek["stock"]) #definujeme skladový pocet
        muj_dt[jmeno] = skladovost #vložíme data do dictionary tzn kod : počet
    print(f"Data z feedu získána čas: {timer()}")


"""________________________________[ POUŽITÍ DT PRO AKTUALIZACI DAT ]"________________________________"""

def aktualizace_dat():
    """Průnik dat z google sheets a z feedu"""
    i = 0 #ok 
    while i < len(sloupec_kody): #zajištění postupného vkládání
        konec_smycky = 0 #definuje konec iterace - na konci nenajde a jde na další
        for jmeno, pocet in muj_dt.items(): #iterujeme dictionary
            konec_smycky +=1 #definujeme konec iterace - pro break
            if jmeno == sloupec_kody[i].upper(): #pokud najdeme jmeno shodne s jinym jmene z excelu
                gc_pocty.append(pocet) #priradime pocet do listu
                i +=1 #navýšíme o 1
                nenalezeno_pocty.append("") #extra sloupec nenalezeno, pokud ma hodnotu nic
                #print(i) #nechám asi defaulntě...
                break
            elif konec_smycky == len(muj_dt): #pokud narazíme na konec iterace a nic nenajdeme
                gc_pocty.append(0) #náš produkt očividně chybí a tudíž dáme default
                nenalezeno_pocty.append("nenalezeno") #pokud nemá udáme nenalezeno
                i +=1
                #print(i) #nechám asi defaulntě...
                break
    print(f"Data jsou připravená pro nahrání čas: {timer()}")
  
"""________________________________[ AKTUALIZUJEME DATA DO EXCELU ]"________________________________"""

def nahraj_data():
    """aktualizujeme data do excelu"""
    cell_list = sheet.range(f'C2:C{len(sloupec_kody)+1}') #definuji rozmezí
    cell_list2 = sheet.range(f'E2:E{len(sloupec_kody)+1}')
    #přiřazujeme jednotlivé hodnoty 
    for index, hodnota in enumerate(gc_pocty): #cell list postupně plním - podle inexu
        cell_list[index].value = hodnota #a dále podle hodnoty a definuje že cell_list.value
    for index, hodnota in enumerate(nenalezeno_pocty): #nyní vkládáme extra sloupec
        cell_list2[index].value = hodnota #prázdné hodnoty a nenalezeno
        #je rovna hodnoty z gc poctu
    sheet.update_cells(cell_list) #již vložím celek
    sheet.update_cells(cell_list2) #vkládám info o nenalezených
    print(f"Data jsou nahraná a aktuální čas: {timer()}\nDatum a čas: {datetime.now()}")

"""____________________________________________[ SOURHN ]"_____________________________________________"""

gc_pocty, sloupec_kody,nenalezeno_pocty, muj_dt = [], [],[], {} 

#@retry(wait_fixed=300_000, stop_max_delay=1200_000)
#pokud fail skriptu, po 5 minutách nový pokus, 20 minut max celkem
def main():
    """Znovu i moc nejsou třeba místo toho 200 a poté retry"""
    i = 0
    while i !=10:
        try:
            doluj_excel() #doluji data
            doluj_data_feed() #data z feedu - muj_dt
            aktualizace_dat() #aktualizujeme data muj_dt x sloupec_kody
            nahraj_data() #a nahrajeme aktuální počty""
            i = 10
        except:
            i +=1
            time.sleep(60)
            if i == 10:
                posli_email("Sheet_selhani", "expedice@yescom.cz")

if __name__ == "__main__":
    main()