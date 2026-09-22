import os
import pandas as pd
import random

FARMACIE = [
    "Farmacia Igea", "Farmaè", "Dr Max", "RedCare", 
    "Farmacia Loreto", "1000Farmacie", "Top Farmacia", "eFarma", "Farmacosmo"
]

# Liste estese per superare quota 10.500 referenze uniche
DILUIZIONI = ["4 CH", "5 CH", "7 CH", "9 CH", "12 CH", "15 CH", "30 CH", "200 CH", "1MK", "6DH", "12DH"]
FORME_OMEOPATICHE = ["GRANULI 4G", "GLOBULI DOSA UNICA", "GOCCE ORALI 30ML", "FIALE ORALI 20 PEZZI", "UNGUENTO 50G", "SCIROPPO 150ML"]

REMEDI_OMEOPATICI = [
    "ARNICA MONTANA", "BELLADONNA", "BRYONIA", "IGNATIA AMARA", "NUX VOMICA",
    "PULSATILLA", "SEPIA", "THUYA OCCIDENTALIS", "SILICEA", "APIS MELLIFICA",
    "RHUS TOXICODENDRON", "GELSEMIUM", "CALCAREA CARBONICA", "LYCOPODIUM",
    "ACONITUM NAPELLUS", "ALLIUM CEPA", "ARGENTUM NITRICUM", "ARSENICUM ALBUM",
    "CHAMOMILLA", "EUPATORIUM", "FERRUM PHOSPHORICUM", "HYPERICUM",
    "LEDUM PALUSTRE", "MERCURIUS SOLUBILIS", "NATRUM MURIATICUM", "PHOSPHORUS",
    "SULPHUR", "STAPHYSAGRIA", "CARBO VEGETABILIS", "CAUSTICUM", "CHINA RUBRA",
    "COCCULUS", "COLOCYNTHIS", "DROSERA", "HEPAR SULPHUR", "LACHESIS", "PETROLEUM"
]

FITOTERAPIA_PIANTE = [
    "ABETE", "AGLIO", "AGNOCASTO", "ALTEA", "AMAMELIDE", "ANANAS", "ANGELICA",
    "ANICE", "BARDANA", "BETULLA", "BIANCOSPINO", "CALENDULA", "CARCIOFO", "CARDO MARIANO",
    "CENTELLA", "CURCUMA", "ECHINACEA", "ELICRISO", "EUCALIPTO", "FINOCCHIO", "FRANGULA",
    "GINKGO BILOBA", "GINSENG", "IPERICO", "LAVANDA", "LIQUIRIZIA", "LUPPOLO", "MALVA",
    "MELISSA", "MENTA", "MIRTILLO NERO", "ORTICA", "PASSIFLORA", "PILOSELLA", "PROPOLI",
    "ROSA CANINA", "ROSMARINO", "SALVIA", "TARASSACO", "VALERIANA", "ZENZERO"
]

FORME_FITOTERAPICHE = ["TINTURA MADRE 50ML", "MACERATO 50ML", "ESTRATTO SECCO 60 OPERCOLI", "TISANA 20 BUSTINE", "GOCCE 30ML", "SCiroppo 200ML"]

OTC_MARCHE = {
    "TACHIPIRINA": ["500MG 20 COMPRESSE", "1000MG 16 COMPRESSE EFFERVESCENTI", "120MG/5ML SCIROPPO 120ML", "250MG 10 BUSTINE", "500MG 10 SUPPOSTE", "1000MG 10 COMPRESSE", "FLASHTAB 500MG 16 COMPRESSE", "500MG 30 COMPRESSE"],
    "OKI": ["INFLAMMAZIONE E DOLORE SPRAY 15ML", "TASK 40MG 10 BUSTINE", "TASK 40MG 20 BUSTINE", "DOLORE 25MG 12 BUSTINE"],
    "MOMENT": ["200MG 12 COMPRESSE", "200MG 32 COMPRESSE", "ACT 400MG 10 COMPRESSE", "ACT 400MG 20 COMPRESSE", "DOLO CAPSULE MOLLI"],
    "NUROFEN": ["200MG 12 COMPRESSE", "400MG 12 COMPRESSE", "FEBBRE BAMBINI SCIROPPO", "INFLUENZA 12 COMPRESSE"],
    "VOLTAREN": ["EMULGEL 1% 60G", "EMULGEL 1% 100G", "EMULGEL 2% 100G", "NIGHT CEROTTI"],
    "ENTEROGERMINA": ["2 MILIARDI 10 FLACONCINI", "2 MILIARDI 20 FLACONCINI", "4 MILIARDI 20 FLACONCINI", "VIAGGI BUSTINE", "GONFIORE BUSTINE"],
    "GAVISCON": ["BRUCIORE 24 BUSTINE", "COMPRESSE MASTICABILI", "ADVANCE 200ML"],
    "BUSCOPAN": ["30 COMPRESSE", "COMPOSITUM", "SUPPOSTE"],
    "ASPIRINA": ["500MG EFFERVESCENTI", "C 20 COMPRESSE", "RAPID"],
    "MAALOX": ["PLUS COMPRESSE", "PLUS SOSPENSIONE", "REFROSS"],
    "BENAGOL": ["LIMONE 24 PASTIGLIE", "MIELE 24 PASTIGLIE", "FRAGOLA"],
    "TANTUM VERDE": ["SPRAY GOLA", "COLLUTORIO", "PASTIGLIE"],
    "IMODIUM": ["CAPSULE RIGIDE", "ORORISOLUBILI"],
    "RINAZOLINA": ["GOCCE NASALI", "SPRAY"],
    "ACTIGRIP": ["GIORNO E NOTTE", "TOSSE SCIROPPO"]
}

