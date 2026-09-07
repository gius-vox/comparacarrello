import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - L'algoritmo intelligente per la tua spesa",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato per ottimizzazione Mobile e rimozione spazi vuoti
st.markdown("""
    <style>
    /* Nasconde menu di debug ed elementi tecnici */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Riduce lo spazio vuoto in cima alla pagina su mobile */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Struttura Intestazione Compatta (Logo + Titolo) */
    .header-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 5px;
    }
    
    .header-box img {
        height: 45px;
        width: auto;
    }
    
    .main-title {
        font-size: 1.6rem !important;
        font-weight: 800;
        color: #2C3E50;
        margin: 0 !important;
        line-height: 1;
    }
    
    .main-title span {
        color: #FF6B00;
    }
    
    .subtitle {
        font-size: 0.75rem !important;
        text-align: center;
        color: #7F8C8D;
        margin-top: 5px;
        margin-bottom: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Footer Professionale */
    .custom-footer {
        margin-top: 40px;
        padding: 15px;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        font-size: 0.75rem;
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione HTML con Logo e Titolo affiancati (Zero spazi sprecati)
st.markdown("""
    <div class="header-box">
        <img src="app/static/logo.png" onerror="this.src='https://raw.githubusercontent.com/streamlit/streamlit/main/docs/static/logo.png'; this.onerror=null;" style="display:none;">
    </div>
""", unsafe_allow_html=True)

# Visualizzazione Logo e Titolo compatti
col_logo, col_text = st.columns([1, 4])
with col_logo:
    st.image("logo.png", width=65)
with col_text:
    st.markdown('<h1 class="main-title" style="padding-top: 10px;">COMPARA<span>CARRELLO</span></h1>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">L\'ALGORITMO INTELLIGENTE PER LA VOSTRA SPESA ONLINE</p>', unsafe_allow_html=True)

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
        <p><b>Comparacarrello.it</b> — Progetto dimostrativo & Technology Showcase</p>
        <p>© 2026 Tutti i diritti riservati — Contatti Partner: info@comparacarrello.it</p>
    </div>
""", unsafe_allow_html=True)
