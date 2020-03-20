#!/usr/bin/python3
from settings import *
from email_sender import posli_email

"""________________________________[ PUT REQUEST API ]"________________________________"""
def posli_json(nazev_souboru, url_api, jmeno_api, heslo_api):
    """Funkce pro posílání aktualizačních JSON souborů přes API"""
    try: #použití put requestu s with open - json soubor
        with open(nazev_souboru, encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            response = requests.put(
                url_api,
                auth=HTTPBasicAuth(jmeno_api,heslo_api), #autorizace
                data=json.dumps(json_data), #data jsou json soubor
                headers={"Content-Type": "application/json"},)
        print(response.text)
    except: #pouze info pokud něco selše a poslání emailu
        posli_email(f"SELHÁNÍ JSON: {nazev_souboru}", "expedice@yescom.cz")
        print(f"{nazev_souboru} propojení selhalo")


"""________________________________[ PUT REQUEST API ]"________________________________"""

def main():
    """Pošle pro všechny obchody naráz"""
    posli_json("yescom.json", url_yescom, jmeno_yescom, heslo_yescom)
    posli_json("ep.json", url_ep, jmeno_ep, heslo_ep)
    posli_json("nabitabaterka.json", url_nb, jmeno_nb, heslo_nb)

if __name__ == "__main__":
    main()