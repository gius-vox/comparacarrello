import pandas as pd

def clean_and_validate_csv(file_path="prodotti.csv"):
    print("🔍 Avvio controllo e pulizia del file CSV...")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Errore nella lettura del file: {e}")
        return

    farmacie = ["Farmacia Igea", "Farmacia Loreto", "Farmacie Raven", "Dr. Max"]

    # Rimozione spazi extra
    df.columns = df.columns.str.strip()

    # Pulizia nomi prodotti e categorie
    df["Prodotto"] = df["Prodotto"].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
    if "Categoria" in df.columns:
        df["Categoria"] = df["Categoria"].astype(str).str.strip().str.title()
    else:
        df["Categoria"] = "Farmaci E Integratori"

    # Conversione prezzi
    for col in farmacie:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').str.replace('€', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    df_clean = df.drop_duplicates(subset=["Prodotto"])
    df_clean.to_csv("prodotti.csv", index=False)
    print("✅ File prodotti.csv verificato e ripulito con successo!")

if __name__ == "__main__":
    clean_and_validate_csv()
