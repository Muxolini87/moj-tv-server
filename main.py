import requests

# --- IZVORI (AGRESIVNA LISTA) ---
# Ovdje kupimo sve sa Balkana sto postoji na GitHubu
IZVORI = [
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/ba.m3u", # Bosna
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/hr.m3u", # Hrvatska
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/rs.m3u", # Srbija
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/mk.m3u", # Makedonija
    "https://raw.githubusercontent.com/junguler/iptv-playlist/main/playlists/si.m3u", # Slovenija
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list", # Mix
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u" # Sport Mix
]

# --- KLJUCNE RIJECI (STA TRAZIMO) ---
# Trazimo sve varijacije imena
TRAZIMO = [
    # SPORT (Najbitnije)
    "arena", "sport", "klub", "sk 1", "sk 2", "sk 3", "premier", 
    "mytv", "moja tv", "eurosport", "nba", "champions",
    # BOSNA
    "bht", "ftv", "federalna", "rtrs", "bn", "hayat", "face", "obn", "kakanj", "sarajevo", "al jazeera",
    # HRVATSKA
    "hrt", "rtl", "nova", "doma", "cinestar",
    # SRBIJA
    "rts", "prva", "b92", "pink", "happy", "superstar",
    # OSTALO
    "film", "hbo", "fox", "cine", "balkan", "exyu"
]

# Maska da nas ne blokiraju
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def main():
    print("--- POCINJEM SAKUPLJANJE BALKANSKIH KANALA ---")
    konacna_lista = ["#EXTM3U"]
    brojac = 0
    
    for izvor in IZVORI:
        print(f"Usisavam: {izvor.split('/')[-1]}...")
        try:
            r = requests.get(izvor, timeout=15, headers=HEADERS)
            if r.status_code == 200:
                linije = r.text.split('\n')
                
                for i in range(len(linije)):
                    linija = linije[i].strip()
                    
                    # Ako nadjemo info o kanalu
                    if linija.startswith("#EXTINF") and i+1 < len(linije):
                        url = linije[i+1].strip()
                        
                        # Ako url nije prazan i pocinje sa http
                        if url.startswith("http"):
                            # Izdvajamo ime kanala radi provjere
                            ime_kanala = linija.split(',')[-1].strip()
                            
                            # DA LI JE OVO ONO STO TRAZIMO?
                            # Provjeravamo sadrzi li ime kanala neku od nasih kljucnih rijeci
                            if any(kljuc.lower() in ime_kanala.lower() for kljuc in TRAZIMO):
                                
                                # Malo uljepsavanja imena grupe
                                grupa = "Balkan-Mix"
                                if "arena" in ime_kanala.lower() or "sport" in ime_kanala.lower():
                                    grupa = "SPORT-JOKER"
                                elif "bht" in ime_kanala.lower() or "ftv" in ime_kanala.lower() or "mytv" in ime_kanala.lower():
                                    grupa = "BIH-DOMACI"
                                
                                # Dodajemo u nasu listu BEZ PROVJERE (Da izvucemo sve moguce)
                                konacna_lista.append(f'#EXTINF:-1 group-title="{grupa}",{ime_kanala}')
                                konacna_lista.append(url)
                                brojac += 1
                                print(f"   [+] Nasao: {ime_kanala}")

        except Exception as e:
            print(f"   [!] Greska sa izvorom: {e}")

    # Snimanje
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write('\n'.join(konacna_lista))
    
    print("="*40)
    print(f"GOTOVO! UKUPNO KANALA: {brojac}")
    print("Link za player je u fajlu 'lista.m3u'")
    print("="*40)

if __name__ == "__main__":
    main()
