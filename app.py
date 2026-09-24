import streamlit as st
from supabase import create_client, Client

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Comparacarrello", layout="wide")

# Connessione a Supabase usando i Secret di Streamlit/Render
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# Funzione per caricare i prodotti dalla tabella creata prima
@st.cache_data(ttl=600)
def get_prodotti():
    response = supabase.table("prodotti_farmacia").select("*").execute()
    return response.data

st.title("🛒 Comparacarrello.it")
st.write("Connesso al database cloud Supabase in tempo reale!")

# Carichiamo i dati
data = get_prodotti()

if data:
    st.success(f"Caricati con successo {len(data)} prodotti dal database!")
    # Mostriamo la tabella dei prodotti nell'app
    st.dataframe(data)
else:
    st.warning("Nessun prodotto trovato nella tabella.")
