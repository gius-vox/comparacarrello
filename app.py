import streamlit as st
import pandas as pd
import numpy as np
import os
import urllib.parse

st.set_page_config(
    page_title="ComparaCarrello.it - Il tuo risparmio in farmacia",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed" # Mantiene la barra compressa di default
)

# Style CSS Avanzato con Full Width & Layout Mobile Smart
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1a252f;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1rem;
        color: #5a6578;
        text-align: center;
        margin-bottom: 15px;
    }

    /* Badges Farmacie Monitorate in Header */
    .pharmacy-badge-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-bottom: 25px;
    }
    .pharm-pill {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        color: #475569;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Cards Classifica */
    .pharmacy-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 2px solid #edf2f7;
        margin-bottom: 15px;
    }
    .pharmacy-card.winner {
        border: 2.5px solid #2ecc71;
        background: linear-gradient(180deg, #ffffff 0%, #f0fff4 100%);
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.15);
    }
    .badge-rank {
        display: inline-block;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 4px 10px;
        border-radius: 20px;
        margin-bottom: 8px;
    }
    .badge-rank.gold { background-color: #fef9e7; color: #d4ac0d; border: 1px solid #f9e79f; }
    .badge-rank.silver { background-color: #f2f4f4; color: #7f8c8d; border: 1px solid #d5dbdb; }
    .badge-rank.bronze { background-color: #fbeee6; color: #dc7633; border: 1px solid #edbb99; }
    .badge-rank.standard { background-color: #ebedef; color: #5d6d7e; }

    .pharm-name { font-size: 1.2rem; font-weight: 700; color: #2c3e50; margin: 4px 0; }
    .pharm-price { font-size: 1.7rem; font-weight: 800; color: #2e7d32; }
    
    .ship-free { color: #16a34a; font-weight: 700; font-size: 0.85rem; margin-top: 5px; }
    .ship-pay { color: #dc2626; font-size: 0.85rem; margin-top: 5px; }
    .ship-missing { color: #d97706; font-weight: 600; font-size: 0.8rem; }

    /* Metrics Box Top */
    .metric-box {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }
    .metric-title { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .metric-val { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-top: 4px; }
    .metric-val.green { color: #16a34a; }
    .metric-val.orange { color: #ea580c; }

    .prod-item-row {
        background: #ffffff;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    
    .btn-buy {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #2563eb;
        color: white !important;
        font-weight: 700;
        padding: 10px 12px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
        font-size: 0.9rem;
    }

    @media (max-width: 768px) {
        .main-title { font-size: 1.7rem; }
        .pharmacy-card { padding: 12px; }
    }
    </style>
""", unsafe_allow_html=True)

CLEAN_PHARMACY_NAMES = {
    'Farmacia Igea': 'Farmacia Igea', 'FarmaciaIgea': 'Farmacia Igea', 'igea': 'Farmacia Igea',
    'Farmae': 'Farmaè', 'Farmaè': 'Farmaè', 'farmae': 'Farmaè',
    'Dr Max': 'Dr. Max', 'DrMax': 'Dr. Max', 'Dott. Max': 'Dr. Max', 'Dottor Max': 'Dr. Max', 'drmax': 'Dr. Max',
    'RedCare': 'RedCare', 'redcare': 'RedCare',
    'Farmacia Loreto': 'Farmacia Loreto', 'loreto': 'Farmacia Loreto',
    '1000Farmacie': '1000Farmacie', '1000farmacie': '1000Farmacie',
    'Top Farmacia': 'Top Farmacia', 'TopFarmacia': 'Top Farmacia', 'topfarmacia': 'Top Farmacia',
    'Farmacia di alto livello': 'Top Farmacia', 'Ristoranti di alto livello': 'Top Farmacia',
    'eFarma': 'eFarma', 'efarma': 'eFarma'
}

SHIPPING_RULES = {
    'Farmacia Igea': {'free_threshold': 29.90, 'cost': 4.50},
    'Farmaè': {'free_threshold': 19.90, 'cost': 3.90},
    'Dr. Max': {'free_threshold': 19.90, 'cost': 3.90},
    'RedCare': {'free_threshold': 18.00, 'cost': 3.99},
    'Farmacia Loreto': {'free_threshold': 29.90, 'cost': 4.90},
    '1000Farmacie': {'free_threshold': 29.00, 'cost': 4.20},
    'Top Farmacia': {'free_threshold': 29.90, 'cost': 4.50},
    'eFarma': {'free_threshold': 19.90, 'cost': 3.90}
}

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv("prodotti.csv", dtype={'MINSAN': str})
        new_cols = [CLEAN_PHARMACY_NAMES.get(col.strip(), col.strip()) for col in df.columns]
        df.columns = new_cols

        fixed_cols = ['MINSAN', 'Prodotto', 'Categoria', 'Immagine']
        pharmacy_cols = [c for c in df.columns if c not in fixed_cols]
        df['MINSAN'] = df['MINSAN'].astype(str).str.zfill(9)
        return df, pharmacy_cols
    except Exception as e:
        st.error(f"Errore nel caricamento: {e}")
        return pd.DataFrame(), []

df_prodotti, farmacie_disponibili = load_data()

st.markdown("<h1 class='main-title'>💊 ComparaCarrello.it</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Trova la farmacia online più conveniente per il tuo carrello</p>", unsafe_allow_html=True)

# Farmacie Monitorate in formato Badge Orizzontali
if farmacie_disponibili:
    badges_html = "".join([f'<span class="pharm-pill">🏥 {f}</span>' for f in farmacie_disponibili])
    st.markdown(f'<div class="pharmacy-badge-container">{badges_html}</div>', unsafe_allow_html=True)

if df_prodotti.empty:
    st.warning("Database in caricamento...")
    st.stop()

# Filtro per categoria posizionato al centro in alto
categorie = ["Tutte le Categorie"] + sorted([str(c) for c in df_prodotti['Categoria'].dropna().unique() if str(c).strip() != ""])
c_cat1, c_cat2, c_cat3 = st.columns([1, 2, 1])
with c_cat2:
    cat_selezionata = st.selectbox("📁 Filtra per Categoria:", categorie)

df_filtrato = df_prodotti if cat_selezionata == "Tutte le Categorie" else df_prodotti[df_prodotti['Categoria'] == cat_selezionata]

if 'cart_indices' not in st.session_state:
    st.session_state.cart_indices = []

st.markdown("---")
st.subheader("🔍 Cerca e Aggiungi Prodotti")

def format_prod(idx):
    row = df_filtrato.loc[idx]
    return f"{row['Prodotto']} — [MINSAN: {row['MINSAN']}]"

selected_to_add = st.selectbox("Seleziona o digita un prodotto:", options=[None] + df_filtrato.index.tolist(), format_func=lambda x: "— Seleziona un prodotto —" if x is None else format_prod(x))

col_b1, col_b2 = st.columns([1.5, 3.5])
with col_b1:
    if st.button("➕ Aggiungi al Carrello", type="primary", use_container_width=True):
        if selected_to_add is not None and selected_to_add not in st.session_state.cart_indices:
            st.session_state.cart_indices.append(selected_to_add)
            st.rerun()

with col_b2:
    if st.session_state.cart_indices and st.button("🗑️ Svuota Carrello"):
        st.session_state.cart_indices = []
        st.rerun()

if st.session_state.cart_indices:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛒 Prodotti nel Carrello")
    df_carrello = df_prodotti.loc[st.session_state.cart_indices].copy()
    
    for idx, row in df_carrello.iterrows():
        c_p1, c_p2 = st.columns([4, 1.5])
        with c_p1:
            st.markdown(f"""
                <div class="prod-item-row">
                    <span style="font-weight:600;">{row['Prodotto']}</span>
                    <span style="font-size:0.8rem; color:#2563eb; margin-left:8px;">MINSAN: {row['MINSAN']}</span>
                </div>
            """, unsafe_allow_html=True)
        with c_p2:
            if st.button("❌ Rimuovi", key=f"rem_{idx}", use_container_width=True):
                st.session_state.cart_indices.remove(idx)
                st.rerun()

    st.markdown("---")
    st.subheader("📊 Classifica Risparmio Carrello Completo")

    totali_prodotti = {}
    totali_finali = {}
    spese_spedizione = {}
    mancanti_spedizione = {}

    for f in farmacie_disponibili:
        prezzi = pd.to_numeric(df_carrello[f], errors='coerce')
        if prezzi.notna().all():
            sum_prod = prezzi.sum()
            totali_prodotti[f] = sum_prod
            
            rules = SHIPPING_RULES.get(f, {'free_threshold': 29.90, 'cost': 4.50})
            thresh = rules['free_threshold']
            
            if sum_prod >= thresh:
                ship_cost = 0.0
                missing = 0.0
            else:
                ship_cost = rules['cost']
                missing = thresh - sum_prod
                
            spese_spedizione[f] = ship_cost
            mancanti_spedizione[f] = missing
            totali_finali[f] = sum_prod + ship_cost

    if totali_finali:
        sorted_pharmacies = sorted(totali_finali.items(), key=lambda x: x[1])
        miglior_farmacia, miglior_prezzo = sorted_pharmacies[0]
        peggior_prezzo = sorted_pharmacies[-1][1]
        risparmio_max = peggior_prezzo - miglior_prezzo

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-box"><div class="metric-title">🥇 Più Conveniente</div><div class="metric-val green">{miglior_farmacia}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><div class="metric-title">💰 Totale (Sped. Inclusa)</div><div class="metric-val">{miglior_prezzo:.2f} €</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><div class="metric-title">🔥 Risparmio Massimo</div><div class="metric-val orange">{risparmio_max:.2f} €</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🏆 Classifica Farmacie")

        cols_cards = st.columns(min(3, len(sorted_pharmacies)))
        
        for i, (pharm_name, tot_val) in enumerate(sorted_pharmacies):
            prod_val = totali_prodotti[pharm_name]
            ship_val = spese_spedizione[pharm_name]
            miss_val = mancanti_spedizione[pharm_name]
            
            card_class = "pharmacy-card winner" if i == 0 else "pharmacy-card"
            
            if i == 0:
                badge_html = '<span class="badge-rank gold">🥇 1° Posto</span>'
            elif i == 1:
                badge_html = '<span class="badge-rank silver">🥈 2° Posto</span>'
            elif i == 2:
                badge_html = '<span class="badge-rank bronze">🥉 3° Posto</span>'
            else:
                badge_html = f'<span class="badge-rank standard">{i+1}° Posto</span>'
                
            if ship_val == 0:
                ship_html = '<div class="ship-free">🚚 Spedizione Gratuita</div>'
            else:
                ship_html = f'<div class="ship-pay">🚚 Spedizione: +{ship_val:.2f} €</div><div class="ship-missing">(mancano {miss_val:.2f} € per la gratuita)</div>'

            col_idx = i % 3
            with cols_cards[col_idx]:
                st.markdown(f"""
                    <div class="{card_class}">
                        {badge_html}
                        <div class="pharm-name">{pharm_name}</div>
                        <div class="pharm-price">{tot_val:.2f} €</div>
                        <div style="font-size:0.85rem; color:#64748b;">Prodotti: {prod_val:.2f} €</div>
                        {ship_html}
                        <a href="https://www.google.com/search?q={urllib.parse.quote(pharm_name)}+farmacia+online" target="_blank" class="btn-buy">🛒 Vai alla Farmacia</a>
                    </div>
                """, unsafe_allow_html=True)

        with st.expander("🔍 Mostra Matrice Dettagliata Prezzi Singoli"):
            st.dataframe(df_carrello[['Prodotto', 'MINSAN'] + farmacie_disponibili], use_container_width=True, hide_index=True)
    else:
        st.warning("I prodotti selezionati non sono presenti contemporaneamente in tutte le farmacie.")
else:
    st.info("💡 Usa la barra di ricerca qui sopra e clicca su **'➕ Aggiungi al Carrello'** per iniziare!")
