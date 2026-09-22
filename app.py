import os
import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURAZIONE DELLA PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Comparacarrello.it - Comparatore Prezzi Farmacie",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. STILI CSS PERSONALIZZATI (UI PROFESSIONALE & MODERNA)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #1e293b; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #0d9488;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0f766e;
        color: white;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. NORMALIZZAZIONE CATEGORIE
# ---------------------------------------------------------
def normalizza_categoria(cat):
    if not isinstance(cat, str):
        return "Farmaci da Banco (SOP/OTC)"
    cat_lower = cat.lower().strip()
    if any(k in cat_lower for k in ["fitoterapia", "omeopatia", "rimedi"]):
        return "Fitoterapia e Omeopatia"
    elif any(k in cat_lower for k in ["integratori", "vitamine", "nutraceutica"]):
        return "Integratori e Vitamine"
    elif any(k in cat_lower for k in ["cosmesi", "dermocosmesi", "bellezza", "viso", "corpo"]):
        return "Cosmesi e Dermocosmesi"
    elif any(k in cat_lower for k in ["veterinaria", "animali", "cane", "gatto"]):
        return "Veterinaria"
    elif any(k in cat_lower for k in ["mamma", "bambino", "infanzia", "neonato"]):
        return "Mamma e Bambino"
    else:
        return "Farmaci da Banco (SOP/OTC)"

# ---------------------------------------------------------
# 4. CARICAMENTO DATI OTTIMIZZATO PER 10.000+ PRODOTTI
# ---------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    for filename in ["prodotti_1000_minsan.csv", "prodotti.csv"]:
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename, dtype=str, on_bad_lines='skip', engine='c')
                df.columns = [c.strip() for c in df.columns]
                df['MINSAN'] = df['MINSAN'].astype(str).str.strip()
                if 'Categoria' not in df.columns:
                    df['Categoria'] = 'Farmaci da Banco (SOP/OTC)'
                else:
                    df['Categoria'] = df['Categoria'].apply(normalizza_categoria)
                return df
            except Exception:
                pass
    return pd.DataFrame()

df_prodotti = load_data()

# ---------------------------------------------------------
# 5. HEADER PRINCIPALE DEL SITO
# ---------------------------------------------------------
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #0d9488; margin-bottom: 5px;'>🛒 Comparacarrello.it</h1>
        <p style='font-size: 1.1rem; color: #64748b;'>Compara i prezzi di oltre 10.000 farmaci e prodotti da banco nelle migliori farmacie online</p>
        <p style='font-size: 0.9rem; color: #94a3b8;'>Calcoliamo in tempo reale il totale del tuo carrello incluse le spese di spedizione</p>
    </div>
""", unsafe_allow_html=True)

# Badge contatore live trasparente per partner e investitori
if not df_prodotti.empty:
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            <span style='background-color: #f1f5f9; color: #334155; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid #e2e8f0;'>
                ✨ Database Attivo: <b>{len(df_prodotti):,}</b> referenze farmaceutiche monitorate
            </span>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. FARMACIE MONITORATE
# ---------------------------------------------------------
FARMACIE_DISPONIBILI = [
    "Farmacia Igea", "Farmaè", "Dr Max", "RedCare", 
    "Farmacia Loreto", "1000Farmacie", "Top Farmacia", "eFarma", "Farmacosmo"
]

st.markdown("""
    <div class='card' style='padding: 12px; margin-bottom: 25px;'>
        <p style='font-size: 0.8rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;'>Farmacie online monitorate in tempo reale</p>
        <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
