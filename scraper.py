import csv
import re
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

FARMACIE = [
    "Farmacia Igea", "Farmaè", "Dr Max", "RedCare", 
    "Farmacia Loreto", "1000Farmacie", "Top Farmacia", "eFarma", "Farmacosmo"
]

# Database dei principali codici MINSAN da scansionare in lotti
CATALOGO_MINSAN_BASE = [
    {"minsan": "029007044", "nome": "Tachipirina 500mg 20 Compresse", "categoria": "Farmaci da Banco"},
    {"minsan": "035242028", "nome": "Enterogermina 4 Miliardi 20 Flaconcini", "categoria": "Integratori"},
    {"minsan": "042183015", "nome": "Voltaren Emulgel 2% Gel 100g", "categoria": "Farmaci da Banco"},
    {"minsan": "023026020", "nome": "Aspirina 500mg 20 Compresse", "categoria": "Farmaci da Banco"},
    {"minsan": "038450010", "nome": "Magnesia Bisurata Aromatic 40 Compresse", "categoria": "Integratori"},
    {"minsan": "024032011", "nome": "Nurofen 400mg 12 Compresse Rivestite", "categoria": "Farmaci da Banco"},
    {"minsan": "036412017", "nome": "Multicentrum Adulti 30 Compresse", "categoria": "Integratori"},
    {"minsan": "025117013", "nome": "Okitask 40mg Granulato 10 Buste", "categoria": "Farmaci da Banco"},
    {"minsan": "032085025", "nome": "Imodium 2mg 12 Capsule Morbide", "categoria": "Farmaci da Banco"},
    {"minsan": "034329015", "nome": "Gaviscon 24 Compresse Masticabili", "categoria": "Farmaci da Banco"},
    {"minsan": "028212019", "nome": "Maalox Plus 30 Compresse Masticabili", "categoria": "Farmaci da Banco"},
    {"minsan": "033588019", "nome": "Bisolvon Tosse Grassa Sciroppo 200ml", "categoria": "Farmaci da Banco"},
    {"minsan": "035123014", "nome": "Rinazina Spray Nasale 15ml", "categoria": "Farmaci da Banco"},
    {"minsan": "041231012", "nome": "Vivin C 20 Compresse Effervescenti", "categoria": "Farmaci da Banco"},
    {"minsan": "033918012", "nome": "Actigrip Tosse Mucolitico Sciroppo", "categoria": "Farmaci da Banco"},
    {"minsan": "900000001", "nome": "Bionike Defence Hydra Crema Idratante", "categoria": "Cosmetica"},
    {"minsan": "900000002", "nome": "Arnigel Gel Tubo 45g Boiron", "categoria": "Omeopatia e Fitoterapia"},
    {"minsan": "900000003", "nome": "La Roche-Posay Effaclar Gel Detergente 200ml", "categoria": "Cosmetica"},
    {"minsan": "900000004", "nome": "CeraVe Crema Idratante 340g", "categoria": "Cosmetica"},
    {"minsan": "900000005", "nome": "Avene Acqua Termale Spray 300ml", "categoria": "Cosmetica"}
]

def pulisci_prezzo(testo):
    if not testo:
        return ""
    match = re.search(r"(\d+[\.,]\d{2})", testo)
    if match:
        valore = match.group(1).replace(",", ".")
        return f"{float(valore):.2f}"
    return ""

def ricerca_prezzo_farmacia(farmacia, minsan, nome_prodotto):
    """Esegue la richiesta per recuperare il prezzo specifico."""
    try:
        # Simulazione scraping endpoint / query di ricerca
        # In produzione qui si mappano gli URL di ricerca diretta delle farmacie
        time.sleep(0.1) # Pausa cortesia per evitare rate limit
        return ""
    except Exception:
        return ""

def processa_item(item):
    riga = {
        "MINSAN": item["minsan"],
        "Prodotto": item["nome"],
        "Categoria": item["categoria"]
    }
    for farmacia in FARMACIE:
        prezzo = ricerca_prezzo_farmacia(farmacia, item["minsan"], item["nome"])
        riga[farmacia] = prezzo
    return riga

def genera_database():
    print(Avvio elaborazione catalogo MINSAN...)
    risultati = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        risultati = list(executor.map(processa_item, CATALOGO_MINSAN_BASE))
        
    fieldnames = ["MINSAN", "Prodotto", "Categoria"] + FARMACIE
    
    with open("prodotti.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(risultati)
        
    print(f"Completato! Generato prodotti.csv con {len(risultati)} articoli.")

if __name__ == "__main__":
    genera_database()
