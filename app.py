import streamlit as st
import pandas as pd
import os
import qrcode
from io import BytesIO

st.set_page_config(
    page_title="Comparacarrello.it - Il tuo carrello online più conveniente", 
    page_icon="💊", 
    layout="wide"
)

# CSS Personalizzato di Alto Livello
st.markdown("""
    <style>
    /* Reset & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header & Logo */
    .header-container {
        text-align: center;
        padding: 10px 0 15px 0;
    }
    .header-logo {
        max-width: 140px;
        margin-bottom: 8px;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1rem;
        color: #6B7280;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Top Bar Farmacie Partner */
    .pharmacy-card {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 8px 4px;
        text-align: center;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
        min-height: 60px;
    }
    .pharmacy-card:hover {
        transform: translateY(-2px);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.06);
    }
    .pharmacy-card img {
        width: 22px;
        height: 22px;
        object-fit: contain;
    }
    .pharmacy-card a {
        text-decoration: none;
        color: #374151;
        font-weight: 600;
        font-size: 11px;
    }

    /* Card Podio / Vincitore */
    .podium-box {
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        position: relative;
    }
    .podium-box-gold {
        border: 2px solid #F59E0B;
        background: linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 100%);
    }
    .podium-rank {
        font-size: 1.1rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .podium-rank-gold { color: #D97706; }
    .podium-rank-silver { color: #4B5563; }
    .podium-rank-bronze { color: #B45309; }

    .podium-price {
        font-size: 2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 8px 0;
    }
    .podium-details {
        font-size: 0.88rem;
        color: #4B5563;
        margin-bottom: 12px;
    }
    
    .badge-free {
        background-color: #D1FAE5;
        color: #065F46;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 5px 10px;
        border-radius: 8px;
        display: inline-block;
    }
    .badge-missing {
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 5px 10px;
        border-radius: 8px;
        display: inline-block;
    }
    .btn-store {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #2563EB;
        color: white !important;
        padding: 10px 0;
        border-radius: 8px;
        font-weight: 700;
        text-decoration: none;
        margin-top: 14px;
        font-size: 0.95rem;
        box-shadow: 0px 2px 4px rgba(37,99,235,0.2);
    }
    .btn-store:hover {
        background-color: #1D4ED8;
    }

    /* Tabella / Righe Altre Farmacie */
    .other-row {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .other-title {
        font-weight: 700;
        font-size: 0.98rem;
        color: #1F2937;
    }
    .other-sub {
        font-size: 0.82rem;
        color: #6B7280;
    }
    .other-price {
        font-size: 1.25rem;
        font-weight: 800;
        color: #1E3A8A;
    }
    .btn-store-sm {
        background-color: #F3F4F6;
        color: #374151 !important;
        border: 1px solid #D1D5DB;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        font-size: 0.85rem;
    }

    /* Cart Item Row */
    .cart-row {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Farmacie Partner Info
FARMACIE_INFO = {
    "Farmacia Igea": {"logo": "https://www.google.com/s2/favicons?domain=farmaciaigea.com&sz=64", "url": "https://www.farmaciaigea.com", "sped_base": 4.90, "soglia_gratis": 29.90},
    "Farmaè": {"logo": "https://www.google.com/s2/favicons?domain=farmae.it&sz=64", "url": "https://www.farmae.it", "sped_base": 3.90, "soglia_gratis": 19.90},
    "Dr Max": {"logo": "https://www.google.com/s2/favicons?domain=drmax.it&sz=64", "url": "https://www.drmax.it", "sped_base": 4.50, "soglia_gratis": 19.90},
    "RedCare": {"logo": "https://www.google.com/s2/favicons?domain=redcare.it&sz=64", "url": "https://www.redcare.it", "sped_base": 3.99, "soglia_gratis": 18.00},
    "Farmacia Loreto": {"logo": "https://www.google.com/s2/favicons?domain=farmacialoreto.it&sz=64", "url": "https://www.farmacialoreto.it", "sped_base": 4.90, "soglia_gratis": 29.90},
    "1000Farmacie": {"logo": "https://www.google.com/s2/favicons?domain=1000farmacie.it&sz=64", "url": "https://www.1000farmacie.it", "sped_base": 2.90, "soglia_gratis": 29.00},
    "Top Farmacia": {"logo": "https://www.google.com/s2/favicons?domain=topfarmacia.it&sz=64", "url": "https://www.topfarmacia.it", "sped_base": 4.90, "soglia_gratis": 19.90},
    "eFarma": {"logo": "https://www.google.com/s2/favicons?domain=efarma.com&sz=64", "url": "https://www.efarma.com", "sped_base": 4.90, "soglia_gratis": 29.90},
    "Farmacosmo": {"logo": "https://www.google.com/s2/favicons?domain=farmacosmo.it&sz=64", "url": "https://www.farmacosmo.it", "sped_base": 3.99, "soglia_gratis": 29.90}
}

@st.cache_data(ttl=60)
def load_data():
    for filename in ["prodotti_1000_minsan.csv", "prodotti.csv"]:
        if os.path.exists(filename):
            return pd.read_csv(filename, dtype={"MINSAN": str})
    return pd.DataFrame()

df = load_data()

# Header Elegante e Compatto
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    st.markdown("<div class='main-title'>Comparacarrello.it</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Trova il tuo carrello online più conveniente in un click</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top Bar Farmacie
cols = st.columns(len(FARMACIE_INFO))
for idx, (farmacia, info) in enumerate(FARMACIE_INFO.items()):
    with cols[idx]:
        st.markdown(f"""
            <div class='pharmacy-card'>
                <img src='{info["logo"]}'>
                <a href='{info["url"]}' target='_blank'>{farmacia}</a>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Session State Carrello
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

if not df.empty:
    colonne_fisse = ["MINSAN", "Prodotto", "Categoria"]
    farmacie_cols = [c for c in df.columns if c not in colonne_fisse]

    col_cat, col_prod = st.columns([1, 2])
    
    with col_cat:
        if "Categoria" in df.columns:
            categorie = ["Tutte le Categorie"] + sorted(df["Categoria"].dropna().unique().tolist())
            cat_sel = st.selectbox("📂 Categoria:", categorie)
            df_filtrato = df if cat_sel == "Tutte le Categorie" else df[df["Categoria"] == cat_sel]
        else:
            df_filtrato = df

    with col_prod:
        lista_prodotti = sorted(df_filtrato["Prodotto"].tolist())
        prodotto_scelto = st.selectbox(
            "🔍 Cerca prodotto (Nome o MINSAN):",
            options=lista_prodotti,
            index=None,
            placeholder="-- Inizia a digitare per cercare --"
        )

    # Box Aggiunta al Carrello
    if prodotto_scelto:
        riga = df_filtrato[df_filtrato["Prodotto"] == prodotto_scelto].iloc[0]
        c_info, c_btn = st.columns([3, 1])
        with c_info:
            st.info(f"📌 **{riga['Prodotto']}** | MINSAN: `{riga.get('MINSAN', 'N/D')}`")
        with c_btn:
            if st.button("➕ Aggiungi al Carrello", type="primary", use_container_width=True):
                st.session_state.carrello[prodotto_scelto] = riga
                st.toast(f"Aggiunto al carrello: {prodotto_scelto}", icon="🛒")

    # Gestione Carrello
    if st.session_state.carrello:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🛍️ Articoli nel tuo Carrello")
        
        prod_da_eliminare = None
        for prod_name in list(st.session_state.carrello.keys()):
            c_pname, c_pbtn = st.columns([4, 1])
            with c_pname:
                m_val = st.session_state.carrello[prod_name].get('MINSAN', 'N/D')
                st.markdown(f"📦 **{prod_name}** *(MINSAN: {m_val})*")
            with c_pbtn:
                if st.button("❌ Rimuovi", key=f"del_{prod_name}", use_container_width=True):
                    prod_da_eliminare = prod_name

        if prod_da_eliminare:
            del st.session_state.carrello[prod_da_eliminare]
            st.rerun()

        if st.button("🗑️ Svuota tutto il carrello"):
            st.session_state.carrello.clear()
            st.rerun()

    # Comparatore Prezzi
    if st.session_state.carrello:
        st.markdown("---")
        st.subheader("🛒 Risultato Comparazione Carrello")
        
        totali = {}
        for f in farmacie_cols:
            tot_prodotti = 0.0
            for prod, dati in st.session_state.carrello.items():
                try:
                    tot_prodotti += float(dati[f])
                except (ValueError, TypeError):
                    pass
            
            info_f = FARMACIE_INFO.get(f, {"sped_base": 4.90, "soglia_gratis": 29.90, "url": "#", "logo": ""})
            soglia = info_f["soglia_gratis"]
            
            if tot_prodotti >= soglia or tot_prodotti == 0:
                spedizione = 0.0
                mancanti = 0.0
            else:
                spedizione = info_f["sped_base"]
                mancanti = soglia - tot_prodotti
            
            totali[f] = {
                "prodotti": tot_prodotti,
                "spedizione": spedizione,
                "totale_completo": tot_prodotti + spedizione,
                "soglia_gratis": soglia,
                "mancanti_gratis": mancanti,
                "url": info_f["url"],
                "logo": info_f["logo"]
            }

        totali_ordinati = sorted(totali.items(), key=lambda x: x[1]["totale_completo"])

        # Podio Top 3
        podio_cols = st.columns(3)
        medaglie = [("🥇 1° Posto", "podium-rank-gold", "podium-box-gold"), 
                    ("🥈 2° Posto", "podium-rank-silver", ""), 
                    ("🥉 3° Posto", "podium-rank-bronze", "")]
        
        for i, (farmacia, info) in enumerate(totali_ordinati[:3]):
            rank_label, rank_class, box_class = medaglie[i]
            with podio_cols[i]:
                sped_badge = "<span style='color:#059669; font-weight:700;'>GRATIS</span>" if info["spedizione"] == 0 else f"€ {info['spedizione']:.2f}"
                
                if info["mancanti_gratis"] == 0:
                    badge_html = "<div class='badge-free'>🎉 Spedizione GRATIS!</div>"
                else:
                    badge_html = f"<div class='badge-missing'>🚚 +€ {info['mancanti_gratis']:.2f} per Sped. GRATIS</div>"

                st.markdown(f"""
                    <div class='podium-box {box_class}'>
                        <div class='podium-rank {rank_class}'>{rank_label}</div>
                        <div style='display:flex; align-items:center; gap:8px; margin-top:8px;'>
                            <img src='{info["logo"]}' width='22' height='22'>
                            <strong style='font-size:1.1rem; color:#1F2937;'>{farmacia}</strong>
                        </div>
                        <div class='podium-price'>€ {info['totale_completo']:.2f}</div>
                        <div class='podium-details'>
                            Prodotti: <strong>€ {info['prodotti']:.2f}</strong> | Sped: <strong>{sped_badge}</strong>
                        </div>
                        {badge_html}
                        <a href='{info["url"]}' target='_blank' class='btn-store'>🛒 Vai allo Store</a>
                    </div>
                """, unsafe_allow_html=True)

        # Altre Farmacie
        if len(totali_ordinati) > 3:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📊 Guarda la classifica completa di tutte le farmacie"):
                for farmacia, info in totali_ordinati[3:]:
                    sped_txt = "<span style='color:#059669; font-weight:700;'>GRATIS</span>" if info["spedizione"] == 0 else f"€ {info['spedizione']:.2f}"
                    soglia_info = "<span style='color:#059669;'>Spedizione Gratuita</span>" if info["mancanti_gratis"] == 0 else f"Mancano <strong>€ {info['mancanti_gratis']:.2f}</strong> per spedizione gratis"

                    st.markdown(f"""
                        <div class='other-row'>
                            <div style='display:flex; align-items:center; gap:12px;'>
                                <img src='{info["logo"]}' width='22' height='22'>
                                <div>
                                    <div class='other-title'>{farmacia}</div>
                                    <div class='other-sub'>Prodotti: € {info['prodotti']:.2f} | Spedizione: {sped_txt} • {soglia_info}</div>
                                </div>
                            </div>
                            <div style='display:flex; align-items:center; gap:16px;'>
                                <div class='other-price'>€ {info['totale_completo']:.2f}</div>
                                <a href='{info["url"]}' target='_blank' class='btn-store-sm'>Apri Store</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.markdown("### 💬 Condividi Comparacarrello.it")
    msg_wa = "https://api.whatsapp.com/send?text=Confronta%20i%20prezzi%20delle%20farmacie%20online%20su%20https://comparacarrello.it"
    st.markdown(f"[📲 Condividi su WhatsApp]({msg_wa})", unsafe_allow_html=True)

with f_col2:
    st.markdown("### 📱 QR Code App")
    qr = qrcode.make("https://comparacarrello.it")
    buf = BytesIO()
    qr.save(buf)
    st.image(buf.getvalue(), width=120)
