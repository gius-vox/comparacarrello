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

# 2. CSS Custom - Look Moderno, Pulito ed Elegante
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Header e Titolo */
    .brand-title-main {
        font-size: 3rem;
        font-weight: 800;
        color: #1e293b;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }

    .brand-title-main span {
        color: #f97316; /* Arancione del logo */
    }

    .brand-subtitle-main {
        font-size: 1.1rem;
        color: #64748b;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Sezione Farmacie Partner (Griglia Badge Eleganti) */
    .partner-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
        margin-bottom: 25px;
    }

    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 8px 16px;
        border-radius: 50px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
        font-weight: 600;
        font-size: 0.9rem;
        color: #1e293b;
    }

    .pharmacy-chip:hover {
        border-color: #f97316;
        box-shadow: 0 4px 10px rgba(249, 115, 22, 0.15);
        transform: translateY(-2px);
    }

    .pharmacy-chip img {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        object-fit: cover;
    }

    /* Result Cards per il Podio */
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

    .stButton>button[kind="primary"] {
        background-color: #f97316 !important;
        border-color: #f97316 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Mappa Farmacie con domini puliti per icone affidabili
FARMACIE = {
    "Farmacia Igea": {"domain": "farmaciaigea.com", "spedizione_base": 4.90, "soglia_gratis": 29.00, "url": "https://www.farmaciaigea.com"},
    "Farmaè": {"domain": "farmae.it", "spedizione_base": 3.90, "soglia_gratis": 19.90, "url": "https://www.farmae.it"},
    "Dr Max": {"domain": "drmax.it", "spedizione_base": 4.50, "soglia_gratis": 24.90, "url": "https://www.drmax.it"},
    "RedCare": {"domain": "redcare.it", "spedizione_base": 3.95, "soglia_gratis": 18.00, "url": "https://www.redcare.it"},
    "Farmacia Loreto": {"domain": "farmacialoreto.it", "spedizione_base": 4.90, "soglia_gratis": 29.90, "url": "https://farmacialoreto.it"},
    "1000Farmacie": {"domain": "1000farmacie.it", "spedizione_base": 2.90, "soglia_gratis": 29.00, "url": "https://www.1000farmacie.it"},
    "Top Farmacia": {"domain": "topfarmacia.it", "spedizione_base": 4.90, "soglia_gratis": 19.90, "url": "https://www.topfarmacia.it"},
    "eFarma": {"domain": "efarma.com", "spedizione_base": 4.90, "soglia_gratis": 29.90, "url": "https://www.efarma.com"},
    "Farmacosmo": {"domain": "farmacosmo.it", "spedizione_base": 3.90, "soglia_gratis": 29.90, "url": "https://www.farmacosmo.it"}
}

# 4. Controllo del Logo Locale
logo_filename = None
for name in ["logo_comparacarrello.jpg", "logo_comparacarrello.png", "logo.jpg", "logo.png"]:
    if os.path.exists(name):
        logo_filename = name
        break

# 5. Header Principale
col_logo, col_title = st.columns([1, 4], vertical_alignment="center")

with col_logo:
    if logo_filename:
        st.image(logo_filename, width=210)
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

# 6. Sezione Farmacie Online (Chips Eleganti con Favicon Garantite)
st.markdown('<div class="partner-label">Farmacie Online Monitorate in Tempo Reale:</div>', unsafe_allow_html=True)

chips_html = '<div class="pharmacy-grid">'
for nome, info in FARMACIE.items():
    icon_url = f"https://www.google.com/s2/favicons?domain={info['domain']}&sz=64"
    chips_html += f'''
        <div class="pharmacy-chip">
            <img src="{icon_url}" alt="{nome}">
            <span>{nome}</span>
        </div>
    '''
chips_html += '</div>'

st.markdown(chips_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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

# 12. Footer
st.markdown("---")
c_share1, c_share2 = st.columns(2)
with c_share1:
    st.subheader("💬 Condividi Comparacarrello.it")
    st.markdown("[📲 Condividi su WhatsApp](https://api.whatsapp.com/send?text=Confronta%20il%20prezzo%20della%20tua%20spesa%20in%20farmacia%20su%20https://comparacarrello.streamlit.app)")
with c_share2:
    st.subheader("📱 QR Code App")
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://comparacarrello.streamlit.app", width=130)
