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
# 3. CSS RESPONSIVE & STYLES (OTTIMIZZATO MOBILE & DESKTOP)
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
        max-width: 1200px !important;
        margin: 0 auto;
    }

    /* HEADER BEN ALLINEATO */
    .header-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        padding: 8px 0;
        margin-bottom: 5px;
        flex-wrap: wrap;
        text-align: center;
    }

    .header-logo {
        height: 60px;
        width: auto;
        object-fit: contain;
    }

    .header-title-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .header-title {
        font-size: 2rem;
        font-weight: 800;
        color: #047857;
        line-height: 1.1;
        margin: 0;
    }

    .header-title span { color: #ea580c; }

    .header-subtitle {
        font-size: 0.9rem;
        color: #475569;
        font-weight: 600;
        margin-top: 4px;
    }

    /* BANNER SLOGAN */
    .value-green-bar {
        background: linear-gradient(90deg, #047857 0%, #10b981 100%);
        padding: 10px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(4, 120, 87, 0.12);
        border-bottom: 3px solid #ea580c;
        margin-bottom: 18px;
        color: #ffffff;
        border-radius: 8px;
    }

    .value-slogan-main {
        font-size: 0.95rem;
        font-weight: 800;
    }

    .value-slogan-sub {
        font-size: 0.82rem;
        font-weight: 600;
        color: #ecfdf5;
        margin-top: 2px;
    }

    /* STRISCIA FARMACIE */
    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 18px;
    }
    
    .pharmacy-bar-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 3px 8px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.75rem;
        color: #334155;
    }

    /* CARD RISULTATI COMPATTE */
    .card-result {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }

    .card-result.best {
        border: 2px solid #ea580c;
        box-shadow: 0 6px 16px rgba(234, 88, 12, 0.15);
    }

    .badge-rank {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .badge-rank.gold { background: #fef3c7; color: #92400e; }
    .badge-rank.silver { background: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background: #ffedd5; color: #9a3412; }

    .card-farmacia-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }

    /* SCONTRINO COMPATTO */
    .receipt-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 10px;
        margin-bottom: 8px;
    }

    .receipt-line {
        display: flex;
        justify-content: space-between;
        font-size: 0.82rem;
        color: #475569;
        font-weight: 600;
        margin-bottom: 3px;
    }

    .receipt-divider {
        border-top: 1px dashed #cbd5e1;
        margin: 5px 0;
    }

    .receipt-total {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.95rem;
        font-weight: 800;
        color: #047857;
    }

    .receipt-total-price {
        font-size: 1.35rem;
        font-weight: 800;
        color: #047857;
    }

    /* BOX SOGLIA SPEDIZIONE */
    .ship-alert {
        background-color: #fff7ed;
        border: 1px solid #ffedd5;
        border-radius: 6px;
        padding: 6px 8px;
        font-size: 0.74rem;
        color: #9a3412;
        line-height: 1.3;
        margin-bottom: 10px;
    }
    .ship-alert.free {
        background-color: #f0fdf4;
        border: 1px solid #dcfce7;
        color: #166534;
    }

    /* BOTTONE ACQUISTO */
    .btn-buy {
        display: block;
        width: 100%;
        background-color: #ea580c;
        color: white !important;
        text-align: center;
        padding: 8px 0;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        text-decoration: none !important;
        box-shadow: 0 2px 6px rgba(234, 88, 12, 0.2);
    }
    .btn-buy:hover {
        background-color: #c2410c;
    }

    .btn-subtext {
        font-size: 0.68rem;
        color: #64748b;
        text-align: center;
        margin-top: 4px;
        line-height: 1.2;
    }

    .minsan-tag {
        background-color: #e2e8f0;
        color: #0f766e;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-family: monospace;
        font-weight: 700;
    }

    /* ADATTAMENTI PER SMARTPHONE (MOBILE) */
    @media (max-width: 768px) {
        .header-title { font-size: 1.6rem; }
        .header-subtitle { font-size: 0.8rem; }
        .header-logo { height: 50px; }
        .value-slogan-main { font-size: 0.85rem; }
        .value-slogan-sub { font-size: 0.75rem; }
        .card-farmacia-title { font-size: 1.1rem; }
        .receipt-total-price { font-size: 1.2rem; }
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
# 6. HEADER PERFETTAMENTE ALLINEATO E CENTRATO
# ---------------------------------------------------------
logo_img_html = f'<img src="{logo_src}" class="header-logo">' if logo_src else '<div style="font-size:2.2rem;">🛒</div>'

st.markdown(f"""
    <div class="header-box">
        {logo_img_html}
        <div class="header-title-box">
            <h1 class="header-title">Comparacarrello<span>.it</span></h1>
            <div class="header-subtitle">Il motore di ricerca per la tua spesa in farmacia al miglior prezzo totale</div>
        </div>
    </div>

    <div class="value-green-bar">
        <div class="value-slogan-main">🛒 Con Comparacarrello fare la spesa online è più bello!</div>
        <div class="value-slogan-sub">⚡ Zero stress per la tua scelta, troverai i prodotti giusti ed in fretta!</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. STRISCIA FARMACIE MONITORATE
# ---------------------------------------------------------
chips = "".join([
    f'<div class="pharmacy-chip"><img src="https://www.google.com/s2/favicons?domain={info["domain"]}&sz=32" width="14" height="14"><span>{nome}</span></div>'
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
            st.image(img_url, width=50)
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
            st.image(img_url, width=30)
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
# 11. RISULTATI COMPARAZIONE (HTML PULITO SENZA ERRORE REZZO)
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
        badges_data = [
            ("1° Posto - Più Economico", "gold", "best"),
            ("2° Posto", "silver", ""),
            ("3° Posto", "bronze", "")
        ]
        
        for i in range(min(3, len(risultati))):
            res = risultati[i]
            rank_label, badge_color, best_class = badges_data[i]
            
            if res['spese_spedizione'] == 0:
                sped_label = "<span style='color:#166534;'>GRATIS</span>"
                ship_box_html = '<div class="ship-alert free">🎉 <b>Spedizione GRATIS sbloccata!</b></div>'
            else:
                sped_label = f"+ € {res['spese_spedizione']:.2f}"
                ship_box_html = f'<div class="ship-alert">💡 Aggiungi <b>€ {res["mancante_gratis"]:.2f}</b> per azzerare la spedizione (soglia € {res["soglia_gratis"]:.2f}).</div>'

            card_html = f'''<div class="card-result {best_class}">
<span class="badge-rank {badge_color}">{rank_label}</span>
<div class="card-farmacia-title">{res['farmacia']}</div>
<div class="receipt-box">
<div class="receipt-line"><span>🛍️ Prezzo prodotti</span><span>€ {res['totale_prodotti']:.2f}</span></div>
<div class="receipt-line"><span>🚚 Spedizione</span><span>{sped_label}</span></div>
<div class="receipt-divider"></div>
<div class="receipt-total"><span>💳 TOTALE</span><span class="receipt-total-price">€ {res['totale_complessivo']:.2f}</span></div>
</div>
{ship_box_html}
<a href="{res['url']}" target="_blank" class="btn-buy">↗️ Acquista su {res['farmacia']}</a>
<div class="btn-subtext">Verrai reindirizzato sul sito della farmacia per aggiungere i prodotti al carrello.</div>
</div>'''

            with cols_podium[i]:
                st.markdown(card_html, unsafe_allow_html=True)
                
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
            <div style="text-align: center; background: white; padding: 10px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <img src="{qr_code_img}" style="width: 110px; height: 110px;"><br>
                <small style="color: #64748b; font-weight: 600;">Inquadra per aprire sul telefono</small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_social:
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px 14px; border-radius:8px; font-weight:700; cursor:pointer;">
                        💬 Condividi Carrello su WhatsApp
                    </button>
                </a>
                <a href="{telegram_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#0088cc; color:white; border:none; padding:10px 14px; border-radius:8px; font-weight:700; cursor:pointer;">
                        ✈️ Condividi Carrello su Telegram
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)
