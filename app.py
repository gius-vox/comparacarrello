import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(
    page_title="ComparaCarrello - Il comparatore per la tua Farmacia Online",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Personalizzato per Card e Interfaccia Moderna
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
        font-size: 2.2rem !important;
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
        margin-bottom: 25px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Styling Card Farmacie */
    .pharmacy-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    
    .pharmacy-card-best {
        background-color: #F0FDF4;
        border-radius: 12px;
        padding: 18px;
        border: 2px solid #22C55E;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.15);
        text-align: center;
        margin-bottom: 10px;
    }
    
    .badge-best {
        background-color: #22C55E;
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 10px;
    }
    
    .card-price-label {
        font-size: 0.8rem;
        color: #64748B;
    }
    
    .card-shipping {
        font-size: 0.78rem;
        color: #475569;
        margin: 8px 0;
        padding: 6px;
        background-color: #F8FAFC;
        border-radius: 6px;
    }
    
    .card-total {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 10px;
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
        st.markdown("#### 🚚 Confronto Carrelli & Spedizioni")

        # Regole e Soglie Spedizione
        soglie = {
            "Farmacia Igea": {"soglia": 49.00, "costo": 4.90},
            "Farmacia Loreto": {"soglia": 39.90, "costo": 4.50},
            "Farmacie Raven": {"soglia": 59.00, "costo": 5.90},
            "Dr. Max": {"soglia": 29.90, "costo": 3.90}
        }

        # Calcolo Totali
        dati_calcolati = {}
        totali_finali = {}

        for f in farmacie:
            tot_prod = df_c[f].sum()
            soglia_f = soglie[f]["soglia"]
            costo_f = soglie[f]["costo"]
            
            if tot_prod >= soglia_f:
                spes = 0.0
                txt_spes = f"<b>GRATIS 🎉</b> <br><small style='color:#16A34A;'>(soglia {soglia_f:.2f}€ superata)</small>"
            else:
                spes = costo_f
                mancanti = soglia_f - tot_prod
                txt_spes = f"<b>+{costo_f:.2f}€</b> <br><small style='color:#DC2626;'>(mancano {mancanti:.2f}€ per la sped. gratis)</small>"
            
            tot_finale = tot_prod + spes
            totali_finali[f] = tot_finale
            dati_calcolati[f] = {
                "tot_prod": tot_prod,
                "spes": spes,
                "txt_spes": txt_spes,
                "tot_finale": tot_finale
            }

        migliore = min(totali_finali, key=totali_finali.get)
        peggiore = max(totali_finali, key=totali_finali.get)
        risparmio = totali_finali[peggiore] - totali_finali[migliore]

        # Rendering Card Grafiche
        cols = st.columns(len(farmacie))

        for idx, f in enumerate(farmacie):
            d = dati_calcolati[f]
            is_best = (f == migliore)
            
            card_class = "pharmacy-card-best" if is_best else "pharmacy-card"
            badge_html = '<div class="badge-best">🏆 Più Conveniente</div>' if is_best else '<div style="height:21px;"></div>'

            with cols[idx]:
                st.markdown(f"""
                    <div class="{card_class}">
                        {badge_html}
                        <div class="card-title">{f}</div>
                        <div class="card-price-label">Prodotti: <b>{d['tot_prod']:.2f}€</b></div>
                        <div class="card-shipping">{d['txt_spes']}</div>
                        <div class="card-total">TOTALE: {d['tot_finale']:.2f}€</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.success(f"🏆 Il carrello più conveniente è su **{migliore}** con un risparmio reale di **{risparmio:.2f}€** rispetto alla scelta più cara!")

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
