import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - L'algoritmo intelligente per la tua spesa",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato pulito e compatto
st.markdown("""
    <style>
    /* Nasconde elementi tecnici */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Riduce gli spazi vuoti in alto */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    .main-title {
        font-size: 1.8rem !important;
        font-weight: 800;
        text-align: center;
        color: #2C3E50;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
        line-height: 1.1;
    }
    
    .main-title span {
        color: #FF6B00;
    }
    
    .subtitle {
        font-size: 0.8rem !important;
        text-align: center;
        color: #7F8C8D;
        margin-top: 2px;
        margin-bottom: 15px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Centra l'immagine del logo */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: -10px;
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

# Logo fisso ben proporzionato
st.image("logo.png", width=80)

# Titolo e Sottotitolo
st.markdown('<h1 class="main-title">COMPARA<span>CARRELLO</span></h1>', unsafe_allow_html=True)
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
        <p><b>Comparacarrello.it</b> — Progetto dimostrativo & Vetrina Tecnologica</p>
        <p>© 2026 Tutti i diritti riservati — Contatti Partner: info@comparacarrello.it</p>
    </div>
""", unsafe_allow_html=True)
