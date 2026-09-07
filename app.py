import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - L'algoritmo intelligente per la tua spesa",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato per ottimizzazione Mobile e pulizia interfaccia
st.markdown("""
    <style>
    /* Nasconde menu di debug ed elementi da cantiere */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Previene spezzature brutte del testo del titolo su smartphone */
    .main-title {
        font-size: 1.8rem !important;
        font-weight: 800;
        text-align: center;
        color: #2C3E50;
        margin-top: -20px;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    .main-title span {
        color: #FF6B00;
    }
    
    .subtitle {
        font-size: 0.9rem !important;
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 25px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Riconfigura il contenitore del logo */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    
    /* Footer Professionale Istituzionale */
    .custom-footer {
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        font-size: 0.8rem;
        color: #94A3B8;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione e Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Mostra il logo con dimensione controllata
    st.image("logo.png", use_container_width=True)

st.markdown('<h1 class="main-title">COMPARA<span>CARRELLO</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">L\'ALGORITMO INTELLIGENTE PER LA VOSTRA SPESA ONLINE</p>', unsafe_allow_html=True)

st.divider()

# Area Ricerca
st.subheader("🔍 Cerca prodotti per la tua spesa")

# Esempio di lista prodotti (sostituisci o collega al tuo database/funzione esistente)
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
