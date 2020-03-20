#!/usr/bin/python3
from settings import *
from email_sender import Posli_email

#TODO: obecně neladím dostupnost URL - místo nějaké smyčky by bohatě stačilo
#testovat zda url obdrží 200 - poté ok a pokud ne tak čekat - ALE AŽ KDYŽ BUDE
#kompelt hotovo a zbyde čas navíc

"""________________________________[STÁHNE A ULOŽÍ XML NA DISK]_________________________"""

def stahne_feed(nazev_feedu, url):
    #global root
    xmldata = requests.get(url)
    with open(nazev_feedu, 'wb') as nazev_feedu:
        nazev_feedu.write(xmldata.content)
        #pouze uložím xml nic víc

"""_________________________________[VYTÁHNE POTŘEBNÁ DATA]_____________________________"""

def vydoluj_feed(nazev_feedu):
    """Feedy mají i 1gb a server má 4gb pamět takže generátor"""
    context = etree.iterparse(nazev_feedu,["start", "end"])
    _, root = next(context) #vždycky berem další a poté čistíme

    for event, elem in context: #naše elementy
        if event == "end":
            if elem.tag == "PRODUCT": #chceme pouze tagy od productu
                for child in elem:
                    if child.tag =="AVAILABILITY": #sběr dostupnotí
                        dostupnost.append(child.text) 
                    if child.tag =="CODE": #sběr codu
                        kod.append(child.text) 
                    if child.tag =="SUPPLIER_CODE": #sber kodu dodavatele
                        kod_dod.append(child.text) #jasne
                root.clear() #po jedné sekvcni čistím - nepřehltím pamět

"""ZDE ŘEŠENÍ právě aby to nenatáhlo přes 4-5gb RAM"""
#https://stackoverflow.com/questions/35308623/in-pythons-elementree-
# library-how-to-use-iterparse-only-for-the-outer-level

"""____________________________[VYTVOŘÍ NOVÉ XML z listů]_____________________________"""

def zmensi_feed(nazev_feedu):
    """Nyní musíme vytvořit nový XML právě ze zadaných hodnot"""
    root_akt = etree.Element('PRODUCTS') #definujeme základní root
    for i in range(len(kod)): #iterujeme skrze delku jednoho z listu
        level1 = etree.SubElement(root_akt, "PRODUCT") #PRODUCT je level 1
        code = etree.SubElement(level1, 'CODE') #KOD patří pod level 1 - subelement
        code.text = kod[i] #a vkládáme jeho text z listu
        availability = etree.SubElement(level1, 'AVAILABILITY') 
        availability.text = dostupnost[i] #pro avalabiliy vkládáme hodnotu
        supplier_code = etree.SubElement(level1, 'SUPPLIER_CODE') 
        supplier_code.text = kod_dod[i] #pro supplier code vkládáme hodnotu

    tree = etree.ElementTree(root_akt) #finální uložení
    tree.write(nazev_feedu, pretty_print=True, xml_declaration=True, encoding="utf-8")

"""_________________________________[CELEK PRO 3 ESHOPY ]____________________________"""

#ČASEM DOLADIT - zrušit smyčku poměrně nedořešené a dodat ověření 200

def feed_celek(nazev_feedu, url): #předává název feedu a url adresu
    """STAHNE kompletni feed z eshopu -> vezme data a změní podle potřeby"""
    i = 0
    while i !=5: #definuji i smyčku pro 5 pokusů
        try: 
            cas = datetime.now().strftime("%H:%M:%S")
            stahne_feed(nazev_feedu, url) #stahneme
            print(f"{nazev_feedu.upper()} stažen v : {cas}")
            vydoluj_feed(nazev_feedu) #dolujeme data
            print(f"{nazev_feedu.upper()} zparsován v : {cas}")
            zmensi_feed(nazev_feedu) #zmešní a přeuložíme
            print(f"{nazev_feedu.upper()} zmenšen a uložen : {cas}")
            posli_email(f"ÚSPĚŠNĚ STAŽENÍ a ZPRACOVÁNÍ {nazev_feedu}","expedice@yescom.cz")
            i = 5 
        except: #pokud ok posíláme email naopak též
            i +=1 #v podstatě můj domácí retry mod pro funkci
            time.sleep(60) #tzn. dám každý funkci 5 minut rezervu aby proběhla
            if i == 5: #času na to je kotel klidně lze zvýšit na 10 poté
                posli_email(f"SELHÁNÍ STAŽENÍ a ZPRACOVÁNÍ: {nazev_feedu}", "expedice@yescom.cz")
    dostupnost.clear(), kod.clear(), kod_dod.clear() #čistím listy

"""________________________________________[MAIN]_____________________________________"""

dostupnost, kod, kod_dod = [], [], [] #základní listy čistím na závěr vždy

def main():
    feed_celek("yescom.xml",yescom_url)
    feed_celek("nabitabaterka.xml", nabitabaterka_url)
    feed_celek("ep.xml",ep_url)

if __name__ == "__main__":
    main()