# Analiza slovenskih gora
Projektna naloga pri predmetu Uvod v programiranje.

## Opis projektne naloge

Cilj naloge je zajeti in analizirati podatke o slovenskih gorah in planinskih poteh s spletne strani [hribi.net](https://www.hribi.net/gorovja).

Program samodejno prenese podatke o gorovjih, gorah in planinskih poteh, jih obdela ter shrani v CSV datoteke. Nato so podatki analizirani v Jupyter Notebooku, kjer so predstavljeni z grafi in statističnimi primerjavami.

## Zbrani podatki

Za vsako goro zberemo:
- ime gore,
- gorovje,
- višino,
- število ogledov na spletni strani,
- priljubljenost,
- število poti.

Za posamezno pot zberemo:
- ime poti,
- čas hoje v minutah,
- zahtevnost.

> Opomba: Pri nekaterih gorah se napisano število poti ne ujema s številom naštetih poti na spletni strani, zato sem za poti posamezne gore upoštevala samo naštete poti.

## Zgradba in delovanje naloge

Zajem podatkov izvedemo z zagonom datoteke `main.py`. Ta predstavlja glavni del programa in vodi celoten postopek pridobivanja podatkov. Pri tem uporablja funkcije, definirane v datoteki `funkcije.py`, kjer so zbrane funkcije za prenos spletne strani, izluščanje podatkov iz HTML-ja ter shranjevanje rezultatov v datoteke CSV.

Program najprej pridobi seznam gorovij, nato za vsako gorovje zbere podatke o gorah, za vsako goro pa še podrobnejše podatke in seznam dostopnih poti. Rezultati se shranijo v datoteki `gore.csv` in `poti.csv`.

Analiza zbranih podatkov je predstavljena v datoteki `analiza.ipynb`.