import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_text_str(val):
    if not isinstance(val, str):
        return val
    cleaned = re.sub(r'[\u4e00-\u9fff]+', '', val)
    return re.sub(r'\s+', ' ', cleaned).strip()

def get_price_igea(query):
    try:
        url = f"https://farmaciaigea.com/ricerca?controller=search&s={requests.utils.quote(query)}"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            price_elem = soup.find('span', class_='price')
            if price_elem:
                price_str = re.sub(r'[^\d,]', '', price_elem.text.strip()).replace(',', '.')
                return float(price_str)
    except Exception as e:
        print(f"Errore Igea per {query}: {e}")
    return None

def update_prices():
    try:
        df = pd.read_csv("prodotti.csv")
    except Exception as e:
        print("Impossibile leggere prodotti.csv:", e)
        return

    df["Prodotto"] = df["Prodotto"].astype(str).apply(clean_text_str)

    print("Inizio aggiornamento prezzi...")
    for idx, row in df.iterrows():
        prod_name = row["Prodotto"]
        print(f"Aggiornamento: {prod_name}")
        
        # Esempio scraping Farmacia Igea (estendibile alle altre)
        p_igea = get_price_igea(prod_name)
        if p_igea:
            df.at[idx, "Farmacia Igea"] = p_igea
            
        time.sleep(1) # pausa di sicurezza per rispetto del server

    df.to_csv("prodotti.csv", index=False)
    print("Aggiornamento completato con successo!")

if __name__ == "__main__":
    update_prices()
