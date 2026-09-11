import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Comparacarrello.it", page_icon="💊", layout="wide")

# Configurazione Farmacie con loghi e link ufficiali
FARMACIE_INFO = {
    "Farmacia Igea": {"logo": "https://www.google.com/s2/favicons?domain=farmaciaigea.com&sz=64", "url": "https://www.farmaciaigea.com"},
    "Farmaè": {"logo": "https://www.google.com/s2/favicons?domain=farmae.it&sz=64", "url": "https://www.farmae.it"},
    "Dr Max": {"logo": "https://www.google.com/s2/favicons?domain=drmax.it&sz=64", "url": "https://www.drmax.it"},
    "RedCare": {"logo": "https://www.google.com/s2/favicons?domain=redcare.it&sz=64", "url": "https://www.redcare.it"},
    "Farmacia Loreto": {"logo": "https://www.google.com/s2/favicons?domain=farmacialoreto.it&sz=64", "url": "https://www.farmacialoreto.it"},
    "1000Farmacie": {"logo": "https://www.google.com/s2/favicons?domain=1000farmacie.it&sz=64", "url": "https://www.1000farmacie.it"},
    "Top Farmacia": {"logo": "https://www.google.com/s2/favicons?domain=topfarmacia.it&sz=64", "url": "https://www.topfarmacia.it"},
    "eFarma": {"logo": "https://www.google.com/s2/favicons?domain=efarma.com&sz=64", "url": "https://www.efarma.com"},
    "Farmacosmo": {"logo": "https://www.google.com/s2/favicons?domain=farmacosmo.it&sz=64", "url": "https://www.farmacosmo.it"}
}

@st.cache_data(ttl=60)
def load_data():
    if os.path.exists("prodotti.csv"):
        return pd.read_csv("prodotti.csv", dtype={"MINSAN": str})
    return pd.DataFrame()

df = load_data()

# Header e Logo
if os.path.exists("logo.png"):
    st.image("logo.png", width=150)

st.markdown("<h3 style='text-align: center;'>Trova la farmacia online più conveniente per il tuo carrello</h3>", unsafe_allow_html=True)

# Barra Superiore Loghi Farmacie
cols = st.columns(len(FARMACIE_INFO))
for i, (farmacia, info) in enumerate(FARMACIE_INFO.items()):
    with cols[i]:
        st.markdown(f"""
            <div style="text-align: center; padding: 4px; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 10px;">
                <img src="{info['logo']}" width="20" style="vertical-align: middle; margin-right: 4px;">
                <a href="{info['url']}" target="_blank" style="text-decoration: none; color: #31333F; font-weight: 500; font-size: 13px;">{farmacia}</a>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

if not df.empty:
    colonne_fisse = ["MINSAN", "Prodotto", "Categoria"]
    farmacie_cols = [c for c in df.columns if c not in colonne_fisse]

    # Filtro Categoria
    if "Categoria" in df.columns:
        categorie = ["Tutte le Categorie"] + sorted(df["Categoria"].dropna().unique().tolist())
        cat_sel = st.selectbox("📂 Filtra per Categoria:", categorie)
        df_filtrato = df if cat_sel == "Tutte le Categorie" else df[df["Categoria"] == cat_sel]
    else:
        df_filtrato = df

    # Selezione Prodotto
    prodotto_scelto = st.selectbox("Seleziona o cerca un prodotto (Nome o MINSAN):", df_filtrato["Prodotto"].tolist())

    if "carrello" not in st.session_state:
        st.session_state.carrello = {}

    col1, col2 = st.columns([3, 1])
    with col1:
        if prodotto_scelto:
            riga = df_filtrato[df_filtrato["Prodotto"] == prodotto_scelto].iloc[0]
            st.write(f"**Prodotto:** {riga['Prodotto']} — **MINSAN:** {riga.get('MINSAN', 'N/D')}")

    with col2:
        if st.button("➕ Aggiungi al Carrello", type="primary"):
            if prodotto_scelto:
                st.session_state.carrello[prodotto_scelto] = riga

    if st.button("🗑️ Svuota Carrello"):
        st.session_state.carrello.clear()
        st.rerun()

    # Calcolo Totali e Podio
    if st.session_state.carrello:
        st.markdown("---")
        st.subheader("🛒 Confronto Prezzi Carrello")
        
        totali = {f: 0.0 for f in farmacie_cols}
        for prod, dati in st.session_state.carrello.items():
            for f in farmacie_cols:
                try:
                    totali[f] += float(dati[f])
                except (ValueError, TypeError):
                    pass

        totali_ordinati = sorted(totali.items(), key=lambda x: x[1])

        st.markdown("### 🏆 Podio Farmacie più Convenienti")
        for i, (farmacia, prezzo) in enumerate(totali_ordinati[:3], 1):
            st.success(f"**#{i} {farmacia}**: € {prezzo:.2f}")

        with st.expander("📊 Vedi i prezzi di tutte le altre farmacie"):
            for farmacia, prezzo in totali_ordinati[3:]:
                st.write(f"**{farmacia}**: € {prezzo:.2f}")
else:
    st.error("File prodotti.csv non trovato o vuoto.")
