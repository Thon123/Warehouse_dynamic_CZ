#!/usr/bin/python3
from settings import *
from email_sender import posli_email

"""___________________________[NAČTU NÁŠ DOSTUPNOSTNÍ DT]__________________________"""

#PRAVDĚPODOBNĚ BY ŠLO ZMENŠIT - PROZATÍM NECHÁVÁM TAKTO
def excel_dostupnost(cislo_sloupce):
    global dostupnostni_list #abych nemusel řešit return apod..
    #otvírám všechny skladové listy v google sheets
    sheet1 = client.open('sklad_gc_dynamic').get_worksheet(0)
    sheet2 = client.open('sklad_gc_dynamic').get_worksheet(1)
    sheet3 = client.open('sklad_gc_dynamic').get_worksheet(2)

    """Případně si hodit do listu a vše proiterovat 1x"""
    #Z listů si vezmu kody a dostpnost - pro foto, cartridge a gc
    gc_produkty, gc_dostupnost = sheet1.col_values(1), sheet1.col_values(cislo_sloupce)
    foto_produkty, foto_dostupnost = sheet2.col_values(1), sheet2.col_values(cislo_sloupce)
    cartridge_produkty, cartridge_dostupnost = sheet3.col_values(1), sheet3.col_values(cislo_sloupce)

    #Všem listům odeberu hlavičku
    gc_produkty, gc_dostupnost = gc_produkty[1:], gc_dostupnost[1:]
    foto_produkty, foto_dostupnost = foto_produkty[1:], foto_dostupnost[1:]
    cartridge_produkty, cartridge_dostupnost = cartridge_produkty[1:], cartridge_dostupnost[1:]

    #Sečtu kody a dostupnosti - jednotné listy
    kody_produktu = gc_produkty + foto_produkty + cartridge_produkty
    dostupnost = gc_dostupnost + foto_dostupnost + cartridge_dostupnost

    #Změním Do týdne a Do týdna na správný formát
    for i in range(len(dostupnost)):
        if dostupnost[i] == "Do týdne":
            dostupnost[i] = "Skladem u dodavatele (expedice do 3 dní)"
        if dostupnost[i] == "Do týdna":
            dostupnost[i] = "Skladom u dodávateľa (expedícia do 3 dní)"
    #vytvořím finální dict - pro tvorbu průniku dat s feedem
    dostupnostni_list = dict(zip(kody_produktu,dostupnost))

"""__________________________________[TVORBA PRŮNIKU DAT]_______________________________"""

#PRO VŠE CO MÁ SUPPLIER_CODE O HODNOTĚ AVAILABILITY
#A ZA PŘEDPOKLADU KDY DOSTUPNOST NENÍ SHODNÁ
#CHCEME SUPPLIER CODE - A DLE TOHO KODU ULOŽIT 
#KOD DODAVATELE, KOD, A STAV DOSTUPNOSTI (počítá google sheets)

def prunik_dat(nazev_feedu):
    """Magic funkce průnik všech dat"""
    global sc_akt, d_akt, c_akt
    """Otevřeme upravený feed"""
    with open(nazev_feedu, encoding="utf8") as file:
        xml = file.read().encode()
        root = etree.fromstring(xml)
    """Vytvoříme z něj průnik dat"""
    for feed in root.getchildren(): #FEED - NA PRODUCT
        for prvek in feed.getchildren(): #PRODUCT - NA TAGY
            for supplier_code in feed.findall("SUPPLIER_CODE"): 
                pass #NAJDEME VŠECHNY SUPPLIER_CODE
            for dostupnost in feed.findall("AVAILABILITY"): 
                pass #NAJDEME VŠECHNY DOSTUPNOSTI
        for key, value in dostupnostni_list.items():#PRO VŠECHNY KLÍČE A HODNOTY ZE SKLADU
            #POKUD JE TEXT SUPPLIER_CODE SHODNÝ S KLÍČEM, A DOSTUPNOSTI NEJSOU ROVNY!
            if supplier_code.text == key and dostupnost.text != value:
                for code in feed.findall("CODE"): #HLEDÁME VŠECHNY KODY
                    sc_akt.append(supplier_code.text) #list kodu dodavatele
                    d_akt.append(value) #list dostupnosti
                    c_akt.append(code.text) #list kodu"""

"""______________________________________[TVORBA KOŠÍKU ]_________________________________"""

def kosik_dostupnost():
    """MUSÍM DOGENEROVAT TAG - LZE VLOZIT DO KOSIKU - ten definujeme dle dostupnosti"""
    for i in range(len(d_akt)): #pro celý list dostupnost iterujeme
        #logika je jasná skladem a do týdne = 1, není skladem = 0
        if d_akt[i] == "Není skladem" or d_akt[i] == "Nie je na sklade":
            kosik_akt.append("0") #vše co není Není skladem má 1
        else:
            kosik_akt.append("1") #jinak dáváme defaultně za 0

