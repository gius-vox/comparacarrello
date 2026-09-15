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
# 3. DESIGN SYSTEM - RESPONSIVE MOBILE & PC
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* SEZIONE BRAND CENTRATA IN ALTO */
    .brand-hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px 10px;
        background: transparent;
    }

    .brand-hero-logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 6px;
        width: 100%;
    }

    .brand-hero-img {
        height: 65px;
        width: auto;
        object-fit: contain;
    }

    .brand-hero-title {
        font-size: clamp(1.6rem, 6vw, 2.8rem);
        font-weight: 800;
        color: #047857;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
        white-space: nowrap;
    }

    .brand-hero-title span {
        color: #ea580c;
    }

    .brand-hero-tagline {
        color: #475569;
        font-size: clamp(0.85rem, 3vw, 1.05rem);
        font-weight: 600;
        margin-top: 6px;
        padding: 0 10px;
    }

    /* BARRA VERDE CON SLOGAN */
    .value-green-bar {
        background: linear-gradient(90deg, #047857 0%, #10b981 100%);
        margin-left: -5rem;
        margin-right: -5rem;
        padding: 12px 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(4, 120, 87, 0.15);
        border-bottom: 3px solid #ea580c;
        margin-bottom: 20px;
        color: #ffffff;
    }

    .value-slogan-main {
        font-size: clamp(0.95rem, 3.5vw, 1.15rem);
        font-weight: 800;
        color: #ffffff;
    }

    .value-slogan-sub {
        font-size: clamp(0.8rem, 2.8vw, 0.95rem);
        font-weight: 600;
        color: #ecfdf5;
        margin-top: 4px;
    }

    /* REGOLE OTTIMIZZAZIONE PER SMARTPHONE */
    @media (max-width: 640px) {
        .brand-hero-logo-box {
            flex-direction: column;
            gap: 8px;
        }
        .brand-hero-img {
            height: 55px;
        }
        .value-green-bar {
            margin-left: -1rem;
            margin-right: -1rem;
            padding: 10px 10px;
        }
    }

    /* BARRA FARMACIE MONITORATE */
    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 15px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .pharmacy-bar-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
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
        font-size: 0.78rem;
        color: #334155;
    }
    .pharmacy-chip img {
        width: 14px;
        height: 14px;
        border-radius: 50%;
    }

    /* CARD RISULTATI COMPATTE */
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

    .minsan-tag {
        background-color: #f1f5f9;
        color: #0f766e;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-family: monospace;
        font-weight: 700;
    }

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
# 6. HEADER CENTRATO + BANNER CON SLOGAN
# ---------------------------------------------------------
logo_html = f'<img src="{logo_src}" class="brand-hero-img">' if logo_src else '<div style="font-size:3rem;">🛒</div>'

st.markdown(f"""
    <div class="brand-hero-section">
        <div class="brand-hero-logo-box">
            {logo_html}
            <h1 class="brand-hero-title">Compara<span>carrello.it</span></h1>
        </div>
        <div class="brand-hero-tagline">Il motore di ricerca per la tua spesa in farmacia al miglior prezzo totale</div>
    </div>

    <div class="value-green-bar">
        <div class="value-slogan-main">🛒 Con Comparacarrello fare la spesa online è bello!</div>
        <div class="value-slogan-sub">⚡ Zero stress per la tua scelta, trova i prodotti giusti ed in fretta!</div>
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

DEFAULT_IMG = "https://cdn-icons-png.flaticon.com/512/3028/3028549.png"

if not df_prodotti.empty:
    c_cat, c_search = st.columns([1, 3], vertical_alignment="bottom")
    
    with c_cat:
        categorie = ["Tutte le Categorie"] + sorted(list(df_prodotti['Categoria'].dropna().unique()))
        cat_selezionata = st.selectbox("Seleziona Categoria:", categorie)
    
    df_filtrato = df_prodotti if cat_selezionata == "Tutte le Categorie" else df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
    
    with c_search:
        opzioni = df_filtrato.apply(lambda row: f"{row['Prodotto']} | MINSAN: {row['MINSAN']}", axis=1).tolist()
        prod_selezionato = st.selectbox(
            "Digita il nome del farmaco o il codice MINSAN:", 
            options=opzioni,
            index=None,
            placeholder="Cerca o seleziona un farmaco..."
        )

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
# 10. CARRELLO UTENTE
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
# 11. RISULTATI COMPARAZIONE
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
