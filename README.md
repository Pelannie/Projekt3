# Treti Python projekt Elections Scraper - Engeto

Tento projekt na vyzadani uzivatelem scrapuje a sbira vysledky ze serveru [volby.cz](http://volby.cz/)

Program ocekava 2 argumenty: **adresu** a **nazev souboru** kam budou vysledky exportovany.

- Adresa : plna adresa uzemniho celku pro scrapovani - napr. [https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103](https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)

- Nazev souboru : exportovani vysledku do tohoto souboru ve formatu csv (s hlavickou) - napr. `vysledky_prostejov.csv`

## Potrebne knihovny

Pro spravnou funkci programu jsou potrebne nasledujici knihovny: `requests`, `urllib3` a `BeautifulSoup4`. Tyto lze nainstalovat nasledujicim prikazem:

`pip install requests urllib3 bs4`

## Spusteni projektu

Projekt lze spustit napriklad takto:

`python main.py https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_prostejov.csv`