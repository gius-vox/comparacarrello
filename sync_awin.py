import os
import io
import gzip
import re
import requests
import pandas as pd
from supabase import create_client, Client

# Recupera le credenziali sicure dai Secrets
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
AWIN_FEED_URL = os.environ.get("AWIN_FEED_URL")

if not all([SUPABASE_URL, SUPABASE_KEY, AWIN_FEED_URL]):
    raise ValueError("Credenziali mancanti nei Secrets di GitHub!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def extract_aic(text):
    if not isinstance(text, str):
        return None
    # Cerca un codice ministeriale AIC a 9 o 6 cifre
    match = re.search(r'\b(0\d{8}|\d{6,9})\b', text)
    return match.group(0) if match else None

def run_sync():
    print("1. Scaricamento del feed compresso da Awin...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(AWIN_FEED_URL, headers=headers, stream=True)
    response.raise_for_status()

    print("2. Decompressione e lettura del CSV in memoria...")
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
        df = pd.read_csv(gz, sep=',', low_memory=False)

    print(f"Totale prodotti nel feed: {len(df)}")

    # Filtra e pulisci i prodotti
    batch = []
    for _, row in df.iterrows():
        p_name = str(row.get('product_name', '')).strip()
        p_id = str(row.get('merchant_product_id', '')).strip()
        desc = str(row.get('description', '')).strip()
        
        # Estrai AIC o ID prodotto
        aic = extract_aic(p_name) or extract_aic(p_id) or extract_aic(desc)
        
        try:
            price = float(str(row.get('search_price', 0)).replace(',', '.'))
        except:
            price = 0.0

        if price <= 0:
            continue

        item = {
            "aw_product_id": str(row.get('aw_product_id', '')),
            "merchant_name": str(row.get('merchant_name', 'Farmacia')).strip(),
            "product_name": p_name,
            "codice_aic": aic,
            "ean": str(row.get('merchant_product_id', ''))[:13] if not aic else None,
            "price": price,
            "delivery_cost": float(str(row.get('delivery_cost', 0)).replace(',', '.')) if pd.notnull(row.get('delivery_cost')) else 0.0,
            "deep_link": str(row.get('aw_deep_link', '')),
            "image_url": str(row.get('aw_image_url', '') or row.get('merchant_image_url', '')),
            "category": str(row.get('category_name', row.get('merchant_category', ''))),
            "in_stock": True
        }
        batch.append(item)

    print(f"3. Inserimento di {len(batch)} prodotti in Supabase...")
    # Inserisci a blocchi da 500 per massima velocità
    chunk_size = 500
    for i in range(0, len(batch), chunk_size):
        chunk = batch[i:i + chunk_size]
        supabase.table("prodotti_farmacia").upsert(chunk, on_conflict="aw_product_id").execute()
        print(f"Caricati {min(i + chunk_size, len(batch))}/{len(batch)}...")

    print("✅ Sincronizzazione completata con successo!")

if __name__ == "__main__":
    run_sync()
