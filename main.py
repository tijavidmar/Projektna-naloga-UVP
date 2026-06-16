import funkcije
import os

url_glavne_strani = "https://www.hribi.net/gorovja"
mapa_za_shranjevanje = "podatki"


os.makedirs(mapa_za_shranjevanje, exist_ok=True)

html = funkcije.zajem_html(url_glavne_strani)

if html is not None:
    pot = os.path.join(mapa_za_shranjevanje, "gorovja.html")
    funkcije.shrani_html(html, pot)

gorovja = funkcije.izlusci_gorovja(html)

vse_gore = funkcije.zberi_vse_gore(gorovja)

podatki_gor, vse_poti = funkcije.zberi_podrobnosti_vseh_gor(vse_gore)

funkcije.shrani_v_csv(podatki_gor, "gore.csv", [
    "id", "ime", "gorovje", "visina", "ogledi", "priljubljenost",
    "stevilo_poti"])

funkcije.shrani_v_csv(vse_poti, "poti.csv", [
    "gora_id", "ime", "cas", "zahtevnost"
    ])
