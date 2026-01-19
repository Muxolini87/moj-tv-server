import requests

# Ovi linkovi rade 100% (Provjereno sad)
IZVORI = [
    "https://iptv-org.github.io/iptv/countries/ba.m3u", # Bosna
    "https://iptv-org.github.io/iptv/countries/hr.m3u", # Hrvatska
    "https://iptv-org.github.io/iptv/countries/rs.m3u", # Srbija
    "https://iptv-org.github.io/iptv/countries/mk.m3u", # Makedonija
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u" # Sport Mix
]

def main():
    print("--- SPAJAM LISTE... ---")
    
    # Otvaramo fajl i pisemo zaglavlje
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for url in IZVORI:
            print(f"Skidam sa: {url}...")
            try:
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    # Uzimamo tekst
                    sadrzaj = r.text
                    
                    # Razdvajamo na linije
                    linije = sadrzaj.split('\n')
                    
                    # Ako prva linija sadrzi #EXTM3U, preskacemo je (jer vec imamo nasu)
                    if linije and "#EXTM3U" in linije[0]:
                        linije = linije[1:]
                    
                    # Upisujemo sve ostalo u nas fajl
                    f.write('\n'.join(linije) + "\n")
                    print(f"   -> USPJEH! Dodano linija: {len(linije)}")
                else:
                    print(f"   -> GRESKA! Server vratio kod: {r.status_code}")
            except Exception as e:
                print(f"   -> GRESKA! {e}")

    print("--- GOTOVO ---")

if __name__ == "__main__":
    main()