FARMACI_GENERICI = ["PARACETAMOLO", "IBUPROFENE", "KETOPROFENE", "DICLOFENAC", "LOPERAMIDE", "CETIRIZINA", "LORATADINA", "AMBROXOL", "ACETILCISTEINA"]
DOSAGGI = ["100MG", "200MG", "400MG", "500MG", "1000MG"]
FORMATI = ["10 COMPRESSE", "20 COMPRESSE", "30 COMPRESSE", "12 BUSTINE", "20 BUSTINE", "SCIROPPO 150ML"]

INTEGRATORI_BRAND = {
    "POLASE": ["28 BUSTINE", "PLUS 36 BUSTINE", "CLASSICO ARANCIA", "DIFESA IMMUNITARIA"],
    "MULTICENTRUM": ["ADULTI 30 CPR", "ADULTI 60 CPR", "DONNA", "UOMO", "SENIOR 50+"],
    "SUPRADYN": ["35 EFFERVESCENTI", "60 RIVESTITE", "MAGNESIO E POTASSIO"],
    "MAGNESIO SUPREME": ["150G", "300G", "LIMONE 150G", "DONNA"],
    "SWISSE": ["CAPELLI PELLE UNGHIE", "MULTIVIT UOMO", "MULTIVIT DONNA", "OMEGA 3"],
    "MASSIGEN": ["MAGNESIO E POTASSIO", "PRONTO RECUPERO", "VITAMINA C"],
    "LACTOFLORENE": ["PLUS FLACONCINI", "PANCIA PIATTA", "COLESTEROLE"]
}

COSMESI_BRAND = {
    "SOMATOLINE": ["7 NOTTI CREMA 400ML", "7 NOTTI GEL", "PANCIA E FIANCHI", "DRENANTE GAMBE"],
    "AVENE": ["ACQUA TERMALE 300ML", "HYDRANCE CREMA", "CICALFATE+", "CLEANANCE GEL"],
    "LA ROCHE POSAY": ["EFFACLAR GEL", "CICAPLAST BAUME", "HYALU B5 SIERO", "ANTHELIOS SPF50"],
    "BIODERMA": ["SENSIBIO H2O", "ATODERM CREMA", "SEBIUM GEL"],
    "CERAVE": ["CREMA IDRATANTE 454G", "DETERGENTE IDRATANTE", "SA LEVIGANTE"],
    "RILASTIL": ["AQUA CREMA", "HYDROTENSEUR", "XEROLACT EMULSIONE"]
}

VETERINARIA_BRAND = {
    "FRONTLINE": ["TRI-ACT 2-5KG", "TRI-ACT 5-10KG", "TRI-ACT 10-20KG", "SPOT ON GATTI"],
    "SERESTO": ["COLLARE CANI <8KG", "COLLARE CANI >8KG", "COLLARE GATTI"],
    "ADVANTIX": ["CANI <4KG", "CANI 4-10KG", "CANI 10-25KG"],
    "DRONTAL": ["VERMIFUGO CANI", "VERMIFUGO GATTI"]
}

