import requests
import urllib3

# Gasimo upozorenja
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- RUSKE I SVJETSKE PIRATSKE LISTE ---
IZVORI = [
    # Tvoja omiljena (Djaweb)
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list",
    # Ruska masina (Cesto ima Balkana)
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/rs.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ba.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hr.m3u",
    # Mixevi
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u",
    "https://raw.githubusercontent.com/volartv/volartv/master/playlist.m3u"
]

# --- SIROKI FILTERI ---
# Trazimo krace rijeci da uhvatimo i "AS 1" i "Arena"
TRAZIMO = [
    # Sport (Sve varijante)
    "arena", "sport", "klub", "as 1", "as 2", "as 3", "as 4", 
    "premier", "fudbal", "nogomet", "liga", "champions",
    # Nasi kanali (Sve varijante)
    "bi h", "bih", "bosna", "srbija", "serbia", "hrvatska", "croatia",
    "rts", "rtrs", "bn", "prva", "nova", "rtl", "hrt", "bht", "ftv",
    "pink", "zadruga", "happy", "kurir", "b92", "studio b",
    "cinestar", "hbo", "fox", "film"
]

def main():
    print("--- POKRECEM NUKLEARNI SKENER ---")
    
    f = open("lista.m3u", "w", encoding="utf-8")
    f.write("#EXTM3U\n")
    
    brojac = 0
    
    for url in IZVORI:
        print(f"Kopam po: {url[-20:]}...")
        try:
            r = requests.get(url, timeout=20, verify=False)
            
            if r.status_code == 200:
                linije = r.text.split('\n')
                
                for i in range(len(linije)):
                    line = linije[i].strip()
                    
                    if line.startswith("http"):
                        # Ime kanala
                        ime = "Nepoznat Kanal"
                        if i > 0:
                            prev = linije[i-1].strip()
                            if prev.startswith("#EXTINF"):
                                ime = prev
                        
                        # Spajamo ime i link u mala slova za provjeru
                        full_text = (ime + line).lower()
                        
                        # PROVJERA (Je li to ono sto trazimo?)
                        if any(k in full_text for k in TRAZIMO):
                            
                            # Ako je ime "AS 1", mi ga uljepsamo da pise "ARENA"
                            if "as 1" in ime.lower() or "as1" in ime.lower():
                                ime = ime + " (MOGUCA ARENA 1)"
                            
                            # Pisemo u fajl
                            if not ime.startswith("#EXTINF"):
                                f.write(f'#EXTINF:-1 group-title="JokerMix", Kanal {brojac}\n')
                            else:
                                f.write(ime + "\n")
                            
                            f.write(line + "\n")
                            brojac += 1
        except Exception as e:
            print(f"Greska: {e}")

    f.close()
    print("="*40)
    print(f"GOTOVO! UPISANO {brojac} KANALA!")
    print("="*40)

if __name__ == "__main__":
    main()
