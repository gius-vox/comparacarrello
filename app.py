import streamlit as st
import pandas as pd

st.set_page_config(page_title="ComparaCarrello.it", page_icon="💊", layout="wide")

# Database ufficiale delle farmacie con loghi e link
FARMACIE_INFO = {
    "Farmacia Igea": {"logo": "https://www.google.com/s2/favicons?domain=farmaciaigea.com&sz=64", "url": "https://www.farmaciaigea.com", "soglia_gratis": 29.90, "costo_sped": 4.90},
    "Farmaè": {"logo": "https://www.google.com/s2/favicons?domain=farmae.it&sz=64", "url": "https://www.farmae.it", "soglia_gratis": 19.90, "costo_sped": 3.90},
    "Dr Max": {"logo": "https://www.google.com/s2/favicons?domain=drmax.it&sz=64", "url": "https://www.drmax.it", "soglia_gratis": 19.90, "costo_sped": 3.90},
    "RedCare": {"logo": "https://www.google.com/s2/favicons?domain=redcare.it&sz=64", "url": "https://www.redcare.it", "soglia_gratis": 18.00, "costo_sped": 3.99},
    "Farmacia Loreto": {"logo": "https://www.google.com/s2/favicons?domain=farmacialoreto.it&sz=64", "url": "https://farmacialoreto.it", "soglia_gratis": 29.90, "costo_sped": 4.90},
    "1000Farmacie": {"logo": "https://www.google.com/s2/favicons?domain=1000farmacie.it&sz=64", "url": "https://www.1000farmacie.it", "soglia_gratis": 29.00, "costo_sped": 4.90},
    "Top Farmacia": {"logo": "https://www.google.com/s2/favicons?domain=topfarmacia.it&sz=64", "url": "https://www.topfarmacia.it", "soglia_gratis": 29.90, "costo_sped": 4.50},
    "eFarma": {"logo": "https://www.google.com/s2/favicons?domain=efarma.com&sz=64", "url": "https://www.efarma.com", "soglia_gratis": 19.90, "costo_sped": 3.90}
}

# Caricamento pulito dal CSV
df = pd.read_csv("prodotti.csv")
products_db = []
for _, row in df.iterrows():
    prezzi = {}
    for farm in FARMACIE_INFO.keys():
        if farm in df.columns:
            prezzi[farm] = float(row[farm])
    products_db.append({
        "id": str(row.get("MINSAN", "")),
        "nome": str(row.get("Prodotto", "")),
        "categoria": str(row.get("Categoria", "Generica")),
        "prezzi": prezzi
    })

# Titolo e Badge superiori
st.markdown("<h1 style='text-align: center;'>💊 ComparaCarrello.it</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Trova la farmacia online più conveniente per il tuo carrello</p>", unsafe_allow_html=True)

badge_items = "".join([f'<div style="display:inline-flex; align-items:center; background:#fff; border:1px solid #cbd5e1; border-radius:20px; padding:6px 14px; margin:4px; font-weight:600; font-size:0.88rem;"><img src="{info["logo"]}" style="width:18px; height:18px; border-radius:50%; margin-right:8px;">{name}</div>' for name, info in FARMACIE_INFO.items()])
st.html(f'<div style="text-align:center; margin-bottom:20px;">{badge_items}</div>')

# Selezione categoria e prodotti
categorie = ["Tutte le Categorie"] + sorted(list(set(p["categoria"] for p in products_db)))
cat_selected = st.selectbox("📁 Filtra per Categoria:", categorie)

prodotti_filtrati = products_db if cat_selected == "Tutte le Categorie" else [p for p in products_db if p["categoria"] == cat_selected]
options_map = {f"{p['nome']} — [{p['id']}]": p for p in prodotti_filtrati}

if "carrello" not in st.session_state:
    st.session_state.carrello = []

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    selected_option = st.selectbox("Seleziona prodotto", options=list(options_map.keys()), label_visibility="collapsed")
with col2:
    if st.button("➕ Aggiungi al Carrello", use_container_width=True, type="primary"):
        st.session_state.carrello.append(options_map[selected_option])
        st.rerun()
with col3:
    if st.button("🗑️ Svuota", use_container_width=True):
        st.session_state.carrello = []
        st.rerun()

