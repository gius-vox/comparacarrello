import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Lista dei prodotti base da estrarre e monitorare (inclusi Omeopatia e Fitoterapia)
MINSAN_LIST = [
    {"MINSAN": "923849102", "Prodotto": "POLASE RICARICA INVERNO*28 BUSTINE", "Categoria": "Integratori"},
    {"MINSAN": "024097014", "Prodotto": "TACHIPIRINA*500MG 20 COMPRESSE", "Categoria": "Farmaci da Banco"},
    {"MINSAN": "038715024", "Prodotto": "OKI INFLAMMAZIONE E DOLORE*SPRAY", "Categoria": "Farmaci da Banco"},
    {"MINSAN": "800012345", "Prodotto": "OSCILLOCOCCINUM 30 DOSI", "Categoria": "Omeopatia"},
    {"MINSAN": "800012346", "Prodotto": "ARNICA MONTANA 9 CH GRANULI", "Categoria": "Omeopatia"},
    {"MINSAN": "800012347", "Prodotto": "SALI DI SCHUSSLER N. 3 FERRUM PHOSPHORICUM", "Categoria": "Sali di Schussler"},
    {"MINSAN": "800012348", "Prodotto": "TUSSISTOP SCIROPPO FITOTERAPICO", "Categoria": "Fitoterapia"}
]

FARMACIE = {
    "Farmacia Igea": "https://www.farmaciaigea.com/ricerca?search_query=",
    "Farmaè": "https://www.farmae.it/catalogsearch/result/?q=",
    "Dr Max": "https://www.drmax.it/catalogsearch/result/?q=",
    "RedCare": "https://www.redcare.it/search.htm?q=",
    "Farmacia Loreto": "https://farmacialoreto.it/catalogsearch/result/?q=",
    "1000Farmacie": "https://www.1000farmacie.it/search?q=",
    "Top Farmacia": "https://www.topfarmacia.it/catalogsearch/result/?q=",
    "eFarma": "https://www.efarma.com/catalogsearch/result/?q=",
    "Farmacosmo": "https://www.farmacosmo.it/ricerca?controller=search&s="
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def genera_catalogo():
    print("Avvio elaborazione catalogo MINSAN...")
    dati_finali = []

    for item in MINSAN_LIST:
        riga = {
            "MINSAN": item["MINSAN"],
            "Prodotto": item["Prodotto"],
            "Categoria": item["Categoria"],
            "Immagine_URL": "https://cdn-icons-png.flaticon.com/512/3028/3028549.png"
        }
        
        # Simula prelievo prezzi per la struttura
        for farmacia in FARMACIE.keys():
            riga[farmacia] = "12.50"
            
        dati_finali.append(riga)

    df = pd.DataFrame(dati_finali)
    df.to_csv("prodotti_1000_minsan.csv", index=False)
    print("Catalogo aggiornato con successo in prodotti_1000_minsan.csv")

if __name__ == "__main__":
    genera_catalogo()
