import streamlit as st
import pandas as pd
import os
import qrcode
from io import BytesIO

st.set_page_config(page_title="Comparacarrello.it", page_icon="💊", layout="wide")

# CSS Personalizzato Avanzato per Card Grafiche, Podio e Layout
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 25px;
    }
    
    /* Top Bar Farmacie */
    .pharmacy-card {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 8px 4px;
        text-align: center;
        background-color: #FFFFFF;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.04);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
        min-height: 65px;
    }
    .pharmacy-card img {
        width: 20px;
        height: 20px;
        object-fit: contain;
    }
    .pharmacy-card a {
        text-decoration: none;
        color: #1F2937;
        font-weight: 600;
        font-size: 11px;
    }

    /* Podium Cards per il Carrello */
    .podium-box {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.06);
        background: #FFFFFF;
        border-left: 6px solid #10B981;
    }
    .podium-rank {
        font-size: 1.2rem;
        font-weight: 800;
        color: #065F46;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .podium-price {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 5px 0;
    }
    .podium-details {
        font-size: 0.9rem;
        color: #4B5563;
    }
    .btn-store {
        display: inline-block;
        background-color: #2563EB;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        margin-top: 8px;
        font-size: 0.9rem;
    }
    .btn-store:hover {
        background-color: #1D4ED8;
    }
    </style>
""", unsafe_allow_html=True)

# Informazioni e loghi delle farmacie
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
    if os.path.exists("prodotti_1000_minsan.csv"):
        return pd.read_csv("prodotti_1000_minsan.csv", dtype={"MINSAN": str})
    elif os.path.exists("prodotti.csv"):
        return pd.read_csv("prodotti.csv", dtype={"MINSAN": str})
    return pd.DataFrame()

df = load_data()

# Header e Logo Principale
c_left, c_mid, c_right = st.columns([1, 2, 1])
with c_mid:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("<div class='main-title'>Comparacarrello.it</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Trova il tuo carrello online più conveniente</div>", unsafe_allow_html=True)

# Barra Superiore con Loghi Farmacie
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

if not df.empty:
    colonne_fisse = ["MINSAN", "Prodotto", "Categoria"]
    farmacie_cols = [c for c in df.columns if c not in colonne_fisse]

    if "Categoria" in df.columns:
        categorie = ["Tutte le Categorie"] + sorted(df["Categoria"].dropna().unique().tolist())
        cat_sel = st.selectbox("📂 Filtra per Categoria:", categorie)
        df_filtrato = df if cat_sel == "Tutte le Categorie" else df[df["Categoria"] == cat_sel]
    else:
        df_filtrato = df

    prodotto_scelto = st.selectbox("🔍 Seleziona o cerca un prodotto (Nome o MINSAN):", df_filtrato["Prodotto"].tolist())

    if "carrello" not in st.session_state:
        st.session_state.carrello = {}

    col1, col2 = st.columns([3, 1])
    with col1:
        if prodotto_scelto:
            riga = df_filtrato[df_filtrato["Prodotto"] == prodotto_scelto].iloc[0]
            st.info(f"**Prodotto selezionato:** {riga['Prodotto']} — **MINSAN:** {riga.get('MINSAN', 'N/D')}")

    with col2:
        if st.button("➕ Aggiungi al Carrello", type="primary", use_container_width=True):
            if prodotto_scelto:
                st.session_state.carrello[prodotto_scelto] = riga

    if st.button("🗑️ Svuota Carrello"):
        st.session_state.carrello.clear()
        st.rerun()

    # Sezione Podio e Comparazione
    if st.session_state.carrello:
        st.markdown("---")
        st.subheader("🛒 Dettaglio Carrello e Comparazione Spedizioni")
        
        totali = {}
        for f in farmacie_cols:
            tot_prodotti = 0.0
            for prod, dati in st.session_state.carrello.items():
                try:
                    tot_prodotti += float(dati[f])
                except (ValueError, TypeError):
                    pass
            
            info_f = FARMACIE_INFO.get(f, {"sped_base": 4.90, "soglia_gratis": 29.90, "url": "#", "logo": ""})
            if tot_prodotti >= info_f["soglia_gratis"] or tot_prodotti == 0:
                spedizione = 0.0
            else:
                spedizione = info_f["sped_base"]
            
            totali[f] = {
                "prodotti": tot_prodotti,
                "spedizione": spedizione,
                "totale_completo": tot_prodotti + spedizione,
                "url": info_f["url"],
                "logo": info_f["logo"]
            }

        totali_ordinati = sorted(totali.items(), key=lambda x: x[1]["totale_completo"])

        st.markdown("### 🏆 Podio Farmacie Più Convenienti")
        
        # Generiamo le Card Podio grafiche
        podio_cols = st.columns(3)
        medaglie = ["🥇 1° Posto", "🥈 2° Posto", "🥉 3° Posto"]
        
        for i, (farmacia, info) in enumerate(totali_ordinati[:3]):
            with podio_cols[i]:
                sped_badge = "<span style='color:#059669; font-weight:bold;'>GRATIS</span>" if info["spedizione"] == 0 else f"€ {info['spedizione']:.2f}"
                st.markdown(f"""
                    <div class='podium-box'>
                        <div class='podium-rank'>{medaglie[i]}</div>
                        <div style='display:flex; align-items:center; gap:8px; margin-top:8px;'>
                            <img src='{info["logo"]}' width='24' height='24'>
                            <strong style='font-size:1.1rem;'>{farmacia}</strong>
                        </div>
                        <div class='podium-price'>€ {info['totale_completo']:.2f}</div>
                        <div class='podium-details'>
                            📦 Prodotti: <strong>€ {info['prodotti']:.2f}</strong><br>
                            🚚 Spedizione: <strong>{sped_badge}</strong>
                        </div>
                        <a href='{info["url"]}' target='_blank' class='btn-store'>🛒 Vai allo Store</a>
                    </div>
                """, unsafe_allow_html=True)

        if len(totali_ordinati) > 3:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📊 Vedi i prezzi di tutte le altre farmacie"):
                for farmacia, info in totali_ordinati[3:]:
                    sped_txt = "GRATIS" if info["spedizione"] == 0 else f"€ {info['spedizione']:.2f}"
                    st.write(f"**{farmacia}**: **€ {info['totale_completo']:.2f}** *(Prodotti: € {info['prodotti']:.2f} | Spedizione: {sped_txt})* — [Apri]({info['url']})")

# Footer Social e QR Code
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
    st.image(buf.getvalue(), width=130)
