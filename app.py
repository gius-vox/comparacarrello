import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- CONFIGURAZIONE DELLA PAGINA ---
st.set_page_config(
    page_title="Comparacarrello.it - Comparatore Prezzi Farmacie",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING CSS AVANZATO (DESIGN SYSTEM) ---
st.markdown("""
<style>
    /* Stili generali e sfondi */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Hero section */
    .hero-container {
        background: #ffffff;
        padding: 30px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #eaeaea;
    }
    
    /* Card podio principale (1° e 2° posto) */
    .podium-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }
    
    /* Card delle altre farmacie (uniformate) */
    .other-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        border: 1px solid #eaeaea;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Box avviso spedizione */
    .shipping-alert {
        background-color: #fff9db;
        border-left: 4px solid #f59f00;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 13px;
        color: #5c4100;
        margin: 12px 0;
    }
    
    /* Divisori stilizzati */
    .custom-divider {
        height: 1px;
        background-color: #eaeaea;
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- CONNESSIONE A SUPABASE (UTILIZZA I SEGRETI ORIGINALI DI STREAMLIT) ---
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

@st.cache_resource
def init_connection():
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = init_connection()

# --- DIZIONARIO FARMACIE (PARTNER AWIN & SOGLIE SPEDIZIONE) ---
FARMACIE = {
    "Farmaè": {"soglia": 19.90, "costo_base": 3.90},
    "Farmacia Igea": {"soglia": 29.00, "costo_base": 4.90},
    "1000Farmacie": {"soglia": 39.00, "costo_base": 4.50},
    "Top Farmacia": {"soglia": 29.90, "costo_base": 3.90},
    "eFarma": {"soglia": 29.90, "costo_base": 4.90},
    "Farmacosmo": {"soglia": 49.00, "costo_base": 5.00},
    "Farmacia Loreto": {"soglia": 39.00, "costo_base": 4.90}
}

# --- HEADER / HERO SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 style="color: #ff6b00; margin-bottom: 5px;">🛒 Comparacarrello.it</h1>
    <p style="font-size: 16px; color: #495057; font-weight: 500;">Compara i prezzi dei farmaci e prodotti da banco nelle migliori farmacie online</p>
    <p style="font-size: 13px; color: #868e96;">Calcoliamo in tempo reale il totale del tuo carrello incluse le spese di spedizione</p>
</div>
""", unsafe_allow_html=True)

# --- RECUPERO DATI DA SUPABASE ---
@st.cache_data(ttl=600)
def carica_prodotti():
    if not supabase:
        return pd.DataFrame()
    response = supabase.table("prodotti_farmacia").select("*").execute()
    return pd.DataFrame(response.data)

df_prodotti = carica_prodotti()

if df_prodotti.empty:
    st.warning("⚠️ Nessun prodotto trovato nel database di Supabase. Esegui lo script SQL di popolamento.")
    st.stop()

# --- GESTIONE DEL CARRELLO NELLA SESSIONE ---
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# --- SEZIONE RICERCA PRODOTTI ---
st.markdown("### 🔍 Cerca e aggiungi un prodotto")
search_query = st.text_input("Cerca per nome farmaco o codice MINSAN (es. 'tachipirina', 'boiron'):", "")

prodotti_filtrati = df_prodotti if not search_query else df_prodotti[
    df_prodotti['Prodotto'].str.contains(search_query, case=False, na=False) | 
    df_prodotti['MINSAN'].str.contains(search_query, case=False, na=False)
]

selected_product = st.selectbox(
    "Seleziona il prodotto dai risultati:",
    options=prodotti_filtrati.itertuples(index=False),
    format_func=lambda x: f"{x.Prodotto} | Categoria: {x.Categoria} (MINSAN: {x.MINSAN})"
) if not prodotti_filtrati.empty else None

col_add1, col_add2 = st.columns([1, 4])
with col_add1:
    quantita = st.number_input("Qtà", min_value=1, value=1, step=1)

with col_add2:
    st.write("")
    st.write("")
    if st.button("➕ Aggiungi al carrello", type="primary", use_container_width=True):
        if selected_product:
            st.session_state.carrello.append({
                "MINSAN": selected_product.MINSAN,
                "Prodotto": selected_product.Prodotto,
                "Quantita": quantita,
                "dati": selected_product
            })
            st.success(f"Aggiunto: {selected_product.Prodotto} (x{quantita})")
            st.rerun()

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# --- VISUALIZZAZIONE CARRELLO E COMPARAZIONE ---
st.markdown("### 🛍️ Il tuo carrello")

if not st.session_state.carrello:
    st.info("Il tuo carrello è vuoto. Cerca un prodotto qui sopra per iniziare il confronto prezzi tra le farmacie partner.")
else:
    carrello_df_display = pd.DataFrame([{
        "Prodotto": item["Prodotto"],
        "Quantità": item["Quantita"]
    } for item in st.session_state.carrello])
    st.dataframe(carrello_df_display, use_container_width=True, hide_index=True)

    if st.button("🗑️ Svuota carrello"):
        st.session_state.carrello = []
        st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🏆 Risultati comparazione spesa completa")

    # Calcolo dei totali per ciascuna farmacia
    risultati = []
    for farmacia, info in FARMACIE.items():
        totale_prodotti = 0
        disponibile_per_tutti = True

        for item in st.session_state.carrello:
            row_dict = item["dati"]._asdict()
            prezzo = row_dict.get(farmacia)
            if prezzo is not None and pd.notna(prezzo):
                totale_prodotti += float(prezzo) * item["Quantita"]
            else:
                disponibile_per_tutti = False
                break

        if disponibile_per_tutti and totale_prodotti > 0:
            soglia = info["soglia"]
            costo_base = info["costo_base"]
            spedizione = 0.0 if totale_prodotti >= soglia else costo_base
            totale_carrello = totale_prodotti + spedizione
            mancante_sped = max(0.0, soglia - totale_prodotti)

            risultati.append({
                "Farmacia": farmacia,
                "Totale Prodotti (€)": round(totale_prodotti, 2),
                "Spedizioni (€)": round(spedizione, 2),
                "Totale Carrello (€)": round(totale_carrello, 2),
                "Soglia Gratis (€)": soglia,
                "Mancante Sped Gratis": round(mancante_sped, 2)
            })

    if risultati:
        classifica_df = pd.DataFrame(risultati).sort_values(by="Totale Carrello (€)").reset_index(drop=True)

        # --- PODIO PRINCIPALE (1° e 2° POSTO IN EVIDENZA) ---
        col_1, col_2 = st.columns(2)

        def render_podium_card(row, posizione_str, badge_color):
            mancante = row['Mancante Sped Gratis']
            avviso_html = ""
            if mancante > 0:
                avviso_html = f"""
                <div class="shipping-alert">
                    📦 <b>Vuoi azzerare la spedizione?</b><br>
                    Aggiungi altri <b>€ {mancante:.2f}</b> di prodotti su {row['Farmacia']} per sbloccare la spedizione GRATIS (soglia a € {row['Soglia Gratis (€)']:.2f}).
                </div>
                """
            else:
                avviso_html = """
                <div class="shipping-alert" style="background-color: #ebfbee; border-left-color: #40c057; color: #2b8a3e;">
                    🎉 <b>Spedizione GRATIS sbloccata!</b>
                </div>
                """

            return f"""
            <div class="podium-card" style="border-color: {badge_color};">
                <div style="text-align: center; margin-bottom: 12px;">
                    <span style="background-color: {badge_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                        {posizione_str}
                    </span>
                    <h3 style="margin: 8px 0 0 0; color: #212529;">{row['Farmacia']}</h3>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; color: #495057; margin-bottom: 4px;">
                    <span>Prezzo prodotti:</span>
                    <span><b>€ {row['Totale Prodotti (€)']:.2f}</b></span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; color: #495057; margin-bottom: 8px;">
                    <span>Spese di spedizione:</span>
                    <span>+ € {row['Spedizioni (€)']:.2f}</span>
                </div>
                <hr style="border: none; border-top: 1px dashed #dee2e6; margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 18px; color: #212529; font-weight: bold; margin-bottom: 10px;">
                    <span>TOTALE SPESA:</span>
                    <span style="color: #2b8a3e;">€ {row['Totale Carrello (€)']:.2f}</span>
                </div>
                {avviso_html}
            </div>
            """

        with col_1:
            if len(classifica_df) > 0:
                st.markdown(render_podium_card(classifica_df.iloc[0], "1° POSTO - PIÙ ECONOMICO", "#e67700"), unsafe_allow_html=True)
                st.link_button(f"Acquista su {classifica_df.iloc[0]['Farmacia']}", "#", use_container_width=True)

        with col_2:
            if len(classifica_df) > 1:
                st.markdown(render_podium_card(classifica_df.iloc[1], "2° POSTO", "#adb5bd"), unsafe_allow_html=True)
                st.link_button(f"Acquista su {classifica_df.iloc[1]['Farmacia']}", "#", use_container_width=True)

        # --- CLASSIFICA COMPLETA ALTRE FARMACIE (A SCOMPARSA CON CARD UNIFORMI) ---
        if len(classifica_df) > 2:
            st.write("")
            with st.expander("🔍 Guarda la classifica completa di tutte le altre farmacie"):
                for idx, row in classifica_df.iloc[2:].iterrows():
                    st.markdown(f"""
                    <div class="other-card">
                        <div>
                            <h4 style="margin: 0; color: #212529; font-size: 16px;">{row['Farmacia']}</h4>
                            <p style="margin: 4px 0 0 0; font-size: 13px; color: #6c757d;">
                                Prodotti: € {row['Totale Prodotti (€)']:.2f} | Spedizione: € {row['Spedizioni (€)']:.2f}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 16px; font-weight: bold; color: #2b8a3e;">€ {row['Totale Carrello (€)']:.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button(f"Acquista su {row['Farmacia']}", "#", use_container_width=True)
    else:
        st.info("Nessuna farmacia ha tutti i prodotti selezionati disponibili nel database.")
