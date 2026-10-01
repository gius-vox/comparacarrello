import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAZIONE DELLA PAGINA & STILE SUPER ---
st.set_page_config(
    page_title="Comparacarrello.it | Il comparatore farmaceutico intelligente",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Iniezione di CSS personalizzato per un look pulito, professionale e di lusso
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1e293b;
        background-color: #f8fafc;
    }

    .main-header {
        background: #ffffff;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    
    .main-header h1 {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        font-size: 1.1rem;
        color: #64748b;
        line-height: 1.6;
    }

    .card-metric {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    /* Stile pulito per i bottoni */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER PROFESSIONALE ---
st.markdown("""
    <div class="main-header">
        <h1>Comparacarrello.it</h1>
        <p>Ottimizza il tuo carrello farmaceutico in tempo reale. Confrontiamo le migliori farmacie online d'Italia per garantirti il massimo risparmio, trasparenza e sicurezza su ogni ordine.</p>
    </div>
""", unsafe_allow_html=True)

# --- SIMULAZIONE DATI (Collegate a Supabase) ---
# Qui sotto la struttura si collega al tuo motore e a Supabase per popolare i dati reali
st.sidebar.markdown("### Area di Gestione")
st.sidebar.info("Connessione attiva a Supabase 🟢")

# Esempio di sezione di ricerca pulita
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Cerca un farmaco o inserisci codice MINSAN")
    search_query = st.text_input("", placeholder="Es. Tachipirina 1000mg o 035672046", label_visibility="collapsed")

with col2:
    st.markdown("### Azioni rapide")
    if st.button("Svuota Carrello", use_container_width=True):
        st.toast("Carrello svuotato con successo.", icon="🧹")

# --- SEZIONE RISULTATI / COMPARAZIONE ---
st.markdown("---")
st.markdown("### Risultati del Confronto in Tempo Reale")

# Tabella dimostrativa pulita in attesa dell'output completo del motore
data_demo = {
    "Farmacia Partner": ["Farmaè", "1000Farmacie", "Top Farmacia", "Amica Farmacia"],
    "Subtotale Prodotti": ["€ 24,50", "€ 23,90", "€ 25,10", "€ 24,00"],
    "Spedizione": ["€ 4,90 (Gratis > 49€)", "€ 3,90 (Gratis > 39€)", "€ 5,90", "€ 4,50"],
    "Totale Ottimizzato": ["€ 29,40", "€ 27,80", "€ 31,00", "€ 28,50"],
}
df_demo = pd.DataFrame(data_demo)

st.dataframe(df_demo, use_container_width=True, hide_index=True)

# Call to Action finale pulita
st.markdown("---")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric(label="Farmacie Monitorate", value="8 Partner")
with col_b:
    st.metric(label="Prezzo Medio Più Basso", value="-18%")
with col_c:
    if st.button("Procedi all'Acquisto Sicuro", type="primary", use_container_width=True):
        st.success("Reindirizzamento protetto verso la farmacia partner...")
