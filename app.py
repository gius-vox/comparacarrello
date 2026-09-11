import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparacarrello.it", page_icon="💊", layout="wide")

# Database ufficiale delle farmacie con loghi e link
FARMACIE_INFO = {
    "Farmacia Igea": {"logo": "https://www.google.com/s2/favicons?domain=farmaciaigea.com&sz=64", "url": "https://www.farmaciaigea.com"},
    "Farmaè": {"logo": "https://www.google.com/s2/favicons?domain=farmae.it&sz=64", "url": "https://www.farmae.it"},
    "Dr Max": {"logo": "https://www.google.com/s2/favicons?domain=drmax.it&sz=64", "url": "https://www.drmax.it"},
    "RedCare": {"logo": "https://www.google.com/s2/favicons?domain=redcare.it&sz=64", "url": "https://www.redcare.it"},
    "Farmacia Loreto": {"logo": "https://www.google.com/s2/favicons?domain=farmacialoreto.it&sz=64", "url": "https://www.farmacialoreto.it"},
    "1000Farmacie": {"logo": "https://www.google.com/s2/favicons?domain=1000farmacie.it&sz=64", "url": "https://www.1000farmacie.it"},
    "Top Farmacia": {"logo": "https://www.google.com/s2/favicons?domain=topfarmacia.it&sz=64", "url": "https://www.topfarmacia.it"},
    "eFarma": {"logo": "https://www.google.com/s2/favicons?domain=efarma.com&sz=64", "url": "https://www.efarma.com"}
}

# Caricamento del file CSV dei prodotti
df = pd.read_csv("prodotti.csv")

# Interfaccia grafica principale
st.image("logo.png", width=150)
st.markdown("<h3 style='text-align: center;'>Trova la farmacia online più conveniente per il tuo carrello</h3>", unsafe_allow_html=True)

# Filtro per categoria
if "Categoria" in df.columns:
    categorie = ["Tutte le Categorie"] + sorted(df["Categoria"].dropna().unique().tolist())
    categoria_selezionata = st.selectbox("📂 Filtra per Categoria:", categorie)
    if categoria_selezionata != "Tutte le Categorie":
        df_filtrato = df[df["Categoria"] == categoria_selezionata]
    else:
        df_filtrato = df
else:
    df_filtrato = df

# Gestione dello stato del carrello
if "carrello" not in st.session_state:
    st.session_state.carrello = {}

# Selezione del prodotto
prodotti_disponibili = df_filtrato["Prodotto"].tolist() if "Prodotto" in df_filtrato.columns else []
prodotto_scelto = st.selectbox("Seleziona un prodotto:", prodotti_disponibili)

col_1, col_2 = st.columns([3, 1])

with col_1:
    if prodotto_scelto:
        riga_prodotto = df_filtrato[df_filtrato["Prodotto"] == prodotto_scelto].iloc[0]
        st.write(f"**Prodotto:** {riga_prodotto.get('Prodotto', '')} — **MINSAN:** {riga_prodotto.get('MINSAN', '')}")

with col_2:
    if st.button("➕ Aggiungi al Carrello", type="primary"):
        if prodotto_scelto:
            st.session_state.carrello[prodotto_scelto] = riga_prodotto

if st.button("🗑️ Svuota"):
    st.session_state.carrello.clear()
    st.rerun()

# Mostra i risultati del confronto prezzi per i prodotti nel carrello
if st.session_state.carrello:
    st.markdown("---")
    st.subheader("🛒 Riepilogo Carrello")
    
    totali_farmacie = {farmacia: 0.0 for farmacia in FARMACIE_INFO.keys()}
    
    for prod, dati in st.session_state.carrello.items():
        st.write(f"- {prod}")
        for farmacia in FARMACIE_INFO.keys():
            if farmacia in dati:
                totali_farmacie[farmacia] += float(dati[farmacia])

    st.markdown("### 🏆 Totali per Farmacia")
    for farmacia, totale in sorted(totali_farmacie.items(), key=lambda x: x[1]):
        st.write(f"**{farmacia}**: € {totale:.2f}")
