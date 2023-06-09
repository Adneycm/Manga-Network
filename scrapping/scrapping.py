import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# df = pd.read_csv("data_5k.csv")
# mangas = df.manga_name.to_list()

df_faltantes = pd.read_csv("mangas_faltantes.csv")
mangas = df_faltantes["Book Title"].to_list()

lixo = ['(', ')', '!', '￣', '∇', 'ゞ', ',', '?', ':', "'"]

def remove_characters(string):
    characters_to_remove = "(!￣∇ゞ,?:')’.;\/$%¨@*"
    translation_table = str.maketrans("", "", characters_to_remove)
    cleaned_string = string.translate(translation_table)
    return cleaned_string

def remove_duplicate_hyphens(string):
    # Use regex to remove consecutive duplicate hyphens
    modified_string = re.sub(r'-{2,}', '-', string)
    return modified_string

def convert_to_lowercase(string):
    return string.lower()

manga_popular = {}
cont = 0

for manga in mangas:
    try:
        manga_real_name = manga
        manga = remove_characters(manga)
        manga = convert_to_lowercase(manga)
        manga = manga.replace(' ', '-')
        manga = manga.replace('&', 'and')
        manga = manga.replace('"', '')
        manga = remove_duplicate_hyphens(manga)
        print(manga_real_name, manga)

        url = f'https://www.anime-planet.com/manga/{manga}'
        print(url)
        req = requests.get(url)
        
        html_content = req.text
        info_bs = BeautifulSoup(html_content, 'html.parser')
        number_avaliation = info_bs.find('div', attrs={'class': 'avgRating'}).text

        time.sleep(3)

        manga_popular[manga_real_name] = number_avaliation
    except:
        print(f"[ERROR] MANGA = {manga_real_name}")
        manga_popular[manga_real_name] = "-"

print(manga_popular)
df_popular = pd.DataFrame(list(manga_popular.items()), columns=['Book Title', 'Value'])
df_popular.to_csv("popular_faltantes.csv", index=False)