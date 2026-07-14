import streamlit as st
import pandas as pd
import os

# 1. Impostazione della pagina e del Layout Premium
st.set_page_config(
    page_title="ComparaCarrello - Il tuo carrello ottimizzato",
    page_icon="🛒",
    layout="wide"
)

# Inizializzazione dello Stato della Memoria (Elimina definitivamente lo sfarfallio)
if "prodotti_scelti" not in st.session_state:
    st.session_state.prodotti_scelti = []
if "quantita" not in st.session_state:
    st.session_state.quantita = {}

# 2. Iniezione CSS Globale per Grafica Premium e Font Jakarta
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
}

.block-container {
    max-width: 85% !important;
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
}

.header-wrapper {
    text-align: center;
    width: 100%;
    margin-bottom: 30px;
}
.header-title {
    color: #0f172a; 
    font-size: 56px; 
    font-weight: 800; 
    letter-spacing: -2px; 
    margin: 18px 0 0 0;
}
.header-subtitle {
    color: #64748b; 
    font-size: 14px; 
    font-weight: 700; 
    letter-spacing: 4px; 
    text-transform: uppercase; 
}

.title-with-icon {
    color: #0f172a;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 20px;
    font-size: 18px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
}
.title-with-icon::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 24px;
    background: linear-gradient(180deg, #f97316 0%, #ea580c 100%);
    border-radius: 4px;
    margin-right: 14px;
}

