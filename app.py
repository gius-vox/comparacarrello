import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Comparacarrello.it - Il tuo Carrello Farmacia al Miglior Prezzo",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# STILE CUSTOM
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #e65100;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #555555;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .banner {
        background-color: #00a86b;
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# INTESTAZIONE
st.markdown('<div class="main-header">🛒 Comparacarrello.it</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Il motore di ricerca per la tua spesa in farmacia al miglior prezzo totale</div>', unsafe_allow_html=True)

st.markdown("""
<div class="banner">
    🛒 Con Comparacarrello fare la spesa online è più bello!<br>
    ⚡ Zero stress per la tua scelta, troverai i prodotti giusti ed in fretta!
</div>
""", unsafe_allow_html=True)

# 2. CARICAMENTO DATI ROBUSTO
@st.cache_data
def load_data():
    files_to_try = ["prodotti_1000_minsan.csv", "prodotti.csv"]
    df = None
    
    for file_name in files_to_try:
        if os.path.exists(file_name):
            try:
                # Prova lettura standard CSV
                df = pd.read_csv(file_name, dtype=str)
                break
            except Exception:
                try:
                    # Fallback con separatore o encoding flessibile
                    df = pd.read_csv(file_name, dtype=str, on_bad_lines='skip')
                    break
                except Exception:
                    continue
                    
    if df is None or df.empty:
        return None
        
    # Pulizia nomi colonne
    df.columns = [col.strip() for col in df.columns]
    return df

df = load_data()

# 3. INTERFACCIA E RICERCA
if df is None:
    st.error("⚠️ Impossibile caricare il catalogo prodotti. Verificare la presenza del file 'prodotti_1000_minsan.csv' su GitHub.")
else:
    # ELENCO FARMACIE (Tutte le colonne escluse quelle standard)
    colonne_base = ['MINSAN', 'Prodotto', 'Categoria', 'Immagine_URL']
    farmacie = [c for c in df.columns if c not in colonne_base]
    
    st.caption("**FARMACIE ONLINE MONITORATE IN TEMPO REALE**")
    st.write(" | ".join([f"💊 {f}" for f in farmacie]))
    st.write("---")
    
    st.subheader("🔍 Cerca e aggiungi un prodotto")
    
    # Preparazione lista prodotti per la selezione
    opzioni_prodotti = (df['Prodotto'].fillna('') + " (MINSAN: " + df['MINSAN'].fillna('') + ")").tolist()
    
    prodotto_selezionato = st.selectbox(
        "Digita il nome del prodotto o il codice MINSAN:",
        options=["-- Seleziona un prodotto --"] + opzioni_prodotti,
        index=0
    )
    
    # Inizializzazione Carrello in Session State
    if 'carrello' not in st.session_state:
        st.session_state.carrello = []

    if prodotto_selezionato != "-- Seleziona un prodotto --":
        # Estrai MINSAN tra parentesi
        minsan_sel = prodotto_selezionato.split("MINSAN: ")[-1].replace(")", "").strip()
        riga_prod = df[df['MINSAN'] == minsan_sel]
        
        if not riga_prod.empty:
            prod_dict = riga_prod.iloc[0].to_dict()
            if st.button("➕ Aggiungi al Carrello", type="primary"):
                if minsan_sel not in [p['MINSAN'] for p in st.session_state.carrello]:
                    st.session_state.carrello.append(prod_dict)
                    st.success(f"Aggiunto: {prod_dict['Prodotto']}")
                else:
                    st.warning("Prodotto già presente nel carrello!")

    # 4. MOSTRA CARRELNO E CONFRONTO PREZZI
    st.write("---")
    st.subheader("🛒 Il tuo Carrello")
    
    if not st.session_state.carrello:
        st.info("Il carrello è vuoto. Cerca un prodotto qui sopra per iniziare il confronto.")
    else:
        # Tabella prodotti nel carrello
        for idx, item in enumerate(st.session_state.carrello):
            c1, c2 = st.columns([4, 1])
            c1.write(f"• **{item['Prodotto']}** (MINSAN: {item['MINSAN']})")
            if c2.button("❌ Rimuovi", key=f"del_{idx}"):
                st.session_state.carrello.pop(idx)
                st.rerun()
                
        # Calcolo Totali per Farmacia
        st.write("### 📊 Calcolo e Confronto Prezzi")
        totali = {f: 0.0 for f in farmacie}
        
        for item in st.session_state.carrello:
            for f in farmacie:
                try:
                    val_str = str(item.get(f, '0')).replace(',', '.').strip()
                    totali[f] += float(val_str)
                except ValueError:
                    totali[f] += 0.0
                    
        # Ordina farmacie dalla più conveniente
        totali_ordinati = sorted(totali.items(), key=lambda x: x[1])
        
        # Display Risultati
        for i, (farmacia, prezzo_totale) in enumerate(totali_ordinati):
            if i == 0:
                st.success(f"🏆 **MIGLIOR PREZZO TOTALE: {farmacia}** - € {prezzo_totale:.2f}")
            else:
                st.write(f"• **{farmacia}**: € {prezzo_totale:.2f}")
