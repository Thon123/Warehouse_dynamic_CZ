# Warehouse_dynamic
<p>Synchronizace skladového hospodářství pro 3 online obchody.
  
## Základní informace:
<strong>1</strong> - Sklad je vedený pouze v Google Sheets a Python propojení (skipnutí databáze) <br>
<strong>2</strong> - Je třeba brát v potaz stav na skladě a stav u dodavatelů (pokud poskytují data)<br>
<strong>3</strong> - Všechny online obchody mají jiné kody, ceny apod. - probíhá stažení XML feedů a jejich rozparsování (cca 1gb soubory)<br>
<strong>4</strong> - Poté probíhá průnik dat z feedu x skladu x dodavatel => a vytváříme výsledný dostupností soubor - AKTUÁLNÍ STAV<br>
<strong>5</strong> - Data získáváme přes XML feed - ale posíláme je zpátky přes API (tzn. JSON soubor)<br>
<strong>6</strong> - Vše je řešeno pouze pomocí Cronu na Ubuntu servru a s jednoduchým timingem <br>

##Credentials.json
<p>Pouze pro propojeí Gsheets a Pythonu, nic víc. Generován až po vytvoření connectu.</br>

##jjj
