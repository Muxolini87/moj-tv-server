import requests

# --- IZVORI ---
# Koristimo direktne liste koje nisu osjetljive na blokade
IZVORI = [
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list", 
    "https://raw.githubusercontent.com/volartv/volartv/master/playlist.m3u",
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u",
    "https://raw.githubusercontent.com/jnk22/kod/master/m3u/srb.m3u", # Srbija
    "https://raw.githubusercontent.com/jnk22/kod/master/m3u/bih.m3u", # Bosna
    "https://raw.githubusercontent.com/jnk22/kod/master/m3u/hrv.m3u"  # Hrvatska
]

# --- KLJUCNE RIJECI ---
# Ako ime kanala sadrzi BILO STA od ovoga, uzimamo ga!
TRAZIMO = [
    "arena", "sport", "klub", "premier", "euro", "champions", "nba", # Sport
    "bht", "ftv", "federalna", "rtrs", "bn", "hayat", "face", "obn", # BiH
    "hrt", "rtl", "nova", "doma", "cinestar", # HR
    "rts", "prva", "b92", "pink", "happy", "superstar", # SRB
    "hbo", "fox", "film", "movie", "serija", "balkan", "exyu" # Ostalo
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def main():
    print("--- TRAZIM KANALE... ---")
    
    # Otvaramo fajl za pisanje
    f = open("lista.m3u", "w", encoding="utf-8")
    f.write("#EXTM3U\n")
    
    brojac = 0
    
    for izvor in IZVORI:
        print(f"Obradjujem: {izvor}...")
        try:
            r = requests.get(izvor, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                lines = r.text.split('\n')
                
                for i in range(len(lines)):
                    line = lines[i].strip()
                    
                    # Trazimo link
                    if line.startswith("http"):
                        # Ime je obicno u liniji iznad
                        ime_kanala = "Nepoznat Kanal"
                        if i > 0:
                            prev_line = lines[i-1].strip()
                            if prev_line.startswith("#EXTINF"):
                                ime_kanala = prev_line
                        
                        # Provjera (Case Insensitive)
                        full_text = (ime_kanala + line).lower()
                        
                        if any(k in full_text for k in TRAZIMO):
                            # Upisujemo u fajl
                            if not ime_kanala.startswith("#EXTINF"):
                                f.write(f'#EXTINF:-1 group-title="BalkanMix", Kanal {brojac}\n')
                            else:
                                f.write(ime_kanala + "\n")
                            
                            f.write(line + "\n")
                            brojac += 1
        except:
            pass

    f.close()
    print(f"--- GOTOVO! UPISANO {brojac} KANALA ---")

if __name__ == "__main__":
    main()
