# Python libs
import sys
import time
import re
import os
import json

# Custom libs
import requests
import bs4 

class LyricScrapper():
    def __init__(self, path=os.getcwd() + "/output"):
        self.download_path = path
        self.session = requests.Session()

        # check if output folder exists if not then create one
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def download_lyric(self, url):
        # http request to the site
        req = self.session.get(url)

        # parsed html
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        # song text div
        song_text_html = soup.find('div', attrs={'class': 'song-text'})

        try:
            song_text_html.h2.extract()
            song_text_html.p.extract()
            song_text_html.a.extract()
            song_text_html.div.extract()
        except AttributeError:
            print("Error")       

        song_text = song_text_html.get_text()

        pattern1 = re.compile(r"\n\n\n\t\t\t\t")
        pattern2 = re.compile(r"\n\n\t\t\t\t\n\n\n")

        song_text = pattern1.sub('', song_text)
        song_text = pattern2.sub('', song_text)

        song_info = url.split("/")[3].split(".")[0].split(",")
        song_info.pop(0)

        artist_path = self.download_path + f"/{song_info[0]}"

        # check if artist folder exists if not then create one
        if not os.path.exists(artist_path):
            os.makedirs(artist_path)

        file = open(f"{self.download_path}/{song_info[0]}/{song_info[1]}.txt", "wb")
        file.write(song_text.encode('utf-8'))
        file.close()
    
    def get_songs_urls(self, artist):
        # http request to the site
        req = self.session.get(f"https://www.tekstowo.pl/piosenki_artysty,{artist}.html")

        # parsed html
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        num_sites = 0
        urls = []

        for item in soup.find_all("a", {"class": "page-link"}):
            if " " not in item.text:
                num_sites += 1
        num_sites = int(num_sites / 2) 

        for num in range(1, num_sites + 1):
            songs = self.session.get(f"https://www.tekstowo.pl/piosenki_artysty,{artist},alfabetycznie,strona,{num}.html")
            songs_soup = bs4.BeautifulSoup(songs.text, "html.parser")
            urls = urls + [a['href'] for a in songs_soup.find_all('a', {"class": "title"}, href=True) if a.text and a.get("title") and a['href'].startswith("/piosenka")]

        return urls

if __name__ == "__main__":
    scrapper = LyricScrapper()
    for artist in [
        "taco_hemingway",
        "kali",
        "schafter",
        "bialas",
        "pezet",
        "solar",
        "adi_nowak",
        "adi_nowak__barvinsky",
        "bialas__lanek_",
        "mata",
        "quebonafide",
        "moli",
        "szpaku",
        "rolex",
        "kacperczyk",
        "otsochodzi",
        "oki",
        "taconafide",
        "pro8l3m",
        "bedoes",
        "kubi_producent_",
        "szpaku__kubi_producent",
        "mrozu",
        "mlodyskiny",
        "piotr_cartman",
        "jan_rapowanie__nocny",
        "jan_rapowanie",
        "oki",
        "gedz",
        "sb_maffija",
        "chillwagon",
        "borixon",
        "reto_borixon",
        "reto",
        "kizo",
        "zabson",
        "white_2115",
        "malik_montana",
        "peja",
        "o_s_t_r_",
        "sokol",
        "Lona",
        "lona_i_webber",
        "paluch",
        "chada",
        "popek",
        "donguralesko",
        "sarius",
        "fisz",
        "fisz_emade",
        "bonus_rpk"
        ]:
            urls = scrapper.get_songs_urls(artist)
            for url in urls:
                print(f"Downloading {url}")
                scrapper.download_lyric("https://www.tekstowo.pl" + url)
    
