import requests
import re
import csv


def zajem_html(url):
    """Funkcija kot argument prejme niz in poskusi vrniti html spletne
    strani kot niz. V primeru, da med izvajanjem pride do napake vrne None.
    """
    try:
        headers = {"User-agent": "Chrome/149.0.7827.103"}
        html = requests.get(url, headers=headers, timeout=5)
        html.raise_for_status()
    except requests.exceptions.RequestException:
        print("Spletna stran ni dosegljiva")
        return None

    return html.text


def shrani_html(html, datoteka):
    """Funkcija zapiše vsebino parametra "html" v novo ustvarjeno datoteko,
    ali povozi obstoječo.
    """
    with open(datoteka, "w", encoding="utf-8") as dat:
        dat.write(html)


def izlusci_gorovja(html):
    """Funkcija kot argument prejme html kot niz, izlušči imena gorovij in
    pripadajoče povezave ter jih vrne v obliki seznama slovarjev.
    """
    vzorec = re.compile(
        r'<a href="(?P<url>/gorovje/[^"]+)">(?P<ime>[^<]+)</a>',
        re.DOTALL
    )
    gorovja = []
    for zadetek in vzorec.finditer(html):
        gorovja.append({
            "ime": zadetek.group("ime").strip(),
            "url": zadetek.group("url")
        })

    return gorovja


def izlusci_gore(html):
    """Funkcija kot argument prejme html strani posameznega gorovja v obliki
    niza in vrne seznam slovarjev z imeni gora in pripadajočimi povezavami.
    """
    vzorec = re.compile(
        r'<a href="(?P<url>/gora/[^"]+)">(?P<ime>[^<]+)</a>'
    )
    gore = []
    for zadetek in vzorec.finditer(html):
        ime = zadetek.group("ime").strip()
        if "&nbsp;m" in ime:
            continue

        gore.append({
            "ime": zadetek.group("ime").strip(),
            "url": zadetek.group("url")
        })

    return gore


def zberi_vse_gore(gorovja):
    """Funkcija kot argument prejme seznam gorovij in za vsako prenese njegovo
    spletno stran ter iz nje izlušči seznam gora. Vse podatke združi v en
    skupen seznam slovarjev, kjer vsak vsebuje ime gorovja, ime gore in URL
    do posamezne gore.
    """
    glavni_url = "https://www.hribi.net"
    vse_gore = []
    gora_id = 1
    for gorovje in gorovja:
        html_gorovje = zajem_html(glavni_url + gorovje["url"])

        if html_gorovje is None:
            print("Napaka pri:", gorovje["url"])
            continue

        gore = izlusci_gore(html_gorovje)

        for gora in gore:
            vse_gore.append({
                "id": gora_id,
                "gorovje": gorovje["ime"],
                "ime": gora["ime"],
                "url": glavni_url + gora["url"]
            })
            gora_id += 1

    return vse_gore


def izlusci_podatke_o_gori(html):
    """Funkcija iz html-ja spletne strani o posamezni gori
    izlušči podatke o gori.
    """
    ime = re.search(r'<title>\s*(.*?)\s*</title>', html)
    gorovje = re.search(r'Gorovje:\s*</b>\s*<a[^>]*>(.*?)</a>', html)
    visina = re.search(r'Višina:\s*</b>\s*([\d]+)\s*&nbsp;m', html)
    priljubljenost = re.search(r'Priljubljenost[^0-9]*([0-9]+)', html)
    ogledi = re.search(r'Ogledov:\s*</b>\s*([\d\.]+)', html)

    return {
        "ime": ime.group(1).strip() if ime else None,
        "gorovje": gorovje.group(1).strip() if gorovje else None,
        "visina": int(visina.group(1)) if visina else None,
        "priljubljenost": int(priljubljenost.group(1)) if priljubljenost else None,
        "ogledi": int(ogledi.group(1).replace(".", "")) if ogledi else None
    }


def izlusci_poti(html):
    """Izlušči poti iz strani posamezne gore."""
    vzorec = re.compile(
        r'<tr[^>]*class="trG[01]"[^>]*>\s*'
        r'<td[^>]*>.*?<a[^>]*>(?P<ime>[^<]+)</a>.*?</td>\s*'
        r'<td[^>]*>.*?(?P<cas>\d+\s*h(?:\s*\d+\s*min)?|\d+\s*min)\s*</a>.*?</td>\s*'
        r'<td[^>]*>.*?<a[^>]*>(?P<zahtevnost>[^<]+)</a>.*?</td>',
        re.DOTALL
    )

    poti = []
    for zadetek in vzorec.finditer(html):
        poti.append({
            "ime": zadetek.group("ime").strip(),
            "cas": zadetek.group("cas").strip(),
            "zahtevnost": zadetek.group("zahtevnost").strip()
        })

    return poti


def cas_v_minute(cas):
    """Pretvori čas oblike '2 h 10 min' v minute."""
    ure = re.search(r'(\d+)\s*h', cas)
    minute = re.search(r'(\d+)\s*min', cas)
    ure = int(ure.group(1)) if ure else 0
    minute = int(minute.group(1)) if minute else 0

    return ure * 60 + minute


def zberi_podrobnosti_vseh_gor(seznam_gor):
    """Funkcija za vsak element v seznamu gor prenese html strani gore,
    izlušči podrobnosti in rezultat doda v nov seznam.
    """
    vse_podrobnosti = []
    vse_poti = []
    for gora in seznam_gor:
        html = zajem_html(gora["url"])
        if html is None:
            continue

        podatki = izlusci_podatke_o_gori(html)
        podatki["id"] = gora["id"]
        poti = izlusci_poti(html)
        podatki["stevilo_poti"] = len(poti)
        vse_podrobnosti.append(podatki)

        for pot in poti:
            vse_poti.append({
                "gora_id": gora["id"],
                "ime": pot["ime"],
                "cas": cas_v_minute(pot["cas"]),
                "zahtevnost": pot["zahtevnost"]
            })

    return vse_podrobnosti, vse_poti


def shrani_v_csv(podatki, datoteka, polja):
    """Podatke zapiše v CSV datoteko z izbranimi stolpci."""
    with open(datoteka, "w", newline="", encoding="utf-8") as f:
        pisec = csv.DictWriter(f, fieldnames=polja, extrasaction="ignore")
        pisec.writeheader()
        for objekt in podatki:
            pisec.writerow(objekt)