# Gestione Carrello e Risultati
if st.session_state.carrello:
    st.markdown("---")
    st.subheader("🛒 Prodotti nel Carrello")
    for idx, item in enumerate(st.session_state.carrello):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.info(f"**{item['nome']}** — `{item['id']}`")
        with c2:
            if st.button("❌ Rimuovi", key=f"del_{idx}"):
                st.session_state.carrello.pop(idx)
                st.rerun()

    st.markdown("---")
    st.subheader("📊 Classifica Risparmio Carrello Completo")

    totals_products = {farm: sum(prod["prezzi"].get(farm, 0.0) for prod in st.session_state.carrello) for farm in FARMACIE_INFO.keys()}
    totals_final = {}
    shipping_details = {}

    for farm, prod_tot in totals_products.items():
        info = FARMACIE_INFO[farm]
        costo_sped = 0.0 if prod_tot >= info["soglia_gratis"] else info["costo_sped"]
        mancanti = 0.0 if prod_tot >= info["soglia_gratis"] else info["soglia_gratis"] - prod_tot
        totals_final[farm] = prod_tot + costo_sped
        shipping_details[farm] = {"costo_sped": costo_sped, "mancanti": mancanti, "soglia": info["soglia_gratis"]}

    sorted_pharmacies = sorted(totals_final.items(), key=lambda x: x[1])
    best_farm, best_price = sorted_pharmacies[0]
    worst_farm, worst_price = sorted_pharmacies[-1]

    m1, m2, m3 = st.columns(3)
    m1.metric("🥇 PIÙ CONVENIENTE", best_farm)
    m2.metric("💰 TOTALE (SPED. INCLUSA)", f"{best_price:.2f} €")
    m3.metric("🔥 RISPARMIO MASSIMO", f"{worst_price - best_price:.2f} €")

    st.markdown("### 🏆 Classifica Farmacie")
    cols_cards = st.columns(3)

    for i, (pharm_name, tot_val) in enumerate(sorted_pharmacies):
        info = FARMACIE_INFO[pharm_name]
        ship_info = shipping_details[pharm_name]
        prod_val = totals_products[pharm_name]
        
        border_style = "border: 2px solid #22c55e; background-color: #f0fdf4;" if i == 0 else "border: 1px solid #e2e8f0; background-color: #ffffff;"
        
        ship_html = '<div style="background:#f8fafc; padding:8px; border-radius:6px; margin-top:10px; font-size:0.85rem; text-align:left; color:#15803d;"><b>🚚 Spedizione GRATUITA!</b></div>' if ship_info["costo_sped"] == 0 else f'<div style="background:#f8fafc; padding:8px; border-radius:6px; margin-top:10px; font-size:0.85rem; text-align:left;"><p style="color:#b91c1c; margin:2px 0;"><b>🚚 Spedizione: +{ship_info["costo_sped"]:.2f} €</b></p><p style="color:#64748b; margin:2px 0;">Soglia gratuita: {ship_info["soglia"]:.2f} €</p><p style="color:#d97706; margin:2px 0;"><b>⚠️ Mancano {ship_info["mancanti"]:.2f} €</b></p></div>'

        card_html = f'''
        <div style="border-radius:12px; padding:18px; margin-bottom:15px; {border_style} text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <div style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:10px;">
                <img src="{info["logo"]}" style="width:22px; height:22px; border-radius:50%;">
                <div style="font-size:1.2rem; font-weight:700; color:#0f172a;">{pharm_name}</div>
            </div>
            <div style="font-size:1.8rem; font-weight:800; color:#15803d; margin:8px 0;">{tot_val:.2f} €</div>
            <div style="font-size:0.85rem; color:#64748b;">Prodotti: {prod_val:.2f} €</div>
            {ship_html}
            <a href="{info["url"]}" target="_blank" style="display:block; width:100%; background-color:#2563eb; color:white !important; text-align:center; padding:10px 0; border-radius:8px; font-weight:600; text-decoration:none; margin-top:15px;">🛒 Vai alla Farmacia</a>
        </div>
        '''
        with cols_cards[i % 3]:
            st.html(card_html)
