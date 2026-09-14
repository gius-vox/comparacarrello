import streamlit as st
import pandas as pd
import os
import urllib.parse

# ---------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Comparacarrello.it - Il tuo Carrello Farmacia al Miglior Prezzo",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. DESIGN SYSTEM - HEADER LUMINOSO E-COMMERCE
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }

    /* Rimuove i margini superiori di Streamlit per incollare l'header in alto */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* HEADER FULL-WIDTH CHIARO E LUMINOSO */
    .tp-header-container {
        background: #ffffff;
        margin-left: -5rem;
        margin-right: -5rem;
        padding: 20px 5rem 22px 5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-bottom: 3px solid #ea580c;
        margin-bottom: 25px;
    }

    .tp-header-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .tp-logo-box {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .tp-brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1;
    }

    .tp-brand-title span {
        color: #ea580c;
    }

    .tp-brand-tagline {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* BANNER VALUE PROPOSITION CHIARO E LEGGIBILE */
    .tp-value-banner {
        background: #fff7ed;
        border: 1px solid #ffedd5;
        border-radius: 30px;
        padding: 8px 18px;
        color: #c2410c;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* STRISCIA FARMACIE MONITORATE */
    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .pharmacy-bar-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }

    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        color: #334155;
    }
    .pharmacy-chip img {
        width: 14px;
        height: 14px;
        border-radius: 50%;
    }

    /* CARD RISULTATI PODIO */
    .result-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .result-card.first {
        border: 2px solid #ea580c;
        background: #fffbf7;
        box-shadow: 0 8px 20px rgba(234, 88, 12, 0.1);
    }
    .badge-rank {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .badge-rank.gold { background-color: #fef3c7; color: #92400e; }
    .badge-rank.silver { background-color: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background-color: #ffedd5; color: #9a3412; }

    .price-tag {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        margin: 6px 0;
    }

    .ship-badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
    }
    .ship-free { background-color: #dcfce7; color: #166534; }
    .ship-paid { background-color: #fef9c3; color: #854d0e; }

    /* STILE PULSANTI OVERRIDE */
    .stButton>button[kind="primary"] {
        background-color: #ea580c !important;
        border-color: #ea580c !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. DATI FARMACIE MONITORATE
# ---------------------------------------------------------
FARMACIE = {
    "Farmacia Igea": {"domain": "farmaciaigea.com", "spedizione_base": 4.90, "soglia_gratis": 29.00, "search_url": "https://www.farmaciaigea.com/ricerca?search_query="},
    "Farmaè": {"domain": "farmae.it", "spedizione_base": 3.90, "soglia_gratis": 19.90, "search_url": "https://www.farmae.it/catalogsearch/result/?q="},
    "Dr Max": {"domain": "drmax.it", "spedizione_base": 4.50, "soglia_gratis": 24.90, "search_url": "https://www.drmax.it/catalogsearch/result/?q="},
    "RedCare": {"domain": "redcare.it", "spedizione_base": 3.95, "soglia_gratis": 18.00, "search_url": "https://www.redcare.it/search.htm?q="},
    "Farmacia Loreto": {"domain": "farmacialoreto.it", "spedizione_base": 4.90, "soglia_gratis": 29.90, "search_url": "https://farmacialoreto.it/catalogsearch/result/?q="},
    "1000Farmacie": {"domain": "1000farmacie.it", "spedizione_base": 2.90, "soglia_gratis": 29.00, "search_url": "https://www.1000farmacie.it/search?q="},
    "Top Farmacia": {"domain": "topfarmacia.it", "spedizione_base": 4.90, "soglia_gratis": 19.90, "search_url": "https://www.topfarmacia.it/catalogsearch/result/?q="},
    "eFarma": {"domain": "efarma.com", "spedizione_base": 4.90, "soglia_gratis": 29.90, "search_url": "https://www.efarma.com/catalogsearch/result/?q="},
    "Farmacosmo": {"domain": "farmacosmo.it", "spedizione_base": 3.90, "soglia_gratis": 29.90, "search_url": "https://www.farmacosmo.it/ricerca?controller=search&s="}
}

# ---------------------------------------------------------
# 4. CARICAMENTO DATI
# ---------------------------------------------------------
@st.cache_data
def load_data():
    for filename in ["prodotti_1000_minsan.csv", "prodotti.csv"]:
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                df['MINSAN'] = df['MINSAN'].astype(str).str.strip()
                if 'Categoria' not in df.columns:
                    df['Categoria'] = 'Generale'
                return df
            except Exception:
                pass
    return pd.DataFrame()

df_prodotti = load_data()

# ---------------------------------------------------------
# 5. HEADER FULL-WIDTH CHIARO E FRESCO
# ---------------------------------------------------------
st.markdown("""
    <div class="tp-header-container">
        <div class="tp-header-top">
            <div class="tp-logo-box">
                <div>
                    <h1 class="tp-brand-title">Compara<span>carrello.it</span></h1>
                    <div class="tp-brand-tagline">Il motore di ricerca per la tua spesa in farmacia al miglior prezzo totale</div>
                </div>
            </div>
            <div class="tp-value-banner">
                ⚡ <b>Calcolo Carrello Unico:</b> Risparmia sulle spedizioni unificando la tua spesa
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. STRISCIA PARTNER FARMACIE
# ---------------------------------------------------------
chips = "".join([
    f'<div class="pharmacy-chip"><img src="https://www.google.com/s2/favicons?domain={info["domain"]}&sz=32"><span>{nome}</span></div>'
    for nome, info in FARMACIE.items()
])

st.markdown(f"""
    <div class="pharmacy-bar">
        <div class="pharmacy-bar-title">Farmacie Online Monitorate in Tempo Reale</div>
        <div class="pharmacy-grid">{chips}</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. CARRELLO STATE
# ---------------------------------------------------------
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# ---------------------------------------------------------
# 8. RICERCA PRODOTTI
# ---------------------------------------------------------
st.markdown("### 🔍 Cerca e aggiungi un prodotto")

if not df_prodotti.empty:
    c_cat, c_search = st.columns([1, 3], vertical_alignment="bottom")
    
    with c_cat:
        categorie = ["Tutte le Categorie"] + sorted(list(df_prodotti['Categoria'].dropna().unique()))
        cat_selezionata = st.selectbox("Seleziona Categoria:", categorie)
    
    df_filtrato = df_prodotti if cat_selezionata == "Tutte le Categorie" else df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
    
    with c_search:
        opzioni = df_filtrato.apply(lambda row: f"{row['Prodotto']} | MINSAN: {row['MINSAN']}", axis=1).tolist()
        prod_selezionato = st.selectbox("Digita il nome del farmaco o il codice MINSAN:", [""] + opzioni)

    if prod_selezionato:
        minsan_sel = prod_selezionato.split("MINSAN: ")[-1]
        row_prod = df_prodotti[df_prodotti['MINSAN'] == minsan_sel].iloc[0]
        
        # Scheda Prodotto selezionato
        img_url = row_prod['Immagine_URL'] if 'Immagine_URL' in row_prod and pd.notna(row_prod['Immagine_URL']) else "https://cdn-icons-png.flaticon.com/512/883/883407.png"
        
        c_p_img, c_p_info, c_p_btn = st.columns([0.8, 3.2, 1], vertical_alignment="center")
        with c_p_img:
            st.image(img_url, width=65)
        with c_p_info:
            st.markdown(f"**{row_prod['Prodotto']}**")
            st.caption(f"Codice MINSAN: `{row_prod['MINSAN']}` | Categoria: {row_prod.get('Categoria', 'Generale')}")
        with c_p_btn:
            if st.button("➕ Aggiungi al Carrello", type="primary", use_container_width=True):
                st.session_state.carrello.append(row_prod)
                st.success("Aggiunto!")
                st.rerun()

# ---------------------------------------------------------
# 9. CARRELLO UTENTE
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 🛍️ Il tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c_img, c_desc, c_del = st.columns([0.5, 4, 1], vertical_alignment="center")
        with c_img:
            img_url = item['Immagine_URL'] if 'Immagine_URL' in item and pd.notna(item['Immagine_URL']) else "https://cdn-icons-png.flaticon.com/512/883/883407.png"
            st.image(img_url, width=35)
        with c_desc:
            st.markdown(f"**{item['Prodotto']}** `<small style='color:#64748b;'>(MINSAN: {item['MINSAN']})</small>`", unsafe_allow_html=True)
        with c_del:
            if st.button("❌ Rimuovi", key=f"del_{idx}"):
                st.session_state.carrello.pop(idx)
                st.rerun()
                
    if st.button("🗑️ Svuota Carrello"):
        st.session_state.carrello = []
        st.rerun()
else:
    st.info("Il carrello è vuoto. Cerca un prodotto qui sopra per iniziare il confronto.")

# ---------------------------------------------------------
# 10. RISULTATI ED ESITO COMPARATORE
# ---------------------------------------------------------
if st.session_state.carrello:
    st.markdown("---")
    st.markdown("### 📊 Risultato Comparazione Spesa Completa")
    
    risultati = []
    
    for farmacia, info in FARMACIE.items():
        totale_prodotti = 0.0
        disponibili = 0
        
        for item in st.session_state.carrello:
            if farmacia in item and pd.notna(item[farmacia]):
                try:
                    totale_prodotti += float(item[farmacia])
                    disponibili += 1
                except ValueError:
                    pass
                
        if disponibili == len(st.session_state.carrello):
            spese_spedizione = 0.0 if totale_prodotti >= info['soglia_gratis'] else info['spedizione_base']
            mancante_gratis = max(0.0, info['soglia_gratis'] - totale_prodotti)
            totale_complessivo = totale_prodotti + spese_spedizione
            
            primo_minsan = st.session_state.carrello[0]['MINSAN']
            target_url = f"{info['search_url']}{urllib.parse.quote(primo_minsan)}"
            
            risultati.append({
                "farmacia": farmacia,
                "totale_prodotti": totale_prodotti,
                "spese_spedizione": spese_spedizione,
                "totale_complessivo": totale_complessivo,
                "mancante_gratis": mancante_gratis,
                "url": target_url
            })
            
    risultati = sorted(risultati, key=lambda x: x['totale_complessivo'])
    
    if risultati:
        cols_podium = st.columns(min(3, len(risultati)))
        badges = [("1° Posto - Più Economico", "gold", "first"), ("2° Posto", "silver", "second"), ("3° Posto", "bronze", "third")]
        
        for i in range(min(3, len(risultati))):
            res = risultati[i]
            rank_label, badge_color, card_class = badges[i]
            
            if res['mancante_gratis'] > 0:
                ship_html = f'<div class="ship-badge ship-paid">🚚 +€ {res["mancante_gratis"]:.2f} per Sped. GRATIS</div>'
            else:
                ship_html = '<div class="ship-badge ship-free">🎉 Spedizione GRATUITA</div>'

            with cols_podium[i]:
                st.markdown(f"""
                    <div class="result-card {card_class}">
                        <div>
                            <span class="badge-rank {badge_color}">{rank_label}</span>
                            <h3 style="margin: 4px 0; color: #0f172a; font-size: 1.25rem;">{res['farmacia']}</h3>
                            <div class="price-tag">€ {res['totale_complessivo']:.2f}</div>
                            <small style="color: #64748b;">Prodotti: € {res['totale_prodotti']:.2f} | Sped: € {res['spese_spedizione']:.2f}</small><br>
                            {ship_html}
                        </div>
                        <div style="margin-top: 14px;">
                            <a href="{res['url']}" target="_blank" style="text-decoration:none;">
                                <button style="width:100%; background-color:#ea580c; color:white; border:none; padding:10px; border-radius:8px; font-weight:700; cursor:pointer;">
                                    🛒 Vai alla Farmacia
                                </button>
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
        with st.expander("📊 Guarda la classifica completa di tutte le farmacie"):
            df_res = pd.DataFrame(risultati)[['farmacia', 'totale_prodotti', 'spese_spedizione', 'totale_complessivo']]
            df_res.columns = ['Farmacia', 'Totale Prodotti (€)', 'Spedizioni (€)', 'Totale Carrello (€)']
            st.dataframe(df_res.style.format({'Totale Prodotti (€)': '{:.2f}', 'Spedizioni (€)': '{:.2f}', 'Totale Carrello (€)': '{:.2f}'}), use_container_width=True)
