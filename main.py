import requests
import urllib3

# Gasimo sigurnost da mozemo vuci sa sumnjivih servera
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- IZVORI SMRTI (NAJVECE LISTE NA INTERNETU) ---
IZVORI = [
    # Balkanske Specijalne
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/ba.m3u",
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/hr.m3u",
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/rs.m3u",
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/mk.m3u",
    # Sport Mixevi
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u",
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list",
    # SVJETSKI GIGANTI (Sadrze sve zivo)
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8",
    "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
    "https://raw.githubusercontent.com/ramoc1/IPTV-2021/master/iptv.m3u",
    "https://iptv-org.github.io/iptv/index.m3u"
]

# --- FILTER (DA NE GLEDAS KINESKE REKLAME) ---
# Trazimo bilo sta od ovoga:
FILTERI = [
    # SPORT (Sve varijante)
    "arena", "sport", "klub", "premier", "euro", "champions", "nba", "ufc", "fight", "racing", "f1",
    # EX-YU (Sve varijante)
    "bht", "ftv", "federalna", "rtrs", "bn", "hayat", "face", "obn", "kakanj", "sarajevo", "zenica", "tuzla",
    "hrt", "rtl", "nova", "doma", "cinestar", "klasik",
    "rts", "prva", "b92", "pink", "happy", "superstar", "zadruga",
    "slovenija", "macedonia", "montenegro", "bosnia", "serbia", "croatia", "balkan", "exyu",
    # FILMOVI I SERIJE
    "hbo", "fox", "film", "movie", "serija", "cinema", "action", "comedy",
    # ODRASLI (Ako hoces XXX, otkomentarisi donju liniju brisanjem tarabe #)
    # "xxx", "porn", "adult", "18+" 
]

def main():
    print("--- POKRECEM MEGALOMANSKI USISIVAC ---")
    
    # Koristimo 'set' za linkove da izbjegnemo duplikate (da nemas 5 istih Arena)
    vidjeni_linkovi = set()
    
    f = open("lista.m3u", "w", encoding="utf-8")
    f.write("#EXTM3U\n")
    
    brojac = 0
    
    for url in IZVORI:
        print(f"Meljem izvor: {url[-20:]}...")
        try:
            r = requests.get(url, timeout=20, verify=False)
            
            if r.status_code == 200:
                linije = r.text.split('\n')
                print(f"   -> Uspjeh! Nasao {len(linije)} linija.")
                
                for i in range(len(linije)):
                    line = linije[i].strip()
                    
                    if line.startswith("http"):
                        # Ime kanala
                        ime = "Nepoznat Kanal"
                        if i > 0:
                            prev = linije[i-1].strip()
                            if prev.startswith("#EXTINF"):
                                ime = prev
                        
                        # Provjera FILTERA
                        full_text = (ime + line).lower()
                        
                        if any(k in full_text for k in FILTERI):
                            # Provjera DUPLIKATA
                            if line not in vidjeni_linkovi:
                                vidjeni_linkovi.add(line)
                                
                                # Lijepo formatiranje imena
                                if "group-title" not in ime:
                                    ime = ime.replace("#EXTINF:-1", '#EXTINF:-1 group-title="JokerMix"')
                                
                                f.write(ime + "\n")
                                f.write(line + "\n")
                                brojac += 1
            else:
                print(f"   -> Blokada (Kod: {r.status_code})")
                
        except Exception as e:
            print(f"   -> Greska: {e}")

    f.close()
    print("="*40)
    print(f"BOLESNO! LISTA IMA {brojac} KANALA!")
    print("="*40)

if __name__ == "__main__":
    main()
