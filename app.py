import os
import streamlit as st
import pandas as pd
import urllib.parse
import base64
import io
import qrcode
from supabase import create_client, Client

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
# 2. CONFIGURAZIONE SUPABASE (CLOUD)
# ---------------------------------------------------------
@st.cache_resource
def init_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
        except Exception:
            pass

    if not url or not key:
        st.error("⚠️ Credenziali di Supabase non trovate! Controlla le variabili d'ambiente su Render.")
        st.stop()

    return create_client(url, key)

supabase = init_supabase()

# ---------------------------------------------------------
# 3. HELPER ASSETS & LOGO
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
# 4. DESIGN SYSTEM (MODERNO, MEDICAL-TECH & HIGH-IMPACT)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1100px !important;
        margin: 0 auto;
    }
    
    .brand-hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 32px 24px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .brand-hero-logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin-bottom: 12px;
        width: 100%;
        flex-wrap: wrap;
    }

    .brand-hero-img {
        max-height: 60px !important;
        width: auto;
        object-fit: contain;
        display: block;
    }

    .brand-hero-title {
        font-size: clamp(2rem, 5vw, 2.8rem) !important;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .brand-hero-title span { color: #38bdf8; }

    .brand-hero-tagline {
        color: #cbd5e1;
        font-size: clamp(0.95rem, 2.5vw, 1.12rem);
        font-weight: 600;
        margin-top: 8px;
        text-align: center;
    }

    .brand-hero-subtagline {
        color: #94a3b8;
        font-size: clamp(0.82rem, 2vw, 0.92rem);
        font-weight: 500;
        margin-top: 4px;
        text-align: center;
    }

    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    
    .pharmacy-bar-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 800;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
        text-align: center;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
    }

    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.78rem;
        color: #334155;
    }

    .pharmacy-chip img { width: 15px; height: 15px; border-radius: 50%; }

    .search-section-title {
        text-align: center;
        color: #0f172a;
        font-weight: 800;
        font-size: 1.35rem;
        margin-top: 20px;
        margin-bottom: 14px;
    }

    .product-preview-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #0f766e;
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    .result-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 16px;
    }
    
    .result-card.first {
        border: 2px solid #0f766e;
        background: #ffffff;
        box-shadow: 0 10px 25px rgba(15, 118, 110, 0.12);
    }

    .badge-rank {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 800;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-rank.gold { background-color: #f0fdf4; color: #047857; border: 1px solid #dcfce7; }
    .badge-rank.silver { background-color: #f8fafc; color: #475569; border: 1px solid #e2e8f0; }
    .badge-rank.standard { background-color: #f8fafc; color: #64748b; border: 1px solid #e2e8f0; }

    .farmacia-name {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0f172a;
        margin: 2px 0 12px 0;
    }

    .calculation-receipt-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 14px;
        text-align: left;
        margin-bottom: 12px;
    }

    .calc-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: #475569;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .calc-divider {
        border-top: 1px dashed #cbd5e1;
        margin: 8px 0;
    }

    .calc-total-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 1rem;
        font-weight: 800;
        color: #0f172a;
    }

    .calc-total-amount {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f766e;
    }

    .shipping-info-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 0.76rem;
        color: #334155;
        text-align: left;
        line-height: 1.35;
        margin-bottom: 12px;
    }

    .shipping-info-box.free {
        background-color: #f0fdf4;
        border: 1px solid #dcfce7;
        color: #166534;
        font-weight: 700;
    }

    .redirect-disclaimer {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 6px;
        line-height: 1.25;
    }

    .minsan-tag {
        background-color: #f1f5f9;
        color: #0f766e;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-family: monospace;
        font-weight: 700;
        border: 1px solid #e2e8f0;
    }

    .footer-container {
        margin-top: 50px;
        padding: 25px 20px;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        text-align: center;
        color: #64748b;
        font-size: 0.82rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. CONFIGURAZIONE FARMACIE PARTNER
# ---------------------------------------------------------
FARMACIE = {
    "Farmaè": {"domain": "farmae.it", "spedizione_base": 3.90, "soglia_gratis": 19.90, "search_url": "https://www.farmae.it/catalogsearch/result/?q="},
    "Farmacia Igea": {"domain": "farmaciaigea.com", "spedizione_base": 4.90, "soglia_gratis": 29.00, "search_url": "https://www.farmaciaigea.com/ricerca?search_query="},
    "1000Farmacie": {"domain": "1000farmacie.it", "spedizione_base": 2.90, "soglia_gratis": 29.00, "search_url": "https://www.1000farmacie.it/search?q="},
    "Top Farmacia": {"domain": "topfarmacia.it", "spedizione_base": 4.90, "soglia_gratis": 19.90, "search_url": "https://www.topfarmacia.it/catalogsearch/result/?q="},
    "eFarma": {"domain": "efarma.com", "spedizione_base": 4.90, "soglia_gratis": 29.90, "search_url": "https://www.efarma.com/catalogsearch/result/?q="},
    "Farmacosmo": {"domain": "farmacosmo.it", "spedizione_base": 3.90, "soglia_gratis": 29.90, "search_url": "https://www.farmacosmo.it/ricerca?controller=search&s="},
    "Farmacia Loreto": {"domain": "farmacialoreto.it", "spedizione_base": 4.90, "soglia_gratis": 29.90, "search_url": "https://farmacialoreto.it/catalogsearch/result/?q="},
    "Antica Farmacia Orlandi": {"domain": "farma.it", "spedizione_base": 3.90, "soglia_gratis": 24.90, "search_url": "https://www.farma.it/catalogsearch/result/?q="}
}

# ---------------------------------------------------------
# 6. LETTURA PURA DA SUPABASE
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def load_data_from_supabase():
    try:
        response = supabase.table("prodotti_farmacia").select("*").execute()
        if response.data:
            return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Errore di connessione a Supabase: {e}")
    return pd.DataFrame()

df_prodotti = load_data_from_supabase()

# ---------------------------------------------------------
# 7. CORPO PRINCIPALE (COMPARACARRELLO.IT)
# ---------------------------------------------------------

logo_html = f'<img src="{logo_src}" class="brand-hero-img">' if logo_src else '''
    <div style="background: #ffffff; width: 52px; height: 52px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border: 2px solid #38bdf8;">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
    </div>
'''

st.markdown(f"""
    <div class="brand-hero-card">
        <div class="brand-hero-logo-box">
            {logo_html}
            <h1 class="brand-hero-title">Compara<span>carrello.it</span></h1>
        </div>
        <div class="brand-hero-tagline">Compara i prezzi dei farmaci e prodotti da banco nelle migliori farmacie online</div>
        <div class="brand-hero-subtagline">Calcoliamo in tempo reale il totale del tuo carrello incluse le spese di spedizione</div>
    </div>
""", unsafe_allow_html=True)

# Chips farmacie con loghi originali
chips = "".join([
    f'<div class="pharmacy-chip"><img src="https://www.google.com/s2/favicons?domain={info["domain"]}&sz=32"><span>{nome}</span></div>'
    for nome, info in FARMACIE.items()
])

st.markdown(f"""
    <div class="pharmacy-bar">
        <div class="pharmacy-bar-title">Migliori Farmacie Online Monitorate in Tempo Reale</div>
        <div class="pharmacy-grid">{chips}</div>
    </div>
""", unsafe_allow_html=True)

if 'carrello' not in st.session_state:
    st.session_state.carrello = []

st.markdown('<div class="search-section-title">Cerca e aggiungi un prodotto</div>', unsafe_allow_html=True)

if not df_prodotti.empty:
    query_testo = st.text_input("Inserisci il nome del farmaco o il codice MINSAN:", placeholder="Es. Tachipirina, 34947019...")

    if query_testo and len(query_testo.strip()) >= 1:
        parola = query_testo.strip().lower()
        df_risultati_ricerca = df_prodotti[
            df_prodotti['Prodotto'].str.lower().str.contains(parola, na=False) |
            df_prodotti['MINSAN'].astype(str).str.contains(parola, na=False)
        ]
    else:
        df_risultati_ricerca = pd.DataFrame()

    if not df_risultati_ricerca.empty:
        opzioni_prodotti = [f"{row['Prodotto']} (MINSAN: {row['MINSAN']})" for _, row in df_risultati_ricerca.iterrows()]
        
        prod_scelto = st.selectbox("Seleziona il prodotto dai risultati:", options=opzioni_prodotti, index=0, label_visibility="collapsed")
        
        if prod_scelto:
            minsan_selezionato = prod_scelto.split("MINSAN: ")[-1].replace(")", "").strip()
            riga_Q = df_prodotti[df_prodotti['MINSAN'].astype(str) == str(minsan_selezionato)]
            
            if not riga_Q.empty:
                row_prod = riga_Q.iloc[0]
                
                st.markdown('<div class="product-preview-card">', unsafe_allow_html=True)
                c_p_info, c_p_btn = st.columns([4, 1.2], vertical_alignment="center")
                with c_p_info:
                    st.markdown(f"<h4 style='margin:0; font-weight:800; color:#0f172a;'>{row_prod['Prodotto']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top:4px; color:#475569; font-size:0.85rem;'>Codice MINSAN: <span class='minsan-tag'>{row_prod['MINSAN']}</span> | Categoria: <b style='color:#0f766e;'>{row_prod['Categoria']}</b></div>", unsafe_allow_html=True)
                with c_p_btn:
                    if st.button("Aggiungi", type="primary", use_container_width=True):
                        st.session_state.carrello.append(row_prod.to_dict())
                        st.success("Aggiunto!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    elif query_testo and len(query_testo.strip()) >= 1:
        st.warning("Nessun prodotto trovato con questo nome o codice MINSAN.")
    else:
        st.info("💡 Digita il nome di un farmaco o un codice MINSAN nella casella sopra per iniziare la ricerca.")
else:
    st.error("Il database di Supabase è vuoto. Carica il catalogo dei prodotti su Supabase per iniziare.")

st.markdown("---")
st.markdown("### Il tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c_desc, c_del = st.columns([4, 1], vertical_alignment="center")
        with c_desc:
            st.markdown(f"**{item['Prodotto']}** &nbsp; <span class='minsan-tag'>MINSAN: {item['MINSAN']}</span>", unsafe_allow_html=True)
        with c_del:
            if st.button("Rimuovi", key=f"del_{idx}", use_container_width=True):
                st.session_state.carrello.pop(idx)
                st.rerun()
                
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    if st.button("Svuota Carrello"):
        st.session_state.carrello = []
        st.rerun()
else:
    st.info("Il carrello è vuoto. Cerca un prodotto qui sopra per iniziare il confronto.")

if st.session_state.carrello:
    st.markdown("---")
    st.markdown("### Risultato Comparazione Spesa Completa")
    
    risultati = []
    lista_minsan = [str(item['MINSAN']) for item in st.session_state.carrello]
    
    for farmacia, info in FARMACIE.items():
        totale_prodotti = 0.0
        disponibili = 0
        
        for item in st.session_state.carrello:
            if farmacia in item and pd.notna(item[farmacia]):
                try:
                    val_clean = str(item[farmacia]).replace(',', '.').strip()
                    totale_prodotti += float(val_clean)
                    disponibili += 1
                except ValueError:
                    pass
                
        if disponibili == len(st.session_state.carrello):
            spese_spedizione = 0.0 if totale_prodotti >= info['soglia_gratis'] else info['spedizione_base']
            mancante_gratis = max(0.0, info['soglia_gratis'] - totale_prodotti)
            totale_complessivo = totale_prodotti + spese_spedizione
            
            primo_minsan = st.session_state.carrello[0]['MINSAN']
            target_url = f"{info['search_url']}{urllib.parse.quote(str(primo_minsan))}"
            
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
        cols_per_row = 2
        for i in range(0, len(risultati), cols_per_row):
            batch_cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                idx = i + j
                if idx < len(risultati):
                    res = risultati[idx]
                    
                    if idx == 0:
                        rank_label = "1° Posto - Più Economico"
                        badge_color = "gold"
                        card_class = "first"
                    elif idx == 1:
                        rank_label = "2° Posto"
                        badge_color = "silver"
                        card_class = ""
                    else:
                        rank_label = f"{idx + 1}° Posto"
                        badge_color = "standard"
                        card_class = ""
                    
                    if res['spese_spedizione'] == 0:
                        sped_str = "<span style='color:#0f766e; font-weight:800;'>GRATIS</span>"
                        info_ship_box = '<div class="shipping-info-box free"><b>Spedizione gratuita sbloccata!</b> Soglia minima superata.</div>'
                    else:
                        sped_str = f"+ € {res['spese_spedizione']:.2f}"
                        mancante_fmt = f"{res['mancante_gratis']:.2f}"
                        soglia_fmt = f"{res['soglia_gratis']:.2f}"
                        farmacia_nome = res['farmacia']
                        info_ship_box = (
                            f'<div class="shipping-info-box">'
                            f'<b>Azzera la spedizione:</b><br>'
                            f'Aggiungi altri <b>€ {mancante_fmt}</b> su {farmacia_nome} '
                            f'(soglia a € {soglia_fmt}).'
                            f'</div>'
                        )

                    html_card = (
                        f'<div class="result-card {card_class}">'
                        f'<span class="badge-rank {badge_color}">{rank_label}</span>'
                        f'<div class="farmacia-name">{res["farmacia"]}</div>'
                        f'<div class="calculation-receipt-box">'
                        f'<div class="calc-row"><span>Prezzo prodotti</span><span>€ {res["totale_prodotti"]:.2f}</span></div>'
                        f'<div class="calc-row"><span>Spese spedizione</span><span>{sped_str}</span></div>'
                        f'<div class="calc-divider"></div>'
                        f'<div class="calc-total-row"><span>TOTALE SPESA</span><span class="calc-total-amount">€ {res["totale_complessivo"]:.2f}</span></div>'
                        f'</div>'
                        f'{info_ship_box}'
                        f'<div style="margin-top: 8px;">'
                        f'<a href="{res["url"]}" target="_blank" style="text-decoration:none;">'
                        f'<button style="width:100%; background-color:#0f766e; color:white; border:none; padding:11px 14px; border-radius:10px; font-weight:800; cursor:pointer; font-size:0.88rem; box-shadow:0 4px 12px rgba(15, 118, 110, 0.2);">Acquista su {res["farmacia"]}</button>'
                        f'</a>'
                        f'<div class="redirect-disclaimer">Reindirizzamento al sito ufficiale della farmacia.</div>'
                        f'</div>'
                        f'</div>'
                    )

                    with batch_cols[j]:
                        st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Condividi Carrello o Salvalo sul Cellulare")
    
    testo_condivisione = f"Ecco i codici MINSAN della mia spesa su Comparacarrello.it: {', '.join(lista_minsan)}"
    text_encoded = urllib.parse.quote(testo_condivisione)
    
    whatsapp_url = f"https://api.whatsapp.com/send?text={text_encoded}"
    telegram_url = f"https://t.me/share/url?url=https://comparacarrello.it&text={text_encoded}"
    
    qr_code_img = generate_qr_code_base64(testo_condivisione)
    
    col_qr, col_social = st.columns([1, 2], vertical_alignment="center")
    
    with col_qr:
        st.markdown(f"""
            <div style="text-align: center; background: white; padding: 12px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow:0 4px 12px rgba(0,0,0,0.02);">
                <img src="{qr_code_img}" style="width: 110px; height: 110px;"><br>
                <small style="color: #64748b; font-weight: 700;">Inquadra per aprire sul telefono</small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_social:
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px 16px; border-radius:10px; font-weight:800; cursor:pointer; box-shadow:0 4px 12px rgba(37, 211, 102, 0.15);">
                        Condividi Carrello su WhatsApp
                    </button>
                </a>
                <a href="{telegram_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#0088cc; color:white; border:none; padding:12px 16px; border-radius:10px; font-weight:800; cursor:pointer; box-shadow:0 4px 12px rgba(0, 136, 204, 0.15);">
                        Condividi Carrello su Telegram
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-container">
    <b>Comparacarrello.it</b> è un motore di ricerca indipendente per farmacie online.<br>
    I prezzi e le disponibilità dei prodotti possono variare in tempo reale sui siti dei partner affiliati.<br>
    © 2026 Comparacarrello.it - Tutti i diritti riservati.
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ Chi Siamo"):
    st.markdown("""
    **Comparacarrello.it** è un progetto ideato e sviluppato da **Giuseppe Voci**. 
    
    Nasce prima di tutto da un'esigenza personale come fruitore di prodotti farmaceutici e parafarmaceutici. Da padre di due bambini, alla continua ricerca del risparmio, mi sono spesso trovato in difficoltà a conciliare il minor prezzo con le spese di spedizione: a volte il prezzo più basso di un farmaco era in una farmacia e quello di un altro in un'altra, e in mezzo c'era sempre l'incognita variabile della spedizione.
    
    Da questa frustrazione quotidiana è nata l'idea di creare questo strumento indipendente, per aiutare tutti i consumatori a orientarsi in modo semplice, trasparente e veloce nel mondo delle farmacie online italiane.
    """)

with st.expander("⚖️ Privacy & Cookie Policy"):
    st.markdown("""
    La presente informativa descrive le modalità di gestione di **Comparacarrello.it** in riferimento al trattamento dei dati personali degli utenti che consultano il portale.
    
    * **Trattamento dei dati:** Il nostro sito utilizza cookie tecnici e di analisi anonima per ottimizzare l'esperienza di navigazione. Non raccogliamo dati di profilazione invasivi.
    * **Trasparenza dell'Affiliazione:** Cliccando sui pulsanti di acquisto verrai reindirizzato sui siti ufficiali dei nostri partner commerciali. Durante l'acquisto sul loro portale si applicheranno le rispettive normative e condizioni di vendita della singola farmacia online.
    """)

with st.expander("✉️ Contatti"):
    st.markdown("""
    Hai domande, suggerimenti o desideri metterti in contatto con me? 
    Puoi scrivermi direttamente all'indirizzo email dedicato:
    
    📧 **info@comparacarrello.it**
    
    Risponderò nel più breve tempo possibile!
    """)
