# Warehouse_dynamic
<p>Synchronizace skladového hospodářství pro 3 online obchody.
  
## Základní informace:
<strong>1</strong> - sklad je vedený pouze v Google Sheets a Python propojení (skipnutí databáze) <br>
<strong>2</strong> - je třeba brát v potaz stav na skladě a stav u dodavatelů (pokud poskytují data)<br>
<strong>3</strong> - všechny online obchody mají jiné kody, ceny apod. - probíhá stažení XML feedů a jejich rozparsování (cca 1gb soubory)<br>
<strong>4</strong> - poté probíhá průnik dat z feedu x skladu x dodavatel => a vytváříme výsledný dostupností soubor - AKTUÁLNÍ STAV<br>
<strong>5</strong> - data získáváme přes XML feed - ale posíláme je zpátky přes API (tzn. JSON soubor)<br>
<strong>6</strong> - vše je řešeno pouze pomocí Cronu na Ubuntu servru a s jednoduchým timingem <br>

## Credentials.json
<p>Pouze pro propojeí Gsheets a Pythonu, nic víc. Generován až po vytvoření connectu.</br>

## b2b_loader.py
<p> Připojí se na dodavatele disponující stavy produktů a nahrává je do Gsheets.</p> <br>
<strong>Postup:</strong><br>
<strong>1</strong> - získá data z Gsheets => kody produktů, které má hledat ve feedu (aby knim našel počty)<br>
<strong>2</strong> - rozparsuje b2b feed a získá počty a kody produktů<br>
<strong>3</strong> - aktualizuje data tzn. průnik skladu x feedu<br>
<strong>4</strong> - nahraje stavy od dodavatele do Gsheets skladu<br>

<strong>Operce běží v Cronu každou 2 minutu v hodině, stačilo by 3x denně - záleží i na aktualizaci stavu u dodavatele.</strong>
  
## email_sender.py
<p>Zpětná vazba v případě výpadků apod. Jakmile nějaký kod selže zasílá email.<br>
  <strong>TODO: opravit čas - je vytvářen v bodě vzniku funkce!</strong>
  
## feed_cutter_v2.py
Skript, který 1x za den (cca ve 4 hodiny ráno) stáhne XML feedy ze tří online obchodů a vydoluje znich potebná data.<br>
V podstatě feedy zmenší. Feedu mají i 1gb takže poměrně náročné na paměť.<br>

<strong>Postup:</strong><br>
<strong>1</strong> - stáhneme XML feedy z eshopů a uložíme na disk (server cca 20gb zde max 3gb) <br>
<strong>2</strong> - rozparsujeme feedy - přes event a čistění paměti => jinak se přehltí a server spadne<br>
<strong>3</strong> - feed zmenšíme v podstatě chceme - kod produktu, dodavatelský kod a dostupností stav<br>
<strong>4</strong> - provedeme pro všechyn tři obchody naráz<br>

<strong>TODO: ověřovat dostupnost url na kod 200</strong><br>
<strong>Sciprt beží na servru jen 1x denně, cca 1 hodinu po XML aktualizace ze strany obchodů.</strong><br>

# bluuuuuu.py
<strong>Postup:</strong><br>
<strong>1</strong><br>
<strong>2</strong><br>
<strong>3</strong><br>
<strong>4</strong><br>

