import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - Il comparatore per la tua Farmacia Online",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    .main-title {
        font-size: 2rem !important;
        font-weight: 800;
        text-align: center;
        color: #2C3E50;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
    }
    
    .main-title span {
        color: #FF6B00;
    }
    
    .subtitle {
        font-size: 0.85rem !important;
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 20px;
        font-weight: 600;
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

# Logo e Titolo
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    st.image("logo.png", use_container_width=True)

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

    st.subheader("💊 Cerca prodotti per la tua spesa pharma")
    scelti = st.multiselect(
        "Seleziona i farmaci o gli integratori da confrontare:",
        options=df["Prodotto"].tolist(),
        placeholder="Scegli i prodotti..."
    )

    if scelti:
        df_c = df[df["Prodotto"].isin(scelti)].copy()

        st.markdown("#### 📊 Dettaglio Prezzi Singoli")
        st.dataframe(df_c[["Prodotto"] + farmacie], hide_index=True, use_container_width=True)

        st.divider()
        st.markdown("#### 🚚 Analisi Totali e Spese di Spedizione")

        # Regole e Soglie Spedizione Reali
        soglie = {
            "Farmacia Igea": {"soglia": 49.00, "costo": 4.90},
            "Farmacia Loreto": {"soglia": 39.90, "costo": 4.50},
            "Farmacie Raven": {"soglia": 59.00, "costo": 5.90},
            "Dr. Max": {"soglia": 29.90, "costo": 3.90}
        }

        totali_finali = {}
        cols = st.columns(len(farmacie))

        for idx, f in enumerate(farmacie):
            tot_prod = df_c[f].sum()
            soglia_f = soglie[f]["soglia"]
            costo_f = soglie[f]["costo"]
            
            # Calcolo spedizione
            spes = 0.0 if tot_prod >= soglia_f else costo_f
            tot_finale = tot_prod + spes
            totali_finali[f] = tot_finale

            with cols[idx]:
                st.markdown(f"### {f}")
                st.write(f"Prodotti: **{tot_prod:.2f}€**")
                
                if spes == 0:
                    st.write(f"Spedizione: **GRATIS 🎉** *(gratis da {soglia_f:.2f}€)*")
                else:
                    mancanti = soglia_f - tot_prod
                    st.write(f"Spedizione: **+{costo_f:.2f}€ 🎉** *(gratis da {soglia_f:.2f}€ — manca {mancanti:.2f}€)*")
                
                st.markdown(f"### TOTALE: {tot_finale:.2f}€")

        # Verdetto
        migliore = min(totali_finali, key=totali_finali.get)
        peggiore = max(totali_finali, key=totali_finali.get)
        risparmio = totali_finali[peggiore] - totali_finali[migliore]

        st.success(f"🏆 Il carrello più conveniente è su **{migliore}** con un risparmio reale di **{risparmio:.2f}€**!")

    else:
        st.info("Seleziona uno o più prodotti per sbloccare il confronto dinamico.")

except Exception as e:
    st.error(f"Errore nel caricamento del file prodotti.csv: {e}")

# Footer
st.markdown("""
    <div class="custom-footer">
        <p><b>Comparacarrello.it</b> — Progetto dimostrativo & Vetrina Tecnologica Pharma</p>
        <p>© 2026 Tutti i diritti riservati — Contatti Partner: info@comparacarrello.it</p>
    </div>
""", unsafe_allow_html=True)
