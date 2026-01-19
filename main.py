import requests
import urllib3
import concurrent.futures

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

IZVORI = [
     "https://iptvm3u.vercel.app/"
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/rs.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ba.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hr.m3u",
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u",
    "https://raw.githubusercontent.com/volartv/volartv/master/playlist.m3u",
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/ba.m3u",
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/rs.m3u",
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/hr.m3u"
]

TRAZIMO = [
    "arena", "sport", "klub", "as 1", "as 2", "as 3", "premier", "champions",
    "bi h", "bih", "bosna", "srbija", "hrvatska", "bht", "ftv", "federalna", 
    "rts", "rtrs", "bn", "prva", "nova", "rtl", "hrt", "pink", "b92", 
    "cinestar", "hbo", "fox", "film", "movie", "balkan"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def provjeri_kanal(kanal_info):
    ime, url = kanal_info
    try:
        # TIMEOUT POVEĆAN NA 6 SEKUNDI (Za sporije Arene)
        with requests.get(url, stream=True, timeout=6, headers=HEADERS, verify=False) as r:
            # Prihvatamo kodove 200 (OK), 301/302 (Redirect)
            if r.status_code in [200, 301, 302]:
                return (ime, url)
    except:
        pass
    return None

def main():
    print("--- SKENIRANJE SA VEĆOM TOLERANCIJOM ---")
    
    kandidati = []
    vidjeni_linkovi = set()
    
    # 1. USISAVANJE
    for url in IZVORI:
        try:
            r = requests.get(url, timeout=15, verify=False)
            if r.status_code == 200:
                linije = r.text.split('\n')
                for i in range(len(linije)):
                    line = linije[i].strip()
                    if line.startswith("http"):
                        ime = "Nepoznat"
                        if i > 0 and linije[i-1].startswith("#EXTINF"):
                            ime = linije[i-1].strip()
                        
                        full_text = (ime + line).lower()
                        if any(k in full_text for k in TRAZIMO):
                            if line not in vidjeni_linkovi:
                                vidjeni_linkovi.add(line)
                                kandidati.append((ime, line))
        except: pass

    print(f"Kandidata: {len(kandidati)}")
    
    # 2. TESTIRANJE (50 radnika)
    zivi_kanali = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        rezultati = list(executor.map(provjeri_kanal, kandidati))
    
    for res in rezultati:
        if res: zivi_kanali.append(res)

    print(f"--- PREŽIVJELO: {len(zivi_kanali)} ---")

    # 3. SNIMANJE
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ime, url in zivi_kanali:
            if "group-title" not in ime:
                ime = ime.replace("#EXTINF:-1", '#EXTINF:-1 group-title="JokerTV"')
            f.write(f"{ime}\n{url}\n")

if __name__ == "__main__":
    main()
