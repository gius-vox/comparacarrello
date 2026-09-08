import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - Il comparatore per la tua Farmacia Online",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato
st.markdown("""
    <style>
    /* Nasconde elementi tecnici di Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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

# Logo centrato
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.image("logo.png", use_container_width=True)

# Titolo e Sottotitolo
st.markdown('<h1 class="main-title">COMPARA<span>CARRELLO</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">L\'ALGORITMO INTELLIGENTE PER FARMACIE E PARAFARMACIE ONLINE</p>', unsafe_allow_html=True)

st.divider()

# Caricamento del database prodotti.csv
@st.cache_data
def load_data():
    return pd.read_csv("prodotti.csv")

try:
    df = load_data()
    farmacie = ["Farmacia Igea", "Farmacia Loreto", "Farmacie Raven", "Dr. Max"]

    # Selezione Prodotti
    st.subheader("💊 Cerca prodotti per la tua spesa pharma")
    scelti = st.multiselect(
        "Seleziona i farmaci o integratori da confrontare:",
        options=df["Prodotto"].tolist(),
        placeholder="Scegli i prodotti..."
    )

    if scelti:
        df_c = df[df["Prodotto"].isin(scelti)].copy()

        st.markdown("#### 📊 Dettaglio Prezzi Singoli")
        # Mostra tabella senza la colonna URL dell'immagine
        st.dataframe(df_c[["Prodotto"] + farmacie], hide_index=True, use_container_width=True)

        st.divider()
        st.markdown("#### 🚚 Analisi Totali e Spese di Spedizione")

        # Soglie spedizione gratuita per ciascuna farmacia (esempi reali)
        soglie = {
            "Farmacia Igea": {"soglia": 29.90, "costo": 4.50},
            "Farmacia Loreto": {"soglia": 39.90, "costo": 4.90},
            "Farmacie Raven": {"soglia": 29.00, "costo": 3.90},
            "Dr. Max": {"soglia": 19.90, "costo": 3.90}
        }

        totali_finali = {}
        cols = st.columns(len(farmacie))

        for idx, f in enumerate(farmacie):
            tot_prod = df_c[f].sum()
            spes = 0.0 if tot_prod >= soglie[f]["soglia"] else soglie[f]["costo"]
            tot_finale = tot_prod + spes
            totali_finali[f] = tot_finale

            with cols[idx]:
                st.markdown(f"**{f}**")
                st.write(f"Prodotti: {tot_prod:.2f}€")
                st.write(f"Spedizione: {spes:.2f}€")
                st.markdown(f"**TOT: {tot_finale:.2f}€**")

        # Determinazione della farmacia più conveniente
        migliore = min(totali_finali, key=totali_finali.get)
        peggiore = max(totali_finali, key=totali_finali.get)
        risparmio = totali_finali[peggiore] - totali_finali[migliore]

        st.success(f"🏆 Il carrello più conveniente è su **{migliore}** con un risparmio reale di **{risparmio:.2f}€**!")

    else:
        st.info("Seleziona uno o più prodotti per sbloccare il confronto dinamico.")

except Exception as e:
    st.error(f"Errore nel caricamento del file prodotti.csv: {e}")

# Footer Istituzionale
st.markdown("""
    <div class="custom-footer">
        <p><b>Comparacarrello.it</b> — Progetto dimostrativo & Vetrina Tecnologica Pharma</p>
        <p>© 2026 Tutti i diritti riservati — Contatti Partner: info@comparacarrello.it</p>
    </div>
""", unsafe_allow_html=True)
