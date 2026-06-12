import funkcije
import os

url_glavne_strani = "https://www.hribi.net/gorovja"
mapa_za_shranjevanje = "podatki"
datoteka_gorovja = 'gorovja.html'
csv_gore = 'gore.csv'


os.makedirs(mapa_za_shranjevanje, exist_ok=True)

html = funkcije.zajem_html(url_glavne_strani)

# 3. shrani v datoteko znotraj mape
if html is not None:
    pot = os.path.join(mapa_za_shranjevanje, "gorovja.html")
    funkcije.shrani_html(html, pot)