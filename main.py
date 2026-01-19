import requests
import urllib3

# Iskljucujemo upozorenja za sigurnost (idemo na silu)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- IZVORI ---
IZVORI = [
    "https://iptv-org.github.io/iptv/countries/ba.m3u", # Bosna
    "https://iptv-org.github.io/iptv/countries/hr.m3u", # Hrvatska
    "https://iptv-org.github.io/iptv/countries/rs.m3u", # Srbija
    "https://raw.githubusercontent.com/notanewbie/LegalStream/main/packages/sport.m3u" # Sport
]

def main():
    print("--- POČINJEM DIAGNOSTIKU ---")
    
    # Otvaramo fajl
    f = open("lista.m3u", "w", encoding="utf-8")
    
    # Pisemo zaglavlje
    f.write("#EXTM3U\n")
    
    # 1. UPISUJEMO TESTNI KANAL (DA VIDIMO RADI LI PISANJE)
    f.write('#EXTINF:-1 group-title="Test", --- AKO VIDIS OVO PISANJE RADI ---\n')
    f.write("http://google.com\n")
    
    # 2. SKIDANJE KANALA (NA SILU)
    for url in IZVORI:
        print(f"Pokusavam skinuti: {url}...")
        try:
            # verify=False znaci: "Ne provjeravaj sigurnost, samo daj podatke"
            r = requests.get(url, timeout=30, verify=False)
            
            print(f"   -> KOD SERVERA: {r.status_code}")
            
            if r.status_code == 200:
                sadrzaj = r.text
                # Micemo #EXTM3U iz tudjih lista da ne kvari nasu
                sadrzaj = sadrzaj.replace("#EXTM3U", "")
                f.write(sadrzaj + "\n")
                print("   -> USPJEH! Podaci upisani.")
            else:
                print("   -> BLOKADA! Server ne da podatke robotu.")
                
        except Exception as e:
            print(f"   -> GRESKA KONEKCIJE: {e}")

    f.close()
    print("--- GOTOVO ---")

if __name__ == "__main__":
    main()
