import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - L'algoritmo intelligente per la tua spesa",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato per forzare il layout compatto su Mobile e Desktop
st.markdown("""
    <style>
    /* Nasconde menu di debug ed elementi tecnici di Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Riduce drasticamente il margine superiore della pagina */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Contenitore Intestazione (Logo + Titolo Affiancati) */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-top: 5px;
        margin-bottom: 5px;
        width: 100%;
    }
    
    .brand-logo {
        width: 55px !important;
        height: auto !important;
        object-fit: contain;
    }
    
    .main-title {
        font-size: 1.5rem !important;
        font-weight: 800;
        color: #2C3E50;
        margin: 0 !important;
        line-height: 1.1;
        white-space: nowrap;
    }
    
    .main-title span {
        color: #FF6B00;
    }
    
    .subtitle {
        font-size: 0.75rem !important;
        text-align: center;
        color: #7F8C8D;
        margin-top: 6px;
        margin-bottom: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Footer Istituzionale */
    .custom-footer {
        margin-top: 30px;
        padding: 15px;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        font-size: 0.75rem;
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione unica in HTML (Forza Logo e Titolo sulla stessa riga)
st.markdown("""
    <div class="brand-header">
        <img src="app/static/logo.png" class="brand-logo" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/streamlit/streamlit/main/docs/static/logo.png';">
        <h1 class="main-title">COMPARA<span>CARRELLO</span></h1>
    </div>
    <p class="subtitle">L'ALGORITMO INTELLIGENTE PER LA VOSTRA SPESA ONLINE</p>
""", unsafe_allow_html=True)

st.divider()

# Area Ricerca
st.subheader("🔍 Cerca prodotti per la tua spesa")

prodotti_disponibili = [
    "Aboca Colilen IBS Colon Irritabile 90 cpr",
    "Latte Parzialmente Scremato 1L",
    "Pasta Barilla Spaghetti n.5 500g",
    "Olio Extravergine d'Oliva 1L",
    "Caffè Lavazza Qualità Rossa 250g"
]

selezione = st.multiselect(
    "Seleziona o digita i prodotti da confrontare:",
    options=prodotti_disponibili,
    placeholder="Scegli i prodotti..."
)

if selezione:
    st.success(f"Hai selezionato {len(selezione)} prodotto/i. Elaborazione confronto in corso...")
    for prod in selezione:
        st.write(f"• **{prod}**")

# Footer Istituzionale
st.markdown("""
    <div class="custom-footer">
        <p><b>Comparacarrello.it</b> — Progetto dimostrativo & Vetrina Tecnologica</p>
        <p>© 2026 Tutti i diritti riservati — Contatti Partner: info@comparacarrello.it</p>
    </div>
""", unsafe_allow_html=True)
