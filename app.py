import streamlit as st
import pandas as pd
import os
import urllib.parse
import base64
import io
import qrcode

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
# 2. HELPER LOGO & QR CODE BASE64
# ---------------------------------------------------------
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            ext = path.split('.')[-1]
            return f"data:image/{ext};base64,{encoded}"
    return None

def generate_qr_code_base64(data_string):
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(data_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

logo_src = None
for name in ["logo.png", "logo_comparacarrello.png", "logo.jpg"]:
    logo_src = get_image_base64(name)
    if logo_src:
        break

# ---------------------------------------------------------
# 3. DESIGN SYSTEM - VERDE FARMACIA + CARD COMPATTE
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* HEADER VERDE FARMACIA */
    .tp-header-container {
        background: linear-gradient(90deg, #047857 0%, #10b981 100%);
        margin-left: -5rem;
        margin-right: -5rem;
        padding: 20px 5rem 22px 5rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
        border-bottom: 4px solid #ea580c;
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
        gap: 18px;
    }

    .tp-logo-img {
        height: 55px;
        width: auto;
        object-fit: contain;
        background: #ffffff;
        padding: 6px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .tp-brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .tp-brand-title span {
        color: #f97316;
    }

    .tp-brand-tagline {
        color: #ecfdf5;
        font-size: 0.88rem;
        font-weight: 500;
        margin-top: 2px;
    }

    .tp-value-banner {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 30px;
        padding: 6px 16px;
        color: #ffffff;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* BARRA FARMACIE */
    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 10px 18px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .pharmacy-bar-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 6px;
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
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.78rem;
        color: #334155;
    }
    .pharmacy-chip img {
        width: 14px;
        height: 14px;
        border-radius: 50%;
    }

    /* CARD PODIO RISULTATI COMPATTE */
    .result-card {
        background: white;
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.03);
        text-align: center;
    }
    .result-card.first {
        border: 2px solid #ea580c;
        background: #fffbf7;
        box-shadow: 0 6px 16px rgba(234, 88, 12, 0.12);
    }
    .badge-rank {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .badge-rank.gold { background-color: #fef3c7; color: #92400e; }
    .badge-rank.silver { background-color: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background-color: #ffedd5; color: #9a3412; }

    .price-tag {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin: 2px 0;
    }

    .ship-info-box {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 6px;
        margin: 8px 0;
        font-size: 0.75rem;
        color: #475569;
        border: 1px dashed #cbd5e1;
    }

    .ship-badge {
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        display: inline-block;
    }
    .ship-free { background-color: #dcfce7; color: #166534; }
    .ship-paid { background-color: #fef9c3; color: #854d0e; }

    /* TAG MINSAN ELEGANTE */
    .minsan-tag {
        background-color: #f1f5f9;
        color: #0f766e;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-family: monospace;
        font-weight: 700;
    }

    /* STREAMLIT BUTTON OVERRIDE */
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
# 4. DATI FARMACIE
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
# 5. CARICAMENTO DATI
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
# 6. HEADER PRINCIPALE
# ---------------------------------------------------------
logo_html = f'<img src="{logo_src}" class="tp-logo-img">' if logo_src else '<div style="font-size:2.2rem;">🛒</div>'

st.markdown(f"""
    <div class="tp-header-container">
        <div class="tp-header-top">
            <div class="tp-logo-box">
                {logo_html}
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
# 7. STRISCIA FARMACIE MONITORATE
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
# 8. CARRELLO STATE
# ---------------------------------------------------------
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# ---------------------------------------------------------
# 9. RICERCA PRODOTTI
# ---------------------------------------------------------
st.markdown("### 🔍 Cerca e aggiungi un prodotto")

DEFAULT_IMG = "https://cdn-icons-png.flaticon.com/512/3028/3028549.png"  # Placeholder elegante farmacia

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
        
        img_url = row_prod['Immagine_URL'] if ('Immagine_URL' in row_prod and pd.notna(row_prod['Immagine_URL']) and str(row_prod['Immagine_URL']).startswith('http')) else DEFAULT_IMG
        
        c_p_img, c_p_info, c_p_btn = st.columns([0.8, 3.2, 1], vertical_alignment="center")
        with c_p_img:
            st.image(img_url, width=60)
        with c_p_info:
            st.markdown(f"**{row_prod['Prodotto']}**")
            st.markdown(f"Codice MINSAN: <span class='minsan-tag'>{row_prod['MINSAN']}</span> | Categoria: {row_prod.get('Categoria', 'Generale')}", unsafe_allow_html=True)
        with c_p_btn:
            if st.button("➕ Aggiungi al Carrello", type="primary", use_container_width=True):
                st.session_state.carrello.append(row_prod)
                st.success("Aggiunto!")
                st.rerun()

# ---------------------------------------------------------
# 10. CARRELLO UTENTE (STRINGA HTML CORRETTA)
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 🛍️ Il tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c_img, c_desc, c_del = st.columns([0.5, 4, 1], vertical_alignment="center")
        with c_img:
            img_url = item['Immagine_URL'] if ('Immagine_URL' in item and pd.notna(item['Immagine_URL']) and str(item['Immagine_URL']).startswith('http')) else DEFAULT_IMG
            st.image(img_url, width=35)
        with c_desc:
            # FIX: Corretto rendering del MINSAN senza la stringa HTML visibile a schermo
            st.markdown(f"**{item['Prodotto']}** &nbsp; <span class='minsan-tag'>MINSAN: {item['MINSAN']}</span>", unsafe_allow_html=True)
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
# 11. RISULTATI COMPARAZIONE (CARD COMPATTE & TRASPARENZA SPEDIZIONE)
# ---------------------------------------------------------
if st.session_state.carrello:
    st.markdown("---")
    st.markdown("### 📊 Risultato Comparazione Spesa Completa")
    
    risultati = []
    lista_minsan = [str(item['MINSAN']) for item in st.session_state.carrello]
    
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
                "soglia_gratis": info['soglia_gratis'],
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
                ship_html = f'<div class="ship-badge ship-paid">🚚 Sped: € {res["spese_spedizione"]:.2f} (+€ {res["mancante_gratis"]:.2f} per Gratis)</div>'
            else:
                ship_html = '<div class="ship-badge ship-free">🎉 Spedizione GRATUITA</div>'

            with cols_podium[i]:
                st.markdown(f"""
                    <div class="result-card {card_class}">
                        <span class="badge-rank {badge_color}">{rank_label}</span>
                        <h4 style="margin: 2px 0; color: #0f172a;">{res['farmacia']}</h4>
                        <div class="price-tag">€ {res['totale_complessivo']:.2f}</div>
                        <div style="font-size: 0.75rem; color: #64748b;">Prodotti: € {res['totale_prodotti']:.2f}</div>
                        <div class="ship-info-box">
                            📌 <b>Soglia Spedizione Gratis: € {res['soglia_gratis']:.2f}</b><br>
                            {ship_html}
                        </div>
                        <div style="margin-top: 10px;">
                            <a href="{res['url']}" target="_blank" style="text-decoration:none;">
                                <button style="width:100%; background-color:#ea580c; color:white; border:none; padding:8px; border-radius:6px; font-weight:700; cursor:pointer; font-size:0.85rem;">
                                    🛒 Vai alla Farmacia
                                </button>
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
        with st.expander("📊 Guarda la classifica completa di tutte le farmacie"):
            df_res = pd.DataFrame(risultati)[['farmacia', 'totale_prodotti', 'spese_spedizione', 'soglia_gratis', 'totale_complessivo']]
            df_res.columns = ['Farmacia', 'Totale Prodotti (€)', 'Spedizioni (€)', 'Soglia Gratis (€)', 'Totale Carrello (€)']
            st.dataframe(df_res.style.format({'Totale Prodotti (€)': '{:.2f}', 'Spedizioni (€)': '{:.2f}', 'Soglia Gratis (€)': '{:.2f}', 'Totale Carrello (€)': '{:.2f}'}), use_container_width=True)

    # ---------------------------------------------------------
    # 12. CONDIVISIONE CARRELLO & QR CODE MOBILE
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📲 Condividi Carrello o Salvalo sul Cellulare")
    
    # Prepara il testo con i codici MINSAN
    testo_condivisione = f"Ecco i codici MINSAN della mia spesa su Comparacarrello.it: {', '.join(lista_minsan)}"
    text_encoded = urllib.parse.quote(testo_condivisione)
    
    whatsapp_url = f"https://api.whatsapp.com/send?text={text_encoded}"
    telegram_url = f"https://t.me/share/url?url=https://comparacarrello.it&text={text_encoded}"
    
    qr_code_img = generate_qr_code_base64(testo_condivisione)
    
    col_qr, col_social = st.columns([1, 2], vertical_alignment="center")
    
    with col_qr:
        st.markdown(f"""
            <div style="text-align: center; background: white; padding: 12px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <img src="{qr_code_img}" style="width: 120px; height: 120px;"><br>
                <small style="color: #64748b; font-weight: 600;">Inquadra per aprire sul telefono</small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_social:
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px 16px; border-radius:8px; font-weight:700; cursor:pointer;">
                        💬 Condividi Carrello su WhatsApp
                    </button>
                </a>
                <a href="{telegram_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#0088cc; color:white; border:none; padding:10px 16px; border-radius:8px; font-weight:700; cursor:pointer;">
                        ✈️ Condividi Carrello su Telegram
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)
