import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Comparacarrello.it", page_icon="💊", layout="wide")

# Carica il database dei prodotti con MINSAN
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists("prodotti.csv"):
        return pd.read_csv("prodotti.csv", dtype={"MINSAN": str})
    return pd.DataFrame()

df = load_data()

if os.path.exists("logo.png"):
    st.image("logo.png", width=150)

st.markdown("<h3 style='text-align: center;'>Trova la farmacia online più conveniente per il tuo carrello</h3>", unsafe_allow_html=True)

if not df.empty:
    # Identifica dinamicamente le colonne delle farmacie (escludendo MINSAN, Prodotto, Categoria)
    colonne_fisse = ["MINSAN", "Prodotto", "Categoria"]
    farmacie_cols = [c for c in df.columns if c not in colonne_fisse]

    # Filtro Categoria
    if "Categoria" in df.columns:
        categorie = ["Tutte le Categorie"] + sorted(df["Categoria"].dropna().unique().tolist())
        cat_sel = st.selectbox("📂 Filtra per Categoria:", categorie)
        df_filtrato = df if cat_sel == "Tutte le Categorie" else df[df["Categoria"] == cat_sel]
    else:
        df_filtrato = df

    # Ricerca Prodotto o MINSAN
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

        # Ordina le farmacie per prezzo crescente
        totali_ordinati = sorted(totali.items(), key=lambda x: x[1])

        st.markdown("### 🏆 Podio Farmacie più Convenienti")
        for i, (farmacia, prezzo) in enumerate(totali_ordinati[:3], 1):
            st.success(f"**#{i} {farmacia}**: € {prezzo:.2f}")

        with st.expander("📊 Vedi i prezzi di tutte le altre farmacie"):
            for farmacia, prezzo in totali_ordinati[3:]:
                st.write(f"**{farmacia}**: € {prezzo:.2f}")
else:
    st.error("File prodotti.csv non trovato o vuoto.")
