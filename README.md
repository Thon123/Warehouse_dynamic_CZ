# Warehouse_dynamic
<p>Synchronizace skladového hospodářství pro 3 online obchody.
  
## Základní informace:
1 - Sklad je vedený pouze v Google Sheets - Python se připojí na sklad <br>
2 - Je třeba brát v potaz stav na skladě a stav u dodavatelů (pokud poskytují data)<br>
3 - Všechny online obchody mají jiné kody, jiné názvy, ceny apod. - Proběhně vždy stažení XML feedu a jejich rozparsování (cca 1gb soubory)<br>
4 - Poté probíhá průnik dat z feedu x skladu x dodavatel => a vytváříme výsledný dostupností soubor - AKTUÁLNÍ STAV
5 - Data získáváme přes XML feed - ale posíláme je zpátky přes API (tzn. JSON soubor)
6 - Vše je řešeno pouze pomocí Cronu na Ubuntu servru a s jednoduchým timingem 
