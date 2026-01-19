import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Trazimo liste koje sadrze user/pass kombinacije (Dumpovi)
IZVORI = [
    "https://raw.githubusercontent.com/djaweb/djaweb/master/iptv_list",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/rs.m3u",
    "https://raw.githubusercontent.com/listas-iptv/iptv-listas/master/iptv.m3u",
    "https://raw.githubusercontent.com/appatver/iptv/master/iptv.m3u",
    "https://raw.githubusercontent.com/sazzad666/IPTV/master/playlist.m3u"
]

# Trazimo BILO STA sto lici na Arenu, ali samo ako je link "ozbiljan"
TRAZIMO = ["arena", "sport", "klub", "premier", "champions", "as 1", "as 2"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def main():
    print("--- TRAZIM PROBIJENE SERVERE (USER/PASS) ---")
    
    f = open("lista.m3u", "w", encoding="utf-8")
    f.write("#EXTM3U\n")
    brojac = 0
    
    for url in IZVORI:
        try:
            r = requests.get(url, timeout=15, verify=False)
            linije = r.text.split('\n')
            
            for i in range(len(linije)):
                line = linije[i].strip()
                
                if line.startswith("http"):
                    # PRVI UVJET: Link mora liciti na placeni server
                    # (mora imati port :8080, :80, :25461 ili username=)
                    je_ozbiljan_server = False
                    if ":80" in line or "username=" in line or "token=" in line:
                        je_ozbiljan_server = True
                    
                    if je_ozbiljan_server:
                        # DRUGI UVJET: Mora biti Arena ili Sport
                        ime = "Nepoznat Kanal"
                        if i > 0 and linije[i-1].startswith("#EXTINF"):
                            ime = linije[i-1]
                        
                        full_text = (ime + line).lower()
                        
                        if any(k in full_text for k in TRAZIMO):
                            # BINGO! Nasli smo placeni link koji je procurio
                            if not ime.startswith("#EXTINF"):
                                f.write(f'#EXTINF:-1 group-title="HAKOVANO-VIP", Kanal {brojac}\n')
                            else:
                                f.write(ime + "\n")
                            f.write(line + "\n")
                            brojac += 1
        except: pass

    f.close()
    print(f"--- GOTOVO! NASAO SAM {brojac} VIP KANALA ---")

if __name__ == "__main__":
    main()