.quantita-row {
    background-color: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    padding: 14px 22px;
    display: flex;
    align-items: center;
}
.quantita-nome { font-size: 15px; color: #0f172a; font-weight: 600; }

.card-farmacia-computata {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 26px 30px;
    margin-bottom: 16px;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.03);
}
.nome-farmacia { font-size: 24px; font-weight: 800; color: #0f172a; }
.prezzo-farmacia { font-size: 38px; font-weight: 800; text-align: right; }
.prezzo-vincitore { 
    color: #f97316; background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.prezzo-normale { color: #0f172a; }
.subtext-card { font-size: 15.5px; color: #475569; font-weight: 500; margin-top: 6px; }

.badge-vincitore-testo {
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white;
    font-size: 11px; font-weight: 800; text-transform: uppercase;
    padding: 6px 14px; border-radius: 10px; display: inline-block; margin-bottom: 14px;
}
.badge-mancanti-testo {
    background-color: #fef2f2; color: #ef4444; border: 1px solid #fee2e2;
    padding: 5px 12px; border-radius: 10px; font-size: 12.5px; font-weight: 700; display: inline-block; margin-top: 10px;
}
.box-suggerimento {
    background-color: #fff7ed; border: 1px dashed #f97316; padding: 16px 22px;
    font-size: 14px; color: #c2410c; border-radius: 14px; margin-bottom: 24px;
}
.box-info-custom {
    background-color: #ffffff; border: 3px dashed #cbd5e1; padding: 45px 30px;
    font-size: 16px; color: #64748b; border-radius: 24px; text-align: center; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# 3. Logo ed Header Principale (Collegato direttamente all'URL per evitare errori)
_, col_logo_centrato, _ = st.columns([5, 2, 5])
with col_logo_centrato:
    st.image("https://huggingface.co/spaces/Giusvox/comparacarrello/resolve/main/logo.png", use_container_width=True)

st.markdown("""
<div class="header-wrapper">
    <h1 class="header-title">COMPARA<span style="color: #f97316;">CARRELLO</span></h1>
    <p class="header-subtitle">L'algoritmo intelligente per la vostra spesa online</p>
</div>
""", unsafe_allow_html=True)
st.write("---")

# 4. Configurazione Regole Negozi e Caricamento CSV
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacia Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

csv_path = "prodotti.csv"
if os.path.exists(csv_path):
    df_prezzi = pd.read_csv(csv_path)
else:
    st.error("Errore: File 'prodotti.csv' non trovato nel sistema.")
    st.stop()

nomi_farmacie = [col for col in df_prezzi.columns if col in farmacie_info]
lista_prodotti = sorted(df_prezzi["Prodotto"].unique().tolist())

# 5. INPUT SELECTION (Senza Form per calcolo immediato in tempo reale senza sfarfallio)
st.markdown('<div class="title-with-icon">Cerca un prodotto o articolo di benessere</div>', unsafe_allow_html=True)
prodotti_selezionati = st.multiselect(
    "Seleziona i prodotti dal catalogo:",
    options=lista_prodotti,
    default=st.session_state.prodotti_scelti,
    label_visibility="collapsed"
)

# Sincronizza lo stato della memoria
st.session_state.prodotti_scelti = prodotti_selezionati

# 6. CONFIGURAZIONE QUANTITÀ E CALCOLO MOTORE
if st.session_state.prodotti_scelti:
    st.markdown('<div class="title-with-icon">Configurazione Quantità Carrello</div>', unsafe_allow_html=True)
    
    for prod in st.session_state.prodotti_scelti:
        valore_precedente = st.session_state.quantita.get(prod, 1)
        
        col_p, col_q = st.columns([5, 1])
        with col_p:
            st.markdown(f'<div class="quantita-row"><span class="quantita-nome">{prod}</span></div>', unsafe_allow_html=True)
        with col_q:
            nuova_q = st.number_input(
                f"Quantità per {prod}", min_value=1, max_value=20, value=valore_precedente,
                key=f"q_input_{prod}", label_visibility="collapsed"
            )
            st.session_state.quantita[prod] = nuova_q

    # --- INIZIO ELABORAZIONE MATEMATICA DEI RISULTATI ---
    st.markdown('<div class="title-with-icon">Confronto Prezzi Migliori</div>', unsafe_allow_html=True)
    
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(st.session_state.prodotti_scelti)].copy()
    df_filtrato["Quantita_Scelta"] = df_filtrato["Prodotto"].map(st.session_state.quantita)
        
    risultati_singoli = []
    n_prodotti_target = len(st.session_state.prodotti_scelti)

    for nome_farmacia in nomi_farmacie:
        regoles = farmacie_info[nome_farmacia]
        df_disponibili = df_filtrato[df_filtrato[nome_farmacia].notna() & (df_filtrato[nome_farmacia] > 0)].copy()
        n_disponibili = len(df_disponibili)
        mancanti = n_prodotti_target - n_disponibili
        
        totale_prodotti = float((df_disponibili[nome_farmacia] * df_disponibili["Quantita_Scelta"]).sum())
        costo_spedizione = 0.0 if totale_prodotti >= regoles["soglia_gratis"] else regoles["spedizione_fissa"]
        totale_complessivo = totale_prodotti + costo_spedizione
                
        info_sped = "Spedizione Gratis" if costo_spedizione == 0.0 else f"Spedizione {costo_spedizione:.2f}€"
        testo_suggerimento = f"Aggiungete {regoles['soglia_gratis'] - totale_prodotti:.2f}€ per azzerare la spedizione su questo negozio." if costo_spedizione > 0 else ""
                
        risultati_singoli.append({
            "Farmacia": nome_farmacia, 
            "Totale_Prodotti": totale_prodotti,
            "Info_Spedizione": info_sped, 
            "Suggerimento": testo_suggerimento, 
            "Prezzo_Finale": totale_complessivo,
            "Mancanti_Count": mancanti
        })
            
    df_risultati_singoli = pd.DataFrame(risultati_singoli).sort_values(by=["Mancanti_Count", "Prezzo_Finale"]).reset_index(drop=True)
    negozi_completi = df_risultati_singoli[df_risultati_singoli["Mancanti_Count"] == 0]
    miglior_negozio_singolo = negozi_completi.iloc[0]["Prezzo_Finale"] if not negozi_completi.empty else df_risultati_singoli.iloc[0]["Prezzo_Finale"]

    # --- CALCOLO EFFETTIVO DELLO SPLIT CARRELLO (ORDINE DIVISO) ---
    carrelli_split = {f: [] for f in nomi_farmacie}
    for _, row in df_filtrato.iterrows():
        prezzi_prodotto = {f: float(row[f]) for f in nomi_farmacie if f in row and pd.notna(row[f]) and float(row[f]) > 0}
        if prezzi_prodotto:
            miglior_farmacia_prodotto = min(prezzi_prodotto, key=prezzi_prodotto.get)
            carrelli_split[migial_farmacia_prodotto if 'migial_farmacia_prodotto' in locals() else miglior_farmacia_prodotto].append(row["Prodotto"])

    costo_totale_split = 0.0
    dettagli_assegnazione = {}
    prodotti_coperti_dallo_split = 0
        
    for farm, prods_in_farm in carrelli_split.items():
        if prods_in_farm:
            sotto_df = df_filtrato[df_filtrato["Prodotto"].isin(prods_in_farm)]
            prezzo_prodotti = float((sotto_df[farm] * sotto_df["Quantita_Scelta"]).sum())
            regoles = farmacie_info[farm]
            spedizione = 0.0 if prezzo_prodotti >= regoles["soglia_gratis"] else regoles["spedizione_fissa"]
            costo_totale_split += (prezzo_prodotti + spedizione)
            prodotti_coperti_dallo_split += len(prods_in_farm)
            dettagli_assegnazione[farm] = {
                "prodotti": prods_in_farm,
                "prezzo_prodotti": prezzo_prodotti,
                "spedizione": spedizione
            }

    # Rendering Box Massimo Risparmio Split (Se conveniente)
    if prodotti_coperti_dallo_split == n_prodotti_target and costo_totale_split < miglior_negozio_singolo - 0.05:
        risparmio_generato = miglior_negozio_singolo - costo_totale_split
        st.html(f"""
        <div class="card-farmacia-computata" style="border-left: 5px solid #ea580c; background: linear-gradient(90deg, #ffffff 0%, #fff7ed 100%);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span class="badge-vincitore-testo" style="background: #ea580c;">🔥 MASSIMO RISPARMIO RISCONTRATO</span>
                    <div class="nome-farmacia">Configurazione con Ordine Diviso</div>
                    <div class="subtext-card">Spezzando gli acquisti abbatti la spesa di ulteriori <b style="color:#ea580c;">{risparmio_generato:.2f} €</b> rispetto al fornitore unico.</div>
                </div>
                <div class="prezzo-farmacia" style="color: #ea580c; font-size:42px;">{costo_totale_split:.2f} €</div>
            </div>
        </div>
        """)
        with st.expander("👀 Vedi come ripartire i prodotti fra i negozi:"):
            for f_nome, dati in dettagli_assegnazione.items():
                elenco_p = ", ".join([f"**{p}**" for p in dati["prodotti"]])
                info_s = "Gratis" if dati["spedizione"] == 0.0 else f"{dati['spedizione']:.2f}€"
                st.write(f"🛒 **{f_nome}** (Sped. {info_s}): Acquista {elenco_p} &rarr; *{dati['prezzo_prodotti']:.2f}€*")

    # Rendering delle Card dei Negozi Singoli
    for idx, row in enumerate(df_risultati_singoli.itertuples()):
        is_vincitore = (idx == 0 and row.Mancanti_Count == 0)
        
        badge_top = '<div class="badge-vincitore-testo">🥇 MIGLIOR PREZZO NEGOZIO UNICO</div>' if is_vincitore else ''
        badge_mancanti = f'<div class="badge-mancanti-testo">⚠️ Assenti {row.Mancanti_Count} articoli nel loro catalogo</div>' if row.Mancanti_Count > 0 else ''
        classe_prezzo = "prezzo-vincitore" if is_vincitore else "prezzo-normale"
        bordo_colore = "#f97316" if is_vincitore else "#cbd5e1"
        
        st.html(f"""
        <div class="card-farmacia-computata" style="border-left: 5px solid {bordo_colore};">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    {badge_top}
                    <div class="nome-farmacia">{row.Farmacia}</div>
                    {badge_mancanti}
                    <div class="subtext-card">Costo Articoli: {row.Totale_Prodotti:.2f} € &nbsp;|&nbsp; {row.Info_Spedizione}</div>
                </div>
                <div class="prezzo-farmacia {classe_prezzo}">{row.Prezzo_Finale:.2f} €</div>
            </div>
        </div>
        """)
        
        if row.Suggerimento and row.Mancanti_Count == 0:
            st.html(f'<div class="box-suggerimento">💡 {row.Suggerimento}</div>')
            
else:
    # Stato Carrello Vuoto di Benvenuto
    st.markdown("""
    <div class="box-info-custom" style="margin-top:25px;">
        <span style="font-size:30px;">🛒</span><br><br>
        Il vostro carrello è vuoto.<br>
        <span style="font-size: 14px; color: #94a3b8; font-weight: 400; margin-top: 5px; display: block;">Selezionate i prodotti all'interno del configuratore in alto per avviare il confronto dei prezzi in tempo reale.</span>
    </div>
    """, unsafe_allow_html=True)