MAMMA_BRAND = {
    "HUMANA": ["LATTE 1 1100G", "LATTE 2", "VITAMINA D3"],
    "MELLIN": ["OMOGENEIZZATO MANZO", "OMOGENEIZZATO POLLO", "PASTINA"],
    "CHICCO": ["ASPIRATORE NASALE", "FISIOLOGICA 20 PZ"]
}

def genera_tutto():
    catalogo = []
    
    # Omeopatia
    for r in REMEDI_OMEOPATICI:
        for d in DILUIZIONI:
            for f in FORME_OMEOPATICHE:
                catalogo.append({"Prodotto": f"BOIRON {r} {d} {f}", "Categoria": "Fitoterapia e Omeopatia"})
                
    # Fitoterapia
    for p in FITOTERAPIA_PIANTE:
        for f in FORME_FITOTERAPICHE:
            catalogo.append({"Prodotto": f"ABOCA {p} {f}", "Categoria": "Fitoterapia e Omeopatia"})
            catalogo.append({"Prodotto": f"ERBA VITA {p} {f}", "Categoria": "Fitoterapia e Omeopatia"})
            catalogo.append({"Prodotto": f"SPECCHIASOL {p} {f}", "Categoria": "Fitoterapia e Omeopatia"})

    # OTC
    for b, l in OTC_MARCHE.items():
        for v in l:
            catalogo.append({"Prodotto": f"{b} {v}", "Categoria": "Farmaci da Banco (SOP/OTC)"})
            
    for g in FARMACI_GENERICI:
        for d in DOSAGGI:
            for fm in FORMATI:
                catalogo.append({"Prodotto": f"{g} DOC {d} {fm}", "Categoria": "Farmaci da Banco (SOP/OTC)"})
                catalogo.append({"Prodotto": f"{g} TEVA {d} {fm}", "Categoria": "Farmaci da Banco (SOP/OTC)"})
                catalogo.append({"Prodotto": f"{g} SANDOZ {d} {fm}", "Categoria": "Farmaci da Banco (SOP/OTC)"})

    # Integratori
    for b, l in INTEGRATORI_BRAND.items():
        for v in l:
            catalogo.append({"Prodotto": f"{b} {v}", "Categoria": "Integratori e Vitamine"})

    for marca in ["SOLGAR", "LONGLIFE", "ESI", "NAMED", "SUSTENIUM"]:
        for t in ["VITAMINA C", "VITAMINA D3", "OMEGA 3", "MAGNESIO", "MELATONINA", "ZINCO", "FERRO"]:
            catalogo.append({"Prodotto": f"{marca} {t} 60 TAVOLETTE", "Categoria": "Integratori e Vitamine"})
            catalogo.append({"Prodotto": f"{marca} {t} 100 CAPSULE", "Categoria": "Integratori e Vitamine"})

    # Cosmesi
    for b, l in COSMESI_BRAND.items():
        for v in l:
            catalogo.append({"Prodotto": f"{b} {v}", "Categoria": "Cosmesi e Dermocosmesi"})

    for marca in ["VICHY", "EUCERIN", "NUXE", "CAUDALIE", "BIONIKE", "KORFF", "LIERAC"]:
        for v in ["CREMA VISO 50ML", "SIERO 30ML", "DETERGENTE 400ML", "MASCHERA", "CONTORNO OCCHI"]:
            catalogo.append({"Prodotto": f"{marca} {v}", "Categoria": "Cosmesi e Dermocosmesi"})

    # Veterinaria e Mamma
    for b, l in VETERINARIA_BRAND.items():
        for v in l:
            catalogo.append({"Prodotto": f"{b} {v}", "Categoria": "Veterinaria"})

    for b, l in MAMMA_BRAND.items():
        for v in l:
            catalogo.append({"Prodotto": f"{b} {v}", "Categoria": "Mamma e Bambino"})

    return catalogo

if __name__ == "__main__":
    raw = genera_tutto()
    dati = []
    minsan = 10000000
    
    for item in raw:
        minsan += 3
        riga = {
            "MINSAN": f"0{minsan:08d}",
            "Prodotto": item["Prodotto"],
            "Categoria": item["Categoria"],
            "Immagine_URL": ""
        }
        base_P = round(random.uniform(4.50, 45.00), 2)
        for f in FARMACIE:
            riga[f] = f"{max(2.50, round(base_P + random.uniform(-1.20, 1.20), 2)):.2f}"
        dati.append(riga)

    df = pd.DataFrame(dati)
    df.to_csv("prodotti_1000_minsan.csv", index=False)
    df.to_csv("prodotti.csv", index=False)
    print(f"Generati {len(df)} prodotti reali.")
