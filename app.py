import streamlit as st
import pandas as pd
import numpy as np
import os

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello.it - Il tuo risparmio in farmacia",
    page_icon="💊",
    layout="wide"
)

# Custom CSS per uno stile pulito ed eliminazione di stili indesiderati
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #0E1117;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #4F4F4F;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stMetric {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv("prodotti.csv", dtype={'MINSAN': str})
        fixed_cols = ['MINSAN', 'Prodotto', 'Immagine', 'Categoria']
        pharmacy_cols = [c for c in df.columns if c not in fixed_cols]
        return df, pharmacy_cols
    except Exception as e:
        st.error(f"Errore nel caricamento del database prodotti: {e}")
        return pd.DataFrame(), []

df_prodotti, farmacie_disponibili = load_data()

# Logo
if os.path.exists("logo.png"):
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.image("logo.png", use_container_width=True)

# Titolo Principale
st.markdown("<h1 class='main-header'>💊 ComparaCarrello.it</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Confronta i prezzi di farmaci, integratori, fitoterapici e omeopatia sulle migliori farmacie online d'Italia</p>", unsafe_allow_html=True)

if df_prodotti.empty:
    st.warning("Database prodotti in fase di aggiornamento. Riprova tra pochi minuti.")
    st.stop()

# BARRA LATERALE (PULITA)
with st.sidebar:
    st.title("⚙️ Filtri App")
    
    categorie = ["Tutte"] + [str(c) for c in df_prodotti['Categoria'].dropna().unique() if str(c).strip() != ""]
    cat_selezionata = st.selectbox("Seleziona Categoria:", categorie)
    
    st.markdown("---")
    st.subheader("🏥 Farmacie attive")
    for f in farmacie_disponibili:
        st.markdown(f"• **{f}**")
    
    st.markdown("---")
    st.caption("Confronto prezzi in tempo reale via codice MINSAN.")

# Filtro categoria
if cat_selezionata != "Tutte":
    df_filtrato = df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
else:
    df_filtrato = df_prodotti

# Carrello e Ricerca
st.subheader("🛒 Crea il tuo carrello di confronto")

def format_func(idx):
    row = df_filtrato.loc[idx]
    minsan_str = f" [MINSAN: {row['MINSAN']}]" if pd.notna(row['MINSAN']) and str(row['MINSAN']).strip() != '' else ""
    return f"{row['Prodotto']}{minsan_str}"

prodotti_selezionati_idx = st.multiselect(
    "Cerca e seleziona i prodotti:",
    options=df_filtrato.index.tolist(),
    format_func=format_func,
    placeholder="Scrivi qui il nome del prodotto o il codice MINSAN..."
)

if prodotti_selezionati_idx:
    df_carrello = df_filtrato.loc[prodotti_selezionati_idx].copy()
    
    st.markdown("---")
    st.subheader("📋 Prodotti Selezionati")
    st.dataframe(
        df_carrello[['MINSAN', 'Prodotto', 'Categoria']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("📊 Confronto Risparmio Carrello")
    
    totali_farmacie = {}
    for f in farmacie_disponibili:
        prezzi = pd.to_numeric(df_carrello[f], errors='coerce')
        if prezzi.notna().all():
            totali_farmacie[f] = prezzi.sum()
        else:
            totali_farmacie[f] = np.nan

    totali_validi = {k: v for k, v in totali_farmacie.items() if not np.isnan(v)}
    
    if totali_validi:
        farmacia_migliore = min(totali_validi, key=totali_validi.get)
        prezzo_min = totali_validi[farmacia_migliore]
        prezzo_max = max(totali_validi.values())
        risparmio_max = prezzo_max - prezzo_min

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🥇 Miglior Farmacia", farmacia_migliore)
        with m2:
            st.metric("💰 Totale Migliore", f"{prezzo_min:.2f} €")
        with m3:
            st.metric("🔥 Risparmio Massimo", f"{risparmio_max:.2f} €")

        st.markdown("### 🏆 Classifica Farmacie")
        df_classifica = pd.DataFrame(list(totali_validi.items()), columns=['Farmacia', 'Totale Carrello (€)'])
        df_classifica = df_classifica.sort_values(by='Totale Carrello (€)').reset_index(drop=True)
        df_classifica['Totale Carrello (€)'] = df_classifica['Totale Carrello (€)'].map('{:.2f} €'.format)
        
        st.table(df_classifica)
    else:
        st.warning("Alcuni prodotti non sono disponibili in tutte le farmacie contemporaneamente.")
        
    with st.expander("🔍 Mostra dettaglio prezzi per singolo prodotto"):
        st.dataframe(
            df_carrello[['Prodotto'] + farmacie_disponibili],
            use_container_width=True,
            hide_index=True
        )

else:
    st.info("💡 Usa la barra qui sopra per aggiungere prodotti al carrello e confrontare i prezzi.")