"""______________________________[_JSON_AKTUALIZACNI_SOUBOR]___________________________"""

def novy_json(json_nazev):
    """Aktualizační soubor - json"""
    for i in range(len(c_akt)):   
        prubezny["code"] = c_akt[i] #zakladá dict s kodem
        prubezny["availability"] = d_akt[i] #přidá dostupnost
        prubezny["can_add_to_basket_yn"] = kosik_akt[i] #přidá košík
        products.append(dict(prubezny)) #s appendi

    muj_dict = {"products": products} #dodefinuje hlavičku

    with open(json_nazev, 'w') as file: #finálně uloží
        json.dump(muj_dict , file, indent=4)

#JE DŮLEŽITÉ NEUSTÁLE ŘEŠIT AKTUALIZAČNÍ SOUBOR - TZN nesmím posílat 1gb feed přes API
#ALE JEN TO CO SE MĚNÍ - zamezím tak možnému problému pokud něco selže - selže jen 
#jedna malá část

"""______________________________[ZPĚTNÁ AKTUALIZACE FEEDU]___________________________"""
#V podstatě je to jednoduché - pokud tento skript zapnu 2x - výsledný  xml bude prázdný
#Test bez testu
#Upravím základní feed o to co jsem upravil na eshopu - LZE VYPNOUT pokud nebude OK

def zpetne_aktualizuj(nazev_feedu): #původní feed upravím o rozdílná data
    """Zpětně přehrajeme XML feed - zmenšíme z 1gb jen na to co je nové"""
    with open(nazev_feedu, encoding="utf8") as file:
        xml = file.read().encode()
        root = etree.fromstring(xml) #otevřeli jsme a z parsovali jsme feed
    for feed in root.getchildren(): #FEED PRODUCTS NA PRODUCT
        for prvek in feed.getchildren(): #FEED PRODTC NA - CODE, AVALABILITY...
            for kod in feed.findall("CODE"): #hledáme všechny kody
                pass #zatím s nimi nic neděláme
            for dostupnost in feed.findall("AVAILABILITY"): #hledám všechny dostupnosti
                pass #též zatím nic
        for key, value in dict(zip(c_akt,d_akt)).items():
            #beru dva listy z průniku dat a přetvořím na list
            if kod.text == key: #pokud se mi shodujou kody produktu
                #print(f"Měním {dostupnost.text} na {value}")
                #print(f"{key} = {kod.text}")
                dostupnost.text = value #nastavím novou dostupnost na hodnotu z průniku
    tree = etree.ElementTree(root) #finální uložení 
    tree.write(nazev_feedu, pretty_print=True, xml_declaration=True, encoding="utf-8")


"""________________________________[CELEK_PRO_ESHOPY]__________________________________"""

#DÁM TO DO SMYČKY - znovu moje opakování s WHILE není ideální prozatím
#číslo sloupce slouží pro dostupnost a jazykovou lokalizaci 14 yescom a nb, 15ep

def feed_maker(nazev_feedu, json_nazev, cislo_sloupce):
    """finální funkce - stáhne, upraví, vytvoří soubor pro api, a aktualizační xml"""
    i = 0
    while i !=5: #definuji i smyčku pro 5 pokusů - jistota
        try:
            cas = datetime.now().strftime("%H:%M:%S")
            excel_dostupnost(cislo_sloupce) #vydoluje dostupnosti z excelu
            print("Excel")
            prunik_dat(nazev_feedu) #najde rozdíly excelu a feedu
            print("prunik")
            kosik_dostupnost() #dotvoří dostupnost 0 a 1 pro feed
            print("dostupnost")
            novy_json(json_nazev) #vytvoří aktualizační feed
            print("json")
            zpetne_aktualizuj(nazev_feedu) #zpětně aktualizuje feed
            print(f"Feed plně aktualizován v {cas}") 
            i = 5
        except: #pokud ok posíláme email naopak též
            i +=1 #v podstatě můj domácí retry mod pro funkci
            time.sleep(60) #tzn. dám každý funkci 5 minut rezervu aby proběhla
            if i == 5: #času na to je kotel klidně lze zvýšit na 10 poté
                posli_email(f"SELHÁNÍ ÚPRAVY: {nazev_feedu}", "expedice@yescom.cz")
    dostupnostni_list.clear(), prubezny.clear()
    sc_akt.clear(), d_akt.clear(), c_akt.clear(), kosik_akt.clear(), products.clear()

"""____________________________________[MAIN]_____________________________________"""

dostupnostni_list, prubezny = {}, {}
sc_akt, d_akt, c_akt, kosik_akt, products  = [], [], [], [], []


def main():
    """pouze souhrn pro 3 obchody"""
    feed_maker("nabitabaterka.xml","nabitabaterka.json",14)
    feed_maker("yescom.xml","yescom.json",14)
    feed_maker("ep.xml","ep.json",15)

if __name__ == "__main__":
    main()
