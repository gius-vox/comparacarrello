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
# 2. STILE CSS AVANZATO E DESIGN SYSTEM
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Banner Strategico Risparmio */
    .hero-banner {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        border: 1px solid #fed7aa;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 25px;
    }
    .hero-title {
        color: #9a3412;
        font-weight: 800;
        font-size: 1.2rem;
        margin-bottom: 4px;
    }
    .hero-desc {
        color: #431407;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Header Titolo */
    .brand-title-main {
        font-size: 2.6rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        line-height: 1.1;
    }
    .brand-title-main span {
        color: #f97316;
    }
    .brand-subtitle-main {
        font-size: 1.05rem;
        color: #64748b;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Griglia Farmacie (Chips) */
    .partner-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        margin-bottom: 20px;
    }
    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        padding: 6px 12px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #334155;
    }
    .pharmacy-chip img {
        width: 16px;
        height: 16px;
        border-radius: 50%;
    }

    /* Card Risultati Podio */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .result-card.first {
        border: 2px solid #f97316;
        background: #fffbf7;
        box-shadow: 0 8px 24px rgba(249, 115, 22, 0.12);
    }
    .badge-rank {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .badge-rank.gold { background-color: #fef3c7; color: #92400e; }
    .badge-rank.silver { background-color: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background-color: #ffedd5; color: #9a3412; }

    .price-tag {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin: 8px 0;
    }

    .ship-badge {
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
    }
    .ship-free { background-color: #dcfce7; color: #166534; }
    .ship-paid { background-color: #fef9c3; color: #854d0e; }

    /* Customizzazioni Stili Streamlit */
    .stButton>button[kind="primary"] {
        background-color: #f97316 !important;
        border-color: #f97316 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. DATI FARMACIE MONITORATE & SOGLIE SPEDIZIONE
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
# 4. CARICAMENTO DATI PRODOTTI CSV
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
            except Exception as e:
                st.error(f"Errore lettura file {filename}: {e}")
    st.error("Nessun file CSV trovato con i dati dei prodotti.")
    return pd.DataFrame()

df_prodotti = load_data()

# ---------------------------------------------------------
# 5. HEADER & LOGO
# ---------------------------------------------------------
logo_filename = None
for name in ["logo.png", "logo_comparacarrello.png", "logo.jpg"]:
    if os.path.exists(name):
        logo_filename = name
        break

col_logo, col_title = st.columns([1, 4], vertical_alignment="center")

with col_logo:
    if logo_filename:
        st.image(logo_filename, width=180)
    else:
        st.markdown("<h1 style='font-size: 3rem; margin:0;'>🛒</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("""
        <h1 class="brand-title-main">Compara<span>carrello.it</span></h1>
        <p class="brand-subtitle-main">Confronta il prezzo TOTALE del tuo carrello nelle farmacie online italiane.</p>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Banner Esplicativo Vantaggio Competitivo
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">💡 Perché usare Comparacarrello invece dei classici comparatori?</div>
        <p class="hero-desc">I comparatori tradizionali ti mostrano il prezzo di un singolo pezzo, ma se compri 3 o 4 articoli rischi di pagare le spese di spedizione su siti diversi. <b>Comparacarrello calcola il totale complessivo della tua spesa in un'unica farmacia</b>, azzerando le spedizioni e garantendoti il massimo risparmio reale.</p>
    </div>
""", unsafe_allow_html=True)

# Griglia Farmacie Partner
st.markdown('<div class="partner-label">Farmacie Online Monitorate in Tempo Reale:</div>', unsafe_allow_html=True)
chips = ""
for nome, info in FARMACIE.items():
    icon_url = f"https://www.google.com/s2/favicons?domain={info['domain']}&sz=64"
    chips += f'<div class="pharmacy-chip"><img src="{icon_url}"><span>{nome}</span></div>'
st.markdown(f'<div class="pharmacy-grid">{chips}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. CARRELLO STATE
# ---------------------------------------------------------
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# ---------------------------------------------------------
# 7. RICERCA E AGGIUNTA PRODOTTI
# ---------------------------------------------------------
st.subheader("🔍 Cerca e Aggiungi Prodotti alla tua Spesa")

if not df_prodotti.empty:
    col_cat, col_search = st.columns([1, 2.5])
    
    with col_cat:
        categorie = ["Tutte le Categorie"] + sorted(list(df_prodotti['Categoria'].dropna().unique()))
        cat_selezionata = st.selectbox("Filtra Categoria:", categorie)
    
    df_filtrato = df_prodotti if cat_selezionata == "Tutte le Categorie" else df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
    
    with col_search:
        opzioni = df_filtrato.apply(lambda row: f"{row['Prodotto']} | MINSAN: {row['MINSAN']}", axis=1).tolist()
        prod_selezionato = st.selectbox("Digita il Nome o il Codice MINSAN del prodotto:", [""] + opzioni)

    if prod_selezionato:
        minsan_sel = prod_selezionato.split("MINSAN: ")[-1]
        row_prod = df_prodotti[df_prodotti['MINSAN'] == minsan_sel].iloc[0]
        
        # Scheda Dettaglio Prodotto selezionato prima dell'aggiunta
        with st.container():
            c_img, c_info, c_btn = st.columns([1, 3, 1.5], vertical_alignment="center")
            with c_img:
                img_url = row_prod['Immagine_URL'] if 'Immagine_URL' in row_prod and pd.notna(row_prod['Immagine_URL']) else "https://cdn-icons-png.flaticon.com/512/883/883407.png"
                st.image(img_url, width=70)
            with c_info:
                st.markdown(f"**{row_prod['Prodotto']}**")
                st.caption(f"Codice MINSAN: `{row_prod['MINSAN']}` | Categoria: {row_prod.get('Categoria', 'Generale')}")
            with c_btn:
                if st.button("➕ Aggiungi al Carrello", use_container_width=True, type="primary"):
                    st.session_state.carrello.append(row_prod)
                    st.success("Aggiunto!")
                    st.rerun()

# ---------------------------------------------------------
# 8. VISUALIZZAZIONE CARRELLO UTENTE
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🛍️ Prodotti attualmente nel tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c_img, c_desc, c_del = st.columns([0.8, 4, 1], vertical_alignment="center")
        with c_img:
            img_url = item['Immagine_URL'] if 'Immagine_URL' in item and pd.notna(item['Immagine_URL']) else "https://cdn-icons-png.flaticon.com/512/883/883407.png"
            st.image(img_url, width=45)
        with c_desc:
            st.write(f"📦 **{item['Prodotto']}** *(MINSAN: {item['MINSAN']})*")
        with c_del:
            if st.button("❌ Rimuovi", key=f"del_{idx}"):
                st.session_state.carrello.pop(idx)
                st.rerun()
                
    if st.button("🗑️ Svuota interamente il carrello"):
        st.session_state.carrello = []
        st.rerun()
else:
    st.info("Il tuo carrello è vuoto. Cerca un prodotto in alto per iniziare la comparazione della tua spesa.")

# ---------------------------------------------------------
# 9. ALGORITMO COMPARATORE DI CARRELLO
# ---------------------------------------------------------
if st.session_state.carrello:
    st.markdown("---")
    st.subheader("📊 Risultato Comparazione della tua Spesa")
    st.caption("Classifica ordinata dal totale reale più economico (Prodotti + Spese Spedizione spediti in un'unica soluzione).")
    
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
            
            # Generazione link di ricerca per il primo prodotto per velocizzare l'acquisto
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
                            <h3 style="margin: 6px 0; color: #1e293b; font-size: 1.35rem;">{res['farmacia']}</h3>
                            <div class="price-tag">€ {res['totale_complessivo']:.2f}</div>
                            <small style="color: #64748b; font-size: 0.88rem;">Prodotti: € {res['totale_prodotti']:.2f} | Spedizione: € {res['spese_spedizione']:.2f}</small><br>
                            {ship_html}
                        </div>
                        <div style="margin-top: 15px;">
                            <a href="{res['url']}" target="_blank" style="text-decoration:none;">
                                <button style="width:100%; background-color:#f97316; color:white; border:none; padding:12px; border-radius:10px; font-weight:700; cursor:pointer;">
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

# ---------------------------------------------------------
# 10. FOOTER & CONDIVISIONE
# ---------------------------------------------------------
st.markdown("---")
c_share1, c_share2 = st.columns(2)
with c_share1:
    st.subheader("💬 Condividi Comparacarrello.it")
    st.markdown("[📲 Condividi su WhatsApp](https://api.whatsapp.com/send?text=Confronta%20il%20prezzo%20della%20tua%20spesa%20in%20farmacia)")
with c_share2:
    st.subheader("📱 QR Code App")
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://comparacarrello-1.onrender.com", width=120)
