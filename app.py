import streamlit as st
import pandas as pd
import numpy as np

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello.it - Il tuo risparmio in farmacia",
    page_icon="💊",
    layout="wide"
)

# Custom CSS per uno stile moderno e pulito
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0E1117;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4F4F4F;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 10px;
    }
    .badge-minsan {
        background-color: #E1F5FE;
        color: #0288D1;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("prodotti.csv", dtype={'MINSAN': str})
        # Pulizia colonne farmacie
        fixed_cols = ['MINSAN', 'Prodotto', 'Immagine', 'Categoria']
        pharmacy_cols = [c for c in df.columns if c not in fixed_cols]
        return df, pharmacy_cols
    except Exception as e:
        st.error(f"Errore nel caricamento del database prodotti: {e}")
        return pd.DataFrame(), []

df_prodotti, farmacie_disponibili = load_data()

# Header Principale
st.markdown("<h1 class='main-header'>💊 ComparaCarrello.it</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Confronta i prezzi di farmaci, integratori, fitoterapici e omeopatia sulle migliori farmacie online d'Italia</p>", unsafe_allow_html=True)

if df_prodotti.empty:
    st.warning("Database prodotti in fase di aggiornamento. Riprova tra pochi minuti.")
    st.stop()

# Sidebar per filtri e informazioni
with st.sidebar:
    st.header("🔍 Opzioni e Filtri")
    
    categorie = ["Tutte"] + list(df_prodotti['Categoria'].dropna().unique())
    cat_selezionata = st.selectbox("Filtra per Categoria", categorie)
    
    st.markdown("---")
    st.markdown("### 🏥 Farmacie Monitorate")
    for f in farmacie_disponibili:
        st.markdown(f"- **{f}**")
    
    st.markdown("---")
    st.caption("I prezzi vengono sincronizzati automaticamente tramite codice MINSAN/PARAF ufficiale.")

# Filtraggio dati per categoria
if cat_selezionata != "Tutte":
    df_filtrato = df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
else:
    df_filtrato = df_prodotti

# Selezione Prodotti per il Carrello
st.subheader("🛒 Crea il tuo carrello di confronto")

# Formattazione per la ricerca multi-prodotto (Nome + MINSAN)
def format_func(idx):
    row = df_filtrato.loc[idx]
    minsan_str = f" [MINSAN: {row['MINSAN']}]" if pd.notna(row['MINSAN']) and str(row['MINSAN']).strip() != '' else ""
    return f"{row['Prodotto']}{minsan_str}"

prodotti_selezionati_idx = st.multiselect(
    "Cerca e seleziona uno o più prodotti da inserire nel carrello:",
    options=df_filtrato.index.tolist(),
    format_func=format_func,
    placeholder="Es. Tachipirina, Magnesio Supremo, Arnica..."
)

if prodotti_selezionati_idx:
    df_carrello = df_filtrato.loc[prodotti_selezionati_idx].copy()
    
    st.markdown("---")
    st.subheader("📋 Prodotti nel Carrello")
    
    # Visualizzazione prodotti selezionati
    cols_display = ['MINSAN', 'Prodotto', 'Categoria']
    st.dataframe(
        df_carrello[cols_display],
        use_container_width=True,
        hide_index=True
    )
    
    # Calcolo totale per ogni farmacia
    st.markdown("---")
    st.subheader("📊 Confronto Risparmio Carrello")
    
    totali_farmacie = {}
    for f in farmacie_disponibili:
        # Converte i prezzi in numerico ed effettua la somma
        prezzi = pd.to_numeric(df_carrello[f], errors='coerce')
        if prezzi.notna().all():
            totali_farmacie[f] = prezzi.sum()
        else:
            totali_farmacie[f] = np.nan

    # Rimozione farmacie con prodotti mancanti
    totali_validi = {k: v for k, v in totali_farmacie.items() if not np.isnan(v)}
    
    if totali_validi:
        farmacia_migliore = min(totali_validi, key=totali_validi.get)
        prezzo_min = totali_validi[farmacia_migliore]
        prezzo_max = max(totali_validi.values())
        risparmio_max = prezzo_max - prezzo_min

        # Dashboard Metriche Principali
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🥇 Miglior Farmacia", farmacia_migliore)
        with m2:
            st.metric("💰 Totale Migliore", f"{prezzo_min:.2f} €")
        with m3:
            st.metric("🔥 Risparmio Massimo", f"{risparmio_max:.2f} €")

        st.markdown("### 🏆 Classifica Farmacie per questo Carrello")
        
        # Creazione DF Classifica
        df_classifica = pd.DataFrame(list(totali_validi.items()), columns=['Farmacia', 'Totale Carrello (€)'])
        df_classifica = df_classifica.sort_values(by='Totale Carrello (€)').reset_index(drop=True)
        df_classifica['Totale Carrello (€)'] = df_classifica['Totale Carrello (€)'].map('{:.2f} €'.format)
        
        st.table(df_classifica)
        
    else:
        st.warning("Alcuni prodotti selezionati non sono disponibili contemporaneamente in tutte le farmacie. Consulta la tabella sottostante per i dettagli sui singoli prezzi.")
        
    # Tabella dettagliata per singolo prodotto
    with st.expander("🔍 Mostra dettaglio prezzi per singolo prodotto"):
        st.dataframe(
            df_carrello[['Prodotto'] + farmacie_disponibili],
            use_container_width=True,
            hide_index=True
        )

else:
    st.info("💡 Inizia digitando un prodotto nella barra di ricerca sopra per confrontare i prezzi.")
