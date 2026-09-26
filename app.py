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

DEFAULT_SVG_IMG = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'>"
    "<rect x='2' y='6' width='20' height='12' rx='2'/>"
    "<path d='M12 10v4M10 12h4'/>"
    "</svg>"
)

# ---------------------------------------------------------
# 4. DESIGN SYSTEM & STYLE CUSTOM
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 1200px !important;
        margin: 0 auto;
    }
    
    .brand-hero-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #cbd5e1;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    .brand-hero-logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 8px;
        width: 100%;
        flex-direction: row !important;
    }

    .brand-hero-img {
        max-height: 65px !important;
        width: auto;
        object-fit: contain;
        display: block;
    }

    .brand-hero-title {
        font-size: clamp(1.8rem, 5vw, 3.0rem) !important;
        font-weight: 800;
        color: #047857;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
        white-space: nowrap !important;
    }

    .brand-hero-title span { color: #ea580c; }

    .brand-hero-tagline {
        color: #334155;
        font-size: clamp(0.9rem, 3vw, 1.15rem);
        font-weight: 700;
        margin-top: 6px;
    }

    .brand-hero-subtagline {
        color: #64748b;
        font-size: clamp(0.8rem, 2.5vw, 0.95rem);
        font-weight: 500;
        margin-top: 4px;
    }

    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .pharmacy-bar-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        color: #64748b;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.78rem;
        color: #334155;
    }

    .pharmacy-chip img { width: 14px; height: 14px; border-radius: 50%; }

    .search-hero-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
        margin-bottom: 25px;
    }

    .product-preview-card {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #047857;
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 12px;
    }

    .product-img-frame {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
    }

    .result-card {
        background: white;
        border-radius: 14px;
        padding: 18px 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 15px;
    }
    
    .result-card.first {
        border: 2px solid #ea580c;
        background: #ffffff;
        box-shadow: 0 8px 20px rgba(234, 88, 12, 0.12);
    }

    .badge-rank {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .badge-rank.gold { background-color: #fef3c7; color: #92400e; }
    .badge-rank.silver { background-color: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background-color: #ffedd5; color: #9a3412; }

    .farmacia-name {
        font-size: 1.3rem;
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
        font-size: 0.88rem;
        color: #475569;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .calc-divider {
        border-top: 2px dashed #cbd5e1;
        margin: 8px 0;
    }

    .calc-total-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 1.1rem;
        font-weight: 800;
        color: #047857;
    }

    .calc-total-amount {
        font-size: 1.7rem;
        font-weight: 800;
        color: #047857;
    }

    .shipping-info-box {
        background-color: #fff7ed;
        border: 1px solid #ffedd5;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 0.78rem;
        color: #9a3412;
        text-align: left;
        line-height: 1.35;
        margin-bottom: 14px;
    }

    .shipping-info-box.free {
        background-color: #f0fdf4;
        border: 1px solid #dcfce7;
        color: #166534;
    }

    .redirect-disclaimer {
        font-size: 0.72rem;
        color: #64748b;
        margin-top: 6px;
        line-height: 1.25;
    }

    .minsan-tag {
        background-color: #f1f5f9;
        color: #0f766e;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-family: monospace;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. CONFIGURAZIONE FARMACIE PARTNER
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
# 6. CARICAMENTO DATI DA SUPABASE
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
# 7. HEADER & BRAND
# ---------------------------------------------------------
logo_html = f'<img src="{logo_src}" class="brand-hero-img">' if logo_src else '<div style="font-size:2.5rem;">🛒</div>'

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

# ---------------------------------------------------------
# 8. STRISCIA FARMACIE MONITORATE
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
# 9. STATE GESTIONE SESSIONE
# ---------------------------------------------------------
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# ---------------------------------------------------------
# 10. MOTORE DI RICERCA LIBERO (SENZA CATEGORIE)
# ---------------------------------------------------------
st.markdown('<div class="search-hero-card">', unsafe_allow_html=True)
st.markdown('<div style="color: #047857; font-size: 1.35rem; font-weight: 800; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 16px;">Cerca e aggiungi un prodotto</div>', unsafe_allow_html=True)

if not df_prodotti.empty:
    query_testo = st.text_input("🔍 Cerca per nome farmaco o codice MINSAN:", placeholder="Digita un termine (es. Tachipirina, Arnica, Belladonna)...")

    if query_testo and len(query_testo.strip()) >= 1:
        q_lower = query_testo.lower()
        df_risultati_ricerca = df_prodotti[df_prodotti['Prodotto'].str.lower().str.contains(q_lower) | df_prodotti['MINSAN'].astype(str).str.contains(q_lower)]
    else:
        df_risultati_ricerca = df_prodotti.head(15)

    if not df_risultati_ricerca.empty:
        opzioni_prodotti = [f"{row['Prodotto']} | Categoria: {row['Categoria']} (MINSAN: {row['MINSAN']})" for _, row in df_risultati_ricerca.iterrows()]
        
        prod_scelto = st.selectbox("Seleziona il prodotto trovato:", options=opzioni_prodotti, index=0, label_visibility="collapsed")
        
        if prod_scelto:
            minsan_selezionato = prod_scelto.split("MINSAN: ")[-1].replace(")", "").strip()
            riga_Q = df_prodotti[df_prodotti['MINSAN'].astype(str) == str(minsan_selezionato)]
            
            if not riga_Q.empty:
                row_prod = riga_Q.iloc[0]
                img_url = row_prod.get('Immagine_URL', '') if pd.notna(row_prod.get('Immagine_URL')) and str(row_prod.get('Immagine_URL')).strip() != '' else DEFAULT_SVG_IMG
                
                st.markdown('<div class="product-preview-card">', unsafe_allow_html=True)
                c_p_img, c_p_info, c_p_btn = st.columns([0.8, 3.2, 1.2], vertical_alignment="center")
                with c_p_img:
                    st.markdown(f'<div class="product-img-frame"><img src="{img_url}"></div>', unsafe_allow_html=True)
                with c_p_info:
                    st.markdown(f"<h4 style='margin:0; font-weight:800; color:#0f172a;'>{row_prod['Prodotto']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top:4px; color:#475569; font-size:0.88rem;'>Codice MINSAN: <span class='minsan-tag'>{row_prod['MINSAN']}</span> | Categoria: <b style='color:#047857;'>{row_prod['Categoria']}</b></div>", unsafe_allow_html=True)
                with c_p_btn:
                    if st.button("Aggiungi al Carrello", type="primary", use_container_width=True):
                        st.session_state.carrello.append(row_prod.to_dict())
                        st.success("Prodotto aggiunto!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Nessun prodotto trovato nel database.")
else:
    st.error("Nessun dato caricato dal database Supabase.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 11. CARRELLO UTENTE
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### Il tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c_img, c_desc, c_del = st.columns([0.6, 4, 1], vertical_alignment="center")
        with c_img:
            img_item = item.get('Immagine_URL', '') if pd.notna(item.get('Immagine_URL')) and str(item.get('Immagine_URL')).strip() != '' else DEFAULT_SVG_IMG
            st.markdown(f'<div class="product-img-frame" style="padding: 2px;"><img src="{img_item}"></div>', unsafe_allow_html=True)
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

# ---------------------------------------------------------
# 12. RISULTATI COMPARAZIONE & SPEDIZIONI
# ---------------------------------------------------------
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
        cols_podium = st.columns(min(3, len(risultati)))
        badges = [("1° Posto - Più Economico", "gold", "first"), ("2° Posto", "silver", "second"), ("3° Posto", "bronze", "third")]
        
        for i in range(min(3, len(risultati))):
            res = risultati[i]
            rank_label, badge_color, card_class = badges[i]
            
            if res['spese_spedizione'] == 0:
                sped_str = "<span style='color:#15803d;'>GRATIS</span>"
                info_ship_box = f'<div class="shipping-info-box free"><b>Spedizione gratuita sbloccata!</b> Hai superato la soglia minima.</div>'
            else:
                sped_str = f"+ € {res['spese_spedizione']:.2f}"
                info_ship_box = f'<div class="shipping-info-box"><b>Vuoi azzerare la spedizione?</b><br>Aggiungi altri <b>€ {res["mancante_gratis"]:.2f}</b> di prodotti su {res["farmacia"]} per sbloccare la spedizione GRATIS (soglia a € {res["soglia_gratis"]:.2f}).</div>'

            html_card = f'''<div class="result-card {card_class}">
<span class="badge-rank {badge_color}">{rank_label}</span>
<div class="farmacia-name">{res["farmacia"]}</div>
<div class="calculation-receipt-box">
<div class="calc-row"><span>Prezzo prodotti</span><span>€ {res["totale_prodotti"]:.2f}</span></div>
<div class="calc-row"><span>Spese di spedizione</span><span>{sped_str}</span></div>
<div class="calc-divider"></div>
<div class="calc-total-row"><span>TOTALE SPESA</span><span class="calc-total-amount">€ {res["totale_complessivo"]:.2f}</span></div>
</div>
{info_ship_box}
<div style="margin-top: 10px;">
<a href="{res["url"]}" target="_blank" style="text-decoration:none;">
<button style="width:100%; background-color:#ea580c; color:white; border:none; padding:11px 14px; border-radius:10px; font-weight:800; cursor:pointer; font-size:0.9rem; box-shadow:0 4px 10px rgba(234, 88, 12, 0.2);">Acquista su {res["farmacia"]}</button>
</a>
<div class="redirect-disclaimer">Verrai reindirizzato sul sito ufficiale della farmacia per selezionare e acquistare i tuoi prodotti.</div>
</div>
</div>'''

            with cols_podium[i]:
                st.markdown(html_card, unsafe_allow_html=True)
                
        with st.expander("Guarda la classifica completa di tutte le farmacie"):
            df_res = pd.DataFrame(risultati)[['farmacia', 'totale_prodotti', 'spese_spedizione', 'soglia_gratis', 'totale_complessivo']]
            df_res.columns = ['Farmacia', 'Totale Prodotti (€)', 'Spedizioni (€)', 'Soglia Gratis (€)', 'Totale Carrello (€)']
            st.dataframe(df_res.style.format({'Totale Prodotti (€)': '{:.2f}', 'Spedizioni (€)': '{:.2f}', 'Soglia Gratis (€)': '{:.2f}', 'Totale Carrello (€)': '{:.2f}'}), use_container_width=True)

    # ---------------------------------------------------------
    # 13. CONDIVISIONE E QR CODE
    # ---------------------------------------------------------
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
            <div style="text-align: center; background: white; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                <img src="{qr_code_img}" style="width: 120px; height: 120px;"><br>
                <small style="color: #64748b; font-weight: 700;">Inquadra per aprire sul telefono</small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_social:
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <a href="{whatsapp_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px 16px; border-radius:10px; font-weight:800; cursor:pointer; box-shadow:0 4px 10px rgba(37, 211, 102, 0.15);">
                        Condividi Carrello su WhatsApp
                    </button>
                </a>
                <a href="{telegram_url}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#0088cc; color:white; border:none; padding:12px 16px; border-radius:10px; font-weight:800; cursor:pointer; box-shadow:0 4px 10px rgba(0, 136, 204, 0.15);">
                        Condividi Carrello su Telegram
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)
