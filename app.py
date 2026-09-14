import streamlit as st
import pandas as pd

# 1. Impostazioni della pagina
st.set_page_config(
    page_title="Comparacarrello.it - Risparmia sulla tua spesa in farmacia",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Avanzato per UI/UX di livello E-commerce
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hero Banner Principale */
    .hero-container {
        background: linear-gradient(135deg, #0d324d 0%, #175681 50%, #1d72aa 100%);
        border-radius: 20px;
        padding: 35px 40px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 12px 30px rgba(13, 50, 77, 0.18);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 20px;
    }

    .hero-text {
        flex: 1;
        min-width: 300px;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: #ffffff;
        line-height: 1.2;
    }

    .hero-title span {
        color: #ffcc00;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #e2e8f0;
        margin-top: 10px;
        margin-bottom: 0;
        font-weight: 400;
    }

    .hero-logo-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 15px 25px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-logo-img {
        max-height: 85px;
        width: auto;
        object-fit: contain;
    }

    /* Sezione Brand Farmacie */
    .brand-bar-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 12px;
        text-align: center;
    }

    .brand-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        transition: transform 0.2s ease;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .brand-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .brand-logo {
        max-height: 38px;
        max-width: 90%;
        object-fit: contain;
    }

    /* Modifica stile Card Risultati Comparazione */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        position: relative;
        margin-bottom: 15px;
    }

    .result-card.first {
        border: 2px solid #3b82f6;
        background: linear-gradient(180deg, #ffffff 0%, #eff6ff 100%);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
    }

    .badge-rank {
        display: inline-block;
        padding: 6px 16px;
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

    /* Stile Pulsanti */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Logo e Configurazione Farmacie Partner
LOGO_COMPARA = "https://raw.githubusercontent.com/yfa9374/comparacarrello/main/logo_comparacarrello.jpg"

FARMACIE = {
    "Farmacia Igea": {"logo": "https://www.farmaciaigea.com/img/logo-1603704877.jpg", "spedizione_base": 4.90, "soglia_gratis": 29.00, "url": "https://www.farmaciaigea.com"},
    "Farmaè": {"logo": "https://www.farmae.it/static/version1709123456/frontend/Farmae/default/it_IT/images/logo.svg", "spedizione_base": 3.90, "soglia_gratis": 19.90, "url": "https://www.farmae.it"},
    "Dr Max": {"logo": "https://www.drmax.it/static/version1709123456/frontend/DrMax/default/it_IT/images/logo.svg", "spedizione_base": 4.50, "soglia_gratis": 24.90, "url": "https://www.drmax.it"},
    "RedCare": {"logo": "https://www.redcare.it/images/logo.svg", "spedizione_base": 3.95, "soglia_gratis": 18.00, "url": "https://www.redcare.it"},
    "Farmacia Loreto": {"logo": "https://farmacialoreto.it/image/catalog/logo.png", "spedizione_base": 4.90, "soglia_gratis": 29.90, "url": "https://farmacialoreto.it"},
    "1000Farmacie": {"logo": "https://www.1000farmacie.it/images/logo.svg", "spedizione_base": 2.90, "soglia_gratis": 29.00, "url": "https://www.1000farmacie.it"},
    "Top Farmacia": {"logo": "https://www.topfarmacia.it/pub/static/frontend/Topfarmacia/theme/it_IT/images/logo.svg", "spedizione_base": 4.90, "soglia_gratis": 19.90, "url": "https://www.topfarmacia.it"},
    "eFarma": {"logo": "https://www.efarma.com/static/version1709123456/frontend/Efarma/default/it_IT/images/logo.svg", "spedizione_base": 4.90, "soglia_gratis": 29.90, "url": "https://www.efarma.com"},
    "Farmacosmo": {"logo": "https://www.farmacosmo.it/img/farmacosmo-logo-1614765632.jpg", "spedizione_base": 3.90, "soglia_gratis": 29.90, "url": "https://www.farmacosmo.it"}
}

# 4. Hero Banner Principale
st.markdown(f"""
<div class="hero-container">
    <div class="hero-text">
        <h1 class="hero-title">Comparacarrello<span>.it</span></h1>
        <p class="hero-subtitle">Confronta il prezzo totale del tuo carrello nelle migliori farmacie online d'Italia.</p>
    </div>
    <div class="hero-logo-box">
        <img src="{LOGO_COMPARA}" class="hero-logo-img" alt="Comparacarrello Logo">
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Barra Loghi Farmacie Partner
st.markdown('<div class="brand-bar-title">Farmacie Online Monitorate in Tempo Reale</div>', unsafe_allow_html=True)
cols_brand = st.columns(len(FARMACIE))
for idx, (nome_f, info_f) in enumerate(FARMACIE.items()):
    with cols_brand[idx]:
        st.markdown(f"""
        <div class="brand-card" title="{nome_f}">
            <img src="{info_f['logo']}" class="brand-logo" alt="{nome_f}" onerror="this.onerror=null; this.src='https://via.placeholder.com/120x40?text={nome_f}';">
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Caricamento Dati
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

# 7. Session State Carrello
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# 8. Sezione Cerca e Aggiungi Prodotto
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
        
        c_info, c_btn = st.columns([3, 1])
        with c_info:
            st.info(f"📌 **{row_prod['Prodotto']}** (MINSAN: `{row_prod['MINSAN']}`)")
        with c_btn:
            if st.button("➕ Aggiungi al Carrello", use_container_width=True, type="primary"):
                st.session_state.carrello.append(row_prod)
                st.success("Aggiunto!")
                st.rerun()

# 9. Sezione Carrello Utente
st.markdown("---")
st.subheader("🛍️ Articoli nel tuo Carrello")

if st.session_state.carrello:
    for idx, item in enumerate(st.session_state.carrello):
        c1, c2 = st.columns([4, 1])
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

# 10. Algoritmo di Comparazione Totale
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
                "logo": info['logo'],
                "totale_prodotti": totale_prodotti,
                "spese_spedizione": spese_spedizione,
                "totale_complessivo": totale_complessivo,
                "mancante_gratis": mancante_gratis,
                "url": info['url']
            })
            
    risultati = sorted(risultati, key=lambda x: x['totale_complessivo'])
    
    if risultati:
        # Top 3 Podium Cards
        cols_podium = st.columns(min(3, len(risultati)))
        
        badges = [("1° Posto", "gold", "first"), ("2° Posto", "silver", "second"), ("3° Posto", "bronze", "third")]
        
        for i in range(min(3, len(risultati))):
            res = risultati[i]
            rank_label, badge_color, card_class = badges[i]
            
            with cols_podium[i]:
                st.markdown(f"""
                <div class="result-card {card_class}">
                    <span class="badge-rank {badge_color}">{rank_label}</span><br>
                    <img src="{res['logo']}" style="max-height: 45px; margin: 10px 0;" alt="{res['farmacia']}"><br>
                    <strong style="font-size: 1.1rem; color: #334155;">{res['farmacia']}</strong>
                    <div class="price-tag">€ {res['totale_complessivo']:.2f}</div>
                    <small style="color: #64748b;">Prodotti: € {res['totale_prodotti']:.2f} | Sped: € {res['spese_spedizione']:.2f}</small><br>
                    {"<div class='ship-badge'>🚚 +€ " + f"{res['mancante_gratis']:.2f}" + " per Sped. GRATIS</div>" if res['mancante_gratis'] > 0 else "<div class='ship-badge' style='background:#dcfce7;color:#166534;'>🎉 Spedizione GRATUITA</div>"}
                    <br><br>
                    <a href="{res['url']}" target="_blank" style="text-decoration:none;">
                        <button style="width:100%; background-color:#2563eb; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">
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

# 11. Footer e Condivisione
st.markdown("---")
c_share1, c_share2 = st.columns(2)
with c_share1:
    st.subheader("💬 Condividi Comparacarrello.it")
    st.markdown("[📲 Condividi su WhatsApp](https://api.whatsapp.com/send?text=Confronta%20il%20prezzo%20della%20tua%20spesa%20in%20farmacia%20su%20https://comparacarrello.streamlit.app)")
with c_share2:
    st.subheader("📱 QR Code App")
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://comparacarrello.streamlit.app", width=130)
