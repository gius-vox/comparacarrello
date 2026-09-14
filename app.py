import streamlit as st
import pandas as pd
import os

# 1. Configurazione della pagina
st.set_page_config(
    page_title="Comparacarrello.it - Risparmia sulla tua spesa in farmacia",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Personalizzato basato sui colori del TUO LOGO (Arancione & Antracite)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Container Header con colori coerenti al Logo */
    .brand-header-container {
        display: flex;
        align-items: center;
        gap: 25px;
        padding: 10px 0 25px 0;
        border-bottom: 2px solid #f1f5f9;
        margin-bottom: 25px;
    }

    .brand-title-main {
        font-size: 3.2rem;
        font-weight: 800;
        color: #1e293b; /* Nero / Antracite */
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }

    .brand-title-main span {
        color: #f97316; /* Arancione coordinato al carrello del logo */
    }

    .brand-subtitle-main {
        font-size: 1.15rem;
        color: #64748b;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Sezione Farmacie con Loghi reali */
    .partner-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .logo-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 65px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .logo-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        border-color: #f97316;
    }

    .logo-card img {
        max-height: 42px;
        max-width: 90%;
        object-fit: contain;
    }

    /* Card Risultati */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        text-align: center;
    }

    .result-card.first {
        border: 2px solid #f97316;
        background: #fffbf7;
        box-shadow: 0 8px 20px rgba(249, 115, 22, 0.12);
    }

    .badge-rank {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .badge-rank.gold { background-color: #fef3c7; color: #92400e; }
    .badge-rank.silver { background-color: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background-color: #ffedd5; color: #9a3412; }

    .price-tag {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin: 10px 0;
    }

    .ship-badge {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
    }

    /* Bottone Principale Arancione */
    .stButton>button[kind="primary"] {
        background-color: #f97316 !important;
        border-color: #f97316 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Mappa Farmacie + URL Loghi reali
FARMACIE = {
    "Farmacia Igea": {
        "spedizione_base": 4.90, "soglia_gratis": 29.00, "url": "https://www.farmaciaigea.com",
        "logo": "https://www.farmaciaigea.com/img/farmacia-igea-logo-1621255554.jpg"
    },
    "Farmaè": {
        "spedizione_base": 3.90, "soglia_gratis": 19.90, "url": "https://www.farmae.it",
        "logo": "https://www.farmae.it/media/logo/default/farmae_logo.png"
    },
    "Dr Max": {
        "spedizione_base": 4.50, "soglia_gratis": 24.90, "url": "https://www.drmax.it",
        "logo": "https://www.drmax.it/static/version1710323315/frontend/DrMax/default/it_IT/images/logo.svg"
    },
    "RedCare": {
        "spedizione_base": 3.95, "soglia_gratis": 18.00, "url": "https://www.redcare.it",
        "logo": "https://www.redcare.it/assets/images/redcare-logo.svg"
    },
    "Farmacia Loreto": {
        "spedizione_base": 4.90, "soglia_gratis": 29.90, "url": "https://farmacialoreto.it",
        "logo": "https://farmacialoreto.it/img/farmacia-loreto-gallo-logo-1663162703.jpg"
    },
    "1000Farmacie": {
        "spedizione_base": 2.90, "soglia_gratis": 29.00, "url": "https://www.1000farmacie.it",
        "logo": "https://www.1000farmacie.it/images/logo.svg"
    },
    "Top Farmacia": {
        "spedizione_base": 4.90, "soglia_gratis": 19.90, "url": "https://www.topfarmacia.it",
        "logo": "https://www.topfarmacia.it/img/top-farmacia-logo-1563287611.jpg"
    },
    "eFarma": {
        "spedizione_base": 4.90, "soglia_gratis": 29.90, "url": "https://www.efarma.com",
        "logo": "https://www.efarma.com/media/logo/default/efarma_logo.png"
    },
    "Farmacosmo": {
        "spedizione_base": 3.90, "soglia_gratis": 29.90, "url": "https://www.farmacosmo.it",
        "logo": "https://www.farmacosmo.it/img/farmacosmo-logo-1588673738.jpg"
    }
}

# 4. Controllo del Logo Locale
logo_filename = None
for name in ["logo_comparacarrello.jpg", "logo_comparacarrello.png", "logo.jpg", "logo.png"]:
    if os.path.exists(name):
        logo_filename = name
        break

# 5. Header Grande con Logo in Evidenza e Titolo Abbinato
col_logo, col_title = st.columns([1, 4], vertical_alignment="center")

with col_logo:
    if logo_filename:
        # Mostra il tuo logo bello GRANDE (larghezza 220px)
        st.image(logo_filename, width=220)
    else:
        st.write("🛒")

with col_title:
    st.markdown("""
    <div>
        <h1 class="brand-title-main">Compara<span>carrello.it</span></h1>
        <p class="brand-subtitle-main">Confronta il prezzo totale della tua spesa nelle migliori farmacie online d'Italia.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Griglia Loghi Farmacie Partner Reali
st.markdown('<div class="partner-label">Farmacie Online Monitorate in Tempo Reale:</div>', unsafe_allow_html=True)

cols = st.columns(len(FARMACIE))
for idx, (nome, info) in enumerate(FARMACIE.items()):
    with cols[idx]:
        st.markdown(f"""
        <div class="logo-card" title="{nome}">
            <img src="{info['logo']}" alt="{nome}" onerror="this.style.display='none'; this.parentNode.innerText='{nome}';">
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 7. Caricamento Dati CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("prodotti_1000_minsan.csv")
        df['MINSAN'] = df['MINSAN'].astype(str)
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del file prodotti_1000_minsan.csv: {e}")
        return pd.DataFrame()

df_prodotti = load_data()

# 8. Session State Carrello
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# 9. Cerca e Aggiungi Prodotto
st.subheader("🔍 Cerca e Aggiungi Prodotti al Carrello")

if not df_prodotti.empty:
    col_cat, col_search = st.columns([1, 2])
    
    with col_cat:
        categorie = ["Tutte"] + sorted(list(df_prodotti['Categoria'].dropna().unique()))
        cat_selezionata = st.selectbox("Categoria:", categorie)
    
    df_filtrato = df_prodotti if cat_selezionata == "Tutte" else df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
    
    with col_search:
        opzioni = df_filtrato.apply(lambda row: f"{row['Prodotto']} | MINSAN: {row['MINSAN']}", axis=1).tolist()
        prod_selezionato = st.selectbox("Cerca prodotto (Nome o MINSAN):", [""] + opzioni)

    if prod_selezionato:
        minsan_sel = prod_selezionato.split("MINSAN: ")[-1]
        row_prod = df_prodotti[df_prodotti['MINSAN'] == minsan_sel].iloc[0]
        
        c_info, c_btn = st.columns([3, 1], vertical_alignment="center")
        with c_info:
            st.info(f"📌 **{row_prod['Prodotto']}** (MINSAN: `{row_prod['MINSAN']}`)")
        with c_btn:
            if st.button("➕ Aggiungi al Carrello", use_container_width=True, type="primary"):
                st.session_state.carrello.append(row_prod)
                st.success("Aggiunto!")
                st.rerun()

# 10. Carrello Utente
st.markdown("---")
st.subheader("🛍️ Articoli nel tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c1, c2 = st.columns([4, 1], vertical_alignment="center")
        with c1:
            st.write(f"📦 **{item['Prodotto']}** *(MINSAN: {item['MINSAN']})*")
        with c2:
            if st.button("❌ Rimuovi", key=f"del_{idx}"):
                st.session_state.carrello.pop(idx)
                st.rerun()
                
    if st.button("🗑️ Svuota tutto il carrello"):
        st.session_state.carrello = []
        st.rerun()
else:
    st.write("Il tuo carrello è vuoto. Cerca un prodotto per iniziare la comparazione.")

# 11. Algoritmo di Comparazione Totale
if st.session_state.carrello:
    st.markdown("---")
    st.subheader("🛒 Risultato Comparazione Carrello")
    
    risultati = []
    
    for farmacia, info in FARMACIE.items():
        totale_prodotti = 0
        disponibili = 0
        
        for item in st.session_state.carrello:
            if farmacia in item and pd.notna(item[farmacia]):
                totale_prodotti += float(item[farmacia])
                disponibili += 1
                
        if disponibili == len(st.session_state.carrello):
            spese_spedizione = 0.0 if totale_prodotti >= info['soglia_gratis'] else info['spedizione_base']
            mancante_gratis = max(0.0, info['soglia_gratis'] - totale_prodotti)
            totale_complessivo = totale_prodotti + spese_spedizione
            
            risultati.append({
                "farmacia": farmacia,
                "totale_prodotti": totale_prodotti,
                "spese_spedizione": spese_spedizione,
                "totale_complessivo": totale_complessivo,
                "mancante_gratis": mancante_gratis,
                "url": info['url']
            })
            
    risultati = sorted(risultati, key=lambda x: x['totale_complessivo'])
    
    if risultati:
        # Podio Top 3
        cols_podium = st.columns(min(3, len(risultati)))
        badges = [("1° Posto - Più Economico", "gold", "first"), ("2° Posto", "silver", "second"), ("3° Posto", "bronze", "third")]
        
        for i in range(min(3, len(risultati))):
            res = risultati[i]
            rank_label, badge_color, card_class = badges[i]
            
            with cols_podium[i]:
                st.markdown(f"""
                <div class="result-card {card_class}">
                    <span class="badge-rank {badge_color}">{rank_label}</span><br>
                    <h3 style="margin: 8px 0; color: #1e293b; font-size: 1.4rem;">{res['farmacia']}</h3>
                    <div class="price-tag">€ {res['totale_complessivo']:.2f}</div>
                    <small style="color: #64748b;">Prodotti: € {res['totale_prodotti']:.2f} | Sped: € {res['spese_spedizione']:.2f}</small><br>
                    {"<div class='ship-badge'>🚚 +€ " + f"{res['mancante_gratis']:.2f}" + " per Sped. GRATIS</div>" if res['mancante_gratis'] > 0 else "<div class='ship-badge' style='background:#dcfce7;color:#166534;'>🎉 Spedizione GRATUITA</div>"}
                    <br><br>
                    <a href="{res['url']}" target="_blank" style="text-decoration:none;">
                        <button style="width:100%; background-color:#f97316; color:white; border:none; padding:12px; border-radius:10px; font-weight:700; cursor:pointer;">
                            🛒 Vai allo Store
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
        # Tabella Classifica Completa
        with st.expander("📊 Guarda la classifica completa di tutte le farmacie"):
            df_res = pd.DataFrame(risultati)[['farmacia', 'totale_prodotti', 'spese_spedizione', 'totale_complessivo']]
            df_res.columns = ['Farmacia', 'Totale Prodotti (€)', 'Spedizioni (€)', 'Totale Carrello (€)']
            st.dataframe(df_res.style.format({'Totale Prodotti (€)': '{:.2f}', 'Spedizioni (€)': '{:.2f}', 'Totale Carrello (€)': '{:.2f}'}), use_container_width=True)

# 12. Footer e Condivisione
st.markdown("---")
c_share1, c_share2 = st.columns(2)
with c_share1:
    st.subheader("💬 Condividi Comparacarrello.it")
    st.markdown("[📲 Condividi su WhatsApp](https://api.whatsapp.com/send?text=Confronta%20il%20prezzo%20della%20tua%20spesa%20in%20farmacia%20su%20https://comparacarrello.streamlit.app)")
with c_share2:
    st.subheader("📱 QR Code App")
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://comparacarrello.streamlit.app", width=130)
