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

def search_price_by_minsan(minsan, query_fallback, pharmacy_type):
    search_term = str(minsan).zfill(9) if pd.notna(minsan) and str(minsan).isdigit() else query_fallback
    try:
        if pharmacy_type == 'igea':
            url = f"https://farmaciaigea.com/ricerca?controller=search&s={requests.utils.quote(search_term)}"
        elif pharmacy_type == 'farmae':
            url = f"https://www.farmae.it/catalogsearch/result/?q={requests.utils.quote(search_term)}"
        elif pharmacy_type == 'drmax':
            url = f"https://www.drmax.it/catalogsearch/result/?q={requests.utils.quote(search_term)}"
        elif pharmacy_type == 'redcare':
            url = f"https://www.redcare.it/search.htm?q={requests.utils.quote(search_term)}"
        else:
            return None

        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            price_elem = soup.find('span', class_=re.compile(r'(price|special-price|prezzo)', re.I))
            if price_elem:
                price_str = re.sub(r'[^\d,]', '', price_elem.text.strip()).replace(',', '.')
                val = float(price_str)
                return val if 0.5 < val < 500 else None
    except Exception as e:
        print(f"Errore ricerca {pharmacy_type} per {search_term}: {e}")
    return None

def update_prices():
    try:
        df = pd.read_csv("prodotti.csv", dtype={'MINSAN': str})
    except Exception as e:
        print("Impossibile leggere prodotti.csv:", e)
        return

    df["Prodotto"] = df["Prodotto"].astype(str).apply(clean_text_str)

    print("Inizio aggiornamento prezzi avanzato (Fase A)...")
    
    pharmacies = ['igea', 'farmae', 'drmax', 'redcare']
    col_mapping = {
        'igea': 'Farmacia Igea',
        'farmae': 'Farmae',
        'drmax': 'Dr Max',
        'redcare': 'RedCare'
    }

    for idx, row in df.iterrows():
        minsan = row.get("MINSAN", "")
        prod_name = row["Prodotto"]
        print(f"Processando: MINSAN {minsan} - {prod_name}")
        
        for p_key in pharmacies:
            col_name = col_mapping[p_key]
            price = search_price_by_minsan(minsan, prod_name, p_key)
            if price is not None:
                df.at[idx, col_name] = price
            time.sleep(0.5)

    df.to_csv("prodotti.csv", index=False)
    print("Aggiornamento completato con successo!")

if __name__ == "__main__":
    update_prices()