""", unsafe_allow_html=True)

cols_f = st.columns(len(FARMACIE_DISPONIBILI))
for idx, f_nome in enumerate(FARMACIE_DISPONIBILI):
    with cols_f[idx]:
        st.markdown(f"<span style='font-size: 0.8rem; background: #f8fafc; padding: 4px 8px; border-radius: 6px; border: 1px solid #e2e8f0; display: inline-block;'>🏪 {f_nome}</span>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. GESTIONE STATO DEL CARRELLO
# ---------------------------------------------------------
if 'carrello' not in st.session_state:
    st.session_state.carrello = []

# ---------------------------------------------------------
# 8. SEZIONE DI RICERCA PRODOTTI (INTELLIGENTE E LIBERA)
# ---------------------------------------------------------
st.markdown("### Cerca e aggiungi un prodotto")

if df_prodotti.empty:
    st.error("⚠️ Nessun database prodotti trovato. Esegui lo scraper per popolare il catalogo.")
else:
    cat_selezionata = st.radio(
        "Filtra per Categoria:",
        ["Tutte le Categorie", "Farmaci da Banco (SOP/OTC)", "Integratori e Vitamine", "Fitoterapia e Omeopatia", "Cosmesi e Dermocosmesi", "Veterinaria", "Mamma e Bambino"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if cat_selezionata == "Tutte le Categorie":
        df_filtrato = df_prodotti
        placeholder_txt = "Cerca tra oltre 10.000 prodotti per nome, brand o codice MINSAN..."
    else:
        df_filtrato = df_prodotti[df_prodotti['Categoria'] == cat_selezionata]
        placeholder_txt = f"Cerca in '{cat_selezionata}' per nome farmaco o codice MINSAN..."

    query_testo = st.text_input(
        "Digita il nome del farmaco, brand o codice MINSAN:",
        placeholder=placeholder_txt,
        label_visibility="collapsed"
    )

    prod_selezionato = None
    if query_testo and len(query_testo.strip()) >= 2:
        q = query_testo.strip().lower()
        df_trovati = df_filtrato[
            df_filtrato['Prodotto'].str.lower().str.contains(q, na=False) |
            df_filtrato['MINSAN'].str.contains(q, na=False)
        ]
        
        if not df_trovati.empty:
            opzioni_trovate = df_trovati.apply(lambda row: f"{row['Prodotto']} | MINSAN: {row['MINSAN']}", axis=1).tolist()
            scelta_tendina = st.selectbox("Seleziona il prodotto trovato:", options=opzioni_trovate, index=0)
            if scelta_tendina:
                prod_selezionato = scelta_tendina
        else:
            st.warning("Nessun prodotto trovato con questo termine.")

    if prod_selezionato:
        minsan_estratto = prod_selezionato.split("MINSAN:")[-1].strip()
        riga_prodotto = df_prodotti[df_prodotti['MINSAN'] == minsan_estratto]
        
        if not riga_prodotto.empty:
            p_data = riga_prodotto.iloc[0]
            
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.markdown(f"**📦 {p_data['Prodotto']}**")
                st.caption(f"Categoria: {p_data['Categoria']} | MINSAN: {p_data['MINSAN']}")
            with col_btn:
                if st.button("➕ Aggiungi al carrello", key=f"add_{p_data['MINSAN']}"):
                    gia_presente = any(item['MINSAN'] == p_data['MINSAN'] for item in st.session_state.carrello)
                    if not gia_presente:
                        st.session_state.carrello.append(p_data.to_dict())
                        st.success("Aggiunto!")
                        st.rerun()
                    else:
                        st.info("Il prodotto è già nel carrello.")

# ---------------------------------------------------------
# 9. VISUALIZZAZIONE CARRELLO E COMPARAZIONE PREZZI
# ---------------------------------------------------------
st.markdown("---")
st.markdown("### 🛒 Il tuo Carrello & Comparazione")

if not st.session_state.carrello:
    st.info("Il tuo carrello è vuoto. Cerca e aggiungi almeno un prodotto per comparare i prezzi tra le farmacie online.")
else:
    for idx, item in enumerate(st.session_state.carrello):
        col_c1, col_c2 = st.columns([5, 1])
        with col_c1:
            st.write(f"• **{item['Prodotto']}** (MINSAN: {item['MINSAN']})")
        with col_c2:
            if st.button("🗑️ Rimuovi", key=f"rem_{idx}_{item['MINSAN']}"):
                st.session_state.carrello.pop(idx)
                st.rerun()

    st.markdown("---")
    st.markdown("### 🏆 Risultato Comparazione per Farmacia")
    
    risultati_farmacie = []
    spese_spedizione = {
        "Farmacia Igea": 4.90, "Farmaè": 3.90, "Dr Max": 4.50, "RedCare": 5.00,
        "Farmacia Loreto": 4.90, "1000Farmacie": 3.50, "Top Farmacia": 4.90, "eFarma": 4.50, "Farmacosmo": 4.90
    }

    for farmacia in FARMACIE_DISPONIBILI:
        totale_prodotti = 0.0
        
        for item in st.session_state.carrello:
            prezzo_str = str(item.get(farmacia, "0"))
            try:
                prezzo_num = float(prezzo_str)
                totale_prodotti += prezzo_num
            except ValueError:
                pass
                
        sped = spese_spedizione.get(farmacia, 4.90)
        totale_complessivo = round(totale_prodotti + sped, 2)
        
        risultati_farmacie.append({
            "Farmacia": farmacia,
            "Prodotti (€)": round(totale_prodotti, 2),
            "Spedizione (€)": sped,
            "Totale Complessivo (€)": totale_complessivo
        })

    df_risultati = pd.DataFrame(risultati_farmacie).sort_values(by="Totale Complessivo (€)")
    
    st.dataframe(
        df_risultati.set_index("Farmacia"),
        use_container_width=True
    )

    migliore = df_risultati.iloc[0]
    st.success(f"🎉 **La farmacia più economica per il tuo carrello è {migliore['Farmacia']}** con un totale complessivo di **€ {migliore['Totale Complessivo (€)]:.2f}** (inclusi i costi di spedizione)!")

    if st.button("Svuota Carrello"):
        st.session_state.carrello = []
        st.rerun()
