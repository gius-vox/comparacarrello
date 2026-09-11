import csv
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Elenco dei prodotti di partenza da scansionare (MINSAN, Nome, Categoria)
LISTA_PRODOTTI = [
    {"minsan": "029007044", "nome": "Tachipirina 500mg 20 Compresse", "categoria": "Farmaci da Banco"},
    {"minsan": "035242028", "nome": "Enterogermina 4 Miliardi 20 Flaconcini", "categoria": "Integratori"},
    {"minsan": "042183015", "nome": "Voltaren Emulgel 2% Gel 100g", "categoria": "Farmaci da Banco"},
    {"minsan": "023026020", "nome": "Aspirina 500mg 20 Compresse", "categoria": "Farmaci da Banco"},
    {"minsan": "038450010", "nome": "Magnesia Bisurata Aromatic 40 Compresse", "categoria": "Integratori"},
    {"minsan": "900000001", "nome": "Bionike Defence Hydra Crema Idratante", "categoria": "Cosmetica"},
    {"minsan": "900000002", "nome": "Arnigel Gel Tubo 45g Boiron", "categoria": "Omeopatia e Fitoterapia"},
]

FARMACIE = [
    "Farmacia Igea", "Farmaè", "Dr Max", "RedCare", 
    "Farmacia Loreto", "1000Farmacie", "Top Farmacia", "eFarma", "Farmacosmo"
]

def estrai_prezzo(testo):
    """Pulisce il testo e restituisce un numero float per il prezzo."""
    if not testo:
        return ""
    m = re.search(r"(\d+[\.,]\d{2})", testo)
    if m:
        valore = m.group(1).replace(",", ".")
        return f"{float(valore):.2f}"
    return ""

def cerca_prezzo_farmacia(farmacia, minsan, nome_prodotto):
    """Funzione di ricerca dei prezzi sui vari store online."""
    try:
        # Esempio di logica di ricerca generica tramite query di ricerca
        query = minsan if minsan else nome_prodotto
        # Nota: In produzione ogni farmacia può avere il suo endpoint personalizzato
        return ""
    except Exception:
        return ""

def elabora_prodotto(item):
    riga = {
        "MINSAN": item["minsan"],
        "Prodotto": item["nome"],
        "Categoria": item["categoria"]
    }
    
    for f in FARMACIE:
        prezzo = cerca_prezzo_farmacia(f, item["minsan"], item["nome"])
        riga[f] = prezzo
        
    return riga

def main():
    print("Inizio scansione prezzi per Comparacarrello.it...")
    risultati = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        risultati = list(executor.map(elabora_prodotto, LISTA_PRODOTTI))
        
    fieldnames = ["MINSAN", "Prodotto", "Categoria"] + FARMACIE
    
    with open("prodotti.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(risultati)
        
    print("Scansione completata! File prodotti.csv generato con successo.")

if __name__ == "__main__":
    main()
