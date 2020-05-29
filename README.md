# Warehouse_dynamic
<p>Synchronizace skladového hospodářství pro 3 online obchody.
  
## Základní informace:
<strong>1</strong> - Sklad je vedený pouze v Google Sheets a Python propojení (skipnutí databáze) <br>
<strong>2</strong> - Je třeba brát v potaz stav na skladě a stav u dodavatelů (pokud poskytují data)<br>
<strong>3</strong> - Všechny online obchody mají jiné kody, ceny apod. - probíhá stažení XML feedů a jejich rozparsování (cca 1gb soubory)<br>
<strong>4</strong> - Poté probíhá průnik dat z feedu x skladu x dodavatel => a vytváříme výsledný dostupností soubor - AKTUÁLNÍ STAV<br>
<strong>5</strong> - Data získáváme přes XML feed - ale posíláme je zpátky přes API (tzn. JSON soubor)<br>
<strong>6</strong> - Vše je řešeno pouze pomocí Cronu na Ubuntu servru a s jednoduchým timingem <br>

## Credentials.json
<p>Pouze pro propojeí Gsheets a Pythonu, nic víc. Generován až po vytvoření connectu.</br>

## b2b_loader.py
<p> Připojí se na dodavatele disponující stavy produktů a nahrává je do Gsheets. <br>
<strong>Postup:</strong><br>
<strong>1</strong> - Získá data z Gsheets => kody produktů, které má hledat ve feedu (aby knim našel počty)<br>
<strong>2</strong> - Rozparsuje b2b feed a získá počty a kody produktů<br>
<strong>3</strong> - Aktualizuje data tzn. průnik skladu x feedu<br>
<strong>4</strong> - Nahraje stavy od dodavatele do Gsheets skladu<br>
<strong>Operce běží v Cronu každou 2 minutu v hodině, stačilo by 3x denně - záleží i na aktualizaci stavu u dodavatele</strong>
  
## email_sender.py
<p>Zpětná vazba v případě výpadků apod. Jakmile nějaký kod selže zasílá email.<br>
  <strong>TODO: opravit čas - je vytvářen v bodě vzniku funkce!</strong>
  
## bluuu.py

