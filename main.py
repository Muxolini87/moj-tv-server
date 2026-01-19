import requests
import urllib3

# Iskljucujemo blokade (ovo je kljuc uspjeha)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- BOLESNE LISTE (SVE ZIVO) ---
IZVORI = [
    # Junguler (Najbolji za Balkan)
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/ba.m3u", # Bosna
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/hr.m3u", # Hrvatska
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/rs.m3u", # Srbija
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/mk.m3u", # Makedonija
    # Sport Mixevi
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u",
    # Mix Balkana (Djaweb)
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list"
]

# --- STA TRAZIMO (DA NE BUDE KINESKIH KANALA) ---
FILTERI = [
    "arena", "sport", "klub", "premier", "euro", "champions", "nba", # Sport
    "bht", "ftv", "federalna", "rtrs", "bn", "hayat", "face", "obn", "kakanj", # BiH
    "hrt", "rtl", "nova", "doma", "cinestar", # HR
    "rts", "prva", "b92", "pink", "happy", "superstar", # SRB
    "hbo", "fox", "film", "movie", "serija", "balkan", "exyu" # Ostalo
]

def main():
    print("--- POKRECEM USISIVAC KANALA ---")
    
    f = open("lista.m3u", "w", encoding="utf-8")
    f.write("#EXTM3U\n")
    
    brojac = 0
    
    for url in IZVORI:
        print(f"Napadamo izvor: {url[-15:]}...")
        try:
            # OVO JE MAGICNA LINIJA (verify=False)
            r = requests.get(url, timeout=30, verify=False)
            
            if r.status_code == 200:
                linije = r.text.split('\n')
                print(f"   -> Uspjeh! Nasao {len(linije)} linija.")
                
                for i in range(len(linije)):
                    line = linije[i].strip()
                    
                    if line.startswith("http"):
                        # Pokusavamo naci ime iznad linka
                        ime = "Nepoznat Kanal"
                        if i > 0:
                            prev = linije[i-1].strip()
                            if prev.startswith("#EXTINF"):
                                ime = prev
                        
                        # Provjera (Da li je nas kanal?)
                        full_text = (ime + line).lower()
                        if any(k in full_text for k in FILTERI):
                            # Upisujemo!
                            if not ime.startswith("#EXTINF"):
                                f.write(f'#EXTINF:-1 group-title="Balkan-Mix", Kanal {brojac}\n')
                            else:
                                f.write(ime + "\n")
                            
                            f.write(line + "\n")
                            brojac += 1
            else:
                print(f"   -> Blokada (Kod: {r.status_code})")
                
        except Exception as e:
            print(f"   -> Greska: {e}")

    f.close()
    print("="*40)
    print(f"GOTOVO! UPISANO {brojac} KANALA!")
    print("="*40)

if __name__ == "__main__":
    main()
