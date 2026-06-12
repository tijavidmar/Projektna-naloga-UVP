import requests


def zajem_html(url):
    """Funkcija kot argument prejme niz in poskusi vrniti html spletne
    strani kot niz. V primeru, da med izvajanjem pride do napake vrne None.
    """
    try:
        headers = {"User-agent": "Chrome/149.0.7827.103"}
        html = requests.get(url, headers=headers)
        html.raise_for_status()
    except requests.exceptions.RequestException:
        print("Spletna stran ni dosegljiva")
        return None
    return html.text


def shrani_html(html, datoteka):
    """Funkcija zapiše vsebino parametra "html" v novo ustvarjeno datoteko
    locirano v podani datoteki, ali povozi obstoječo. 
    """
    with open(datoteka, "w", encoding="utf-8") as dat:
        dat.write(html)