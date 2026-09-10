import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="ComparaCarrello.it - Il tuo risparmio",
    page_icon="💊",
    layout="wide"
)

# ---------------------------------------------------------
# 2. STILI CSS PERSONALIZZATI
# ---------------------------------------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 25px;
    }
    
    .farm-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-bottom: 20px;
    }
    .farm-badge {
        display: inline-flex;
        align-items: center;
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 20px;
        padding: 6px 14px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #334155;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .farm-badge img {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .card-container {
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .card-best {
        border: 2px solid #22c55e !important;
        background-color: #f0fdf4 !important;
    }
    .pharm-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-bottom: 10px;
    }
    .pharm-header img {
        width: 22px;
        height: 22px;
        border-radius: 50%;
    }
    .pharm-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
    }
    .pharm-price {
        font-size: 1.8rem;
        font-weight: 800;
        color: #15803d;
        margin: 8px 0;
    }
    
    .btn-buy {
        display: block;
        width: 100%;
        background-color: #2563eb;
        color: white !important;
        text-align: center;
        padding: 10px 0;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none !important;
        margin-top: 15px;
    }

    .shipping-box {
        background-color: #f8fafc;
        border-radius: 6px;
        padding: 8px;
        margin-top: 10px;
        font-size: 0.85rem;
        text-align: left;
    }
    .shipping-box p {
        margin: 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. DATABASE FARMACIE E LOGHI
# ---------------------------------------------------------
FARMACIE_INFO = {
    "Farmacia Igea": {
        "logo": "https://www.google.com/s2/favicons?domain=farmaciaigea.com&sz=64",
        "url": "https://www.farmaciaigea.com",
        "soglia_gratis": 29.90,
        "costo_sped": 4.90
    },
    "Farmaè": {
        "logo": "https://www.google.com/s2/favicons?domain=farmae.it&sz=64",
        "url": "https://www.farmae.it",
        "soglia_gratis": 19.90,
        "costo_sped": 3.90
    },
    "Dr. Max": {
        "logo": "https://www.google.com/s2/favicons?domain=drmax.it&sz=64",
        "url": "https://www.drmax.it",
        "soglia_gratis": 19.90,
        "costo_sped": 3.90
    },
    "RedCare": {
        "logo": "https://www.google.com/s2/favicons?domain=redcare.it&sz=64",
        "url": "https://www.redcare.it",
        "soglia_gratis": 18.00,
        "costo_sped": 3.99
    },
    "Farmacia Loreto": {
        "logo": "https://www.google.com/s2/favicons?domain=farmacialoreto.it&sz=64",
        "url": "https://farmacialoreto.it",
        "soglia_gratis": 29.90,
        "costo_sped": 4.90
    },
    "1000Farmacie": {
        "logo": "https://www.google.com/s2/favicons?domain=1000farmacie.it&sz=64",
        "url": "https://www.1000farmacie.it",
        "soglia_gratis": 29.00,
        "costo_sped": 4.90
    },
    "Top Farmacia": {
        "logo": "https://www.google.com/s2/favicons?domain=topfarmacia.it&sz=64",
        "url": "https://www.topfarmacia.it",
        "soglia_gratis": 29.90,
        "costo_sped": 4.50
    },
    "eFarma": {
        "logo": "https://www.google.com/s2/favicons?domain=efarma.com&sz=64",
        "url": "https://www.efarma.com",
        "soglia_gratis": 19.90,
        "costo_sped": 3.90
    }
}

# ---------------------------------------------------------
# 4. CARICAMENTO DATI
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return [
        {
            "id": "MINSAN: 900000001",
            "nome": "Magnesio Supremo 150g",
            "categoria": "Integratori",
            "prezzi": {
                "Farmaè": 15.50,
                "Dr. Max": 15.50,
                "eFarma": 15.50,
                "Farmacia Igea": 16.90,
                "RedCare": 17.20,
                "1000Farmacie": 16.50,
                "Farmacia Loreto": 18.00,
                "Top Farmacia": 17.90
            }
        },
        {
            "id": "MINSAN: 029007044",
            "nome": "Tachipirina 500mg 20 Compresse",
            "categoria": "Farmaci da Banco",
            "prezzi": {
                "Farmaè": 5.20,
                "Dr. Max": 4.90,
                "eFarma": 5.10,
                "Farmacia Igea": 5.50,
                "RedCare": 5.30,
                "1000Farmacie": 5.00,
                "Farmacia Loreto": 5.60,
                "Top Farmacia": 5.40
            }
        }
    ]

products_db = load_data()

# ---------------------------------------------------------
# 5. HEADER & BADGE TOP FARMACIE
# ---------------------------------------------------------
st.markdown('<div class="main-title">💊 ComparaCarrello.it</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Trova la farmacia online più conveniente per il tuo carrello</div>', unsafe_allow_html=True)

# Badge farmacie senza andate a capo che rompono l'HTML
badge_items = "".join([f'<div class="farm-badge"><img src="{info["logo"]}"><span>{name}</span></div>' for name, info in FARMACIE_INFO.items()])
badges_html = f'<div class="farm-container">{badge_items}</div>'

st.html(badges_html)

# Filtro Categoria
col_cat1, col_cat2, col_cat3 = st.columns([1, 2, 1])
with col_cat2:
    categorie = ["Tutte le Categorie"] + sorted(list(set(p["categoria"] for p in products_db)))
    cat_selected = st.selectbox("📁 Filtra per Categoria:", categorie)

# ---------------------------------------------------------
# 6. CARRELLO ED INTERFACCIA
# ---------------------------------------------------------
if "carrello" not in st.session_state:
    st.session_state.carrello = []

st.markdown("---")
st.subheader("🔍 Cerca e Aggiungi Prodotti")

prodotti_filtrati = products_db
if cat_selected != "Tutte le Categorie":
    prodotti_filtrati = [p for p in products_db if p["categoria"] == cat_selected]

options_map = {f"{p['nome']} — [{p['id']}]": p for p in prodotti_filtrati}

col_search, col_btn1, col_btn2 = st.columns([3, 1, 1])

with col_search:
    selected_option = st.selectbox(
        "Seleziona o digita un prodotto:",
        options=list(options_map.keys()),
        label_visibility="collapsed"
    )

with col_btn1:
    if st.button("➕ Aggiungi al Carrello", use_container_width=True, type="primary"):
        prod_obj = options_map[selected_option]
        st.session_state.carrello.append(prod_obj)
        st.rerun()

with col_btn2:
    if st.button("🗑️ Svuota Carrello", use_container_width=True):
        st.session_state.carrello = []
        st.rerun()

# Display Prodotti nel Carrello
if st.session_state.carrello:
    st.subheader("🛒 Prodotti nel Carrello")
    for idx, item in enumerate(st.session_state.carrello):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.info(f"**{item['nome']}** &nbsp;&nbsp; `<small>{item['id']}</small>`", icon="📦")
        with c2:
            if st.button("❌ Rimuovi", key=f"del_{idx}"):
                st.session_state.carrello.pop(idx)
                st.rerun()

# ---------------------------------------------------------
# 7. CALCOLO E RISULTATI CLASSIFICA
# ---------------------------------------------------------
if st.session_state.carrello:
    st.markdown("---")
    st.subheader("📊 Classifica Risparmio Carrello Completo")

    totals_products = {farm: 0.0 for farm in FARMACIE_INFO.keys()}
    for prod in st.session_state.carrello:
        for farm in FARMACIE_INFO.keys():
            prezzo = prod["prezzi"].get(farm, 0.0)
            totals_products[farm] += prezzo

    totals_final = {}
    shipping_details = {}

    for farm, prod_tot in totals_products.items():
        info = FARMACIE_INFO[farm]
        if prod_tot >= info["soglia_gratis"]:
            costo_sped = 0.0
            mancanti = 0.0
        else:
            costo_sped = info["costo_sped"]
            mancanti = info["soglia_gratis"] - prod_tot

        totals_final[farm] = prod_tot + costo_sped
        shipping_details[farm] = {
            "costo_sped": costo_sped,
            "mancanti": mancanti,
            "soglia": info["soglia_gratis"]
        }

    sorted_pharmacies = sorted(totals_final.items(), key=lambda x: x[1])
    best_farm, best_price = sorted_pharmacies[0]
    worst_farm, worst_price = sorted_pharmacies[-1]
    max_risparmio = worst_price - best_price

    m1, m2, m3 = st.columns(3)
    m1.metric("🥇 PIÙ CONVENIENTE", best_farm)
    m2.metric("💰 TOTALE (SPED. INCLUSA)", f"{best_price:.2f} €")
    m3.metric("🔥 RISPARMIO MASSIMO", f"{max_risparmio:.2f} €")

    st.markdown("### 🏆 Classifica Farmacie")

    cols_cards = st.columns(3)

    for i, (pharm_name, tot_val) in enumerate(sorted_pharmacies):
        info = FARMACIE_INFO[pharm_name]
        ship_info = shipping_details[pharm_name]
        prod_val = totals_products[pharm_name]
        
        if i == 0:
            badge_html = '<span style="background:#dcfce7; color:#15803d; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.8rem;">🥇 1° Posto</span>'
            card_class = "card-container card-best"
        elif i == 1:
            badge_html = '<span style="background:#f1f5f9; color:#475569; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.8rem;">🥈 2° Posto</span>'
            card_class = "card-container"
        elif i == 2:
            badge_html = '<span style="background:#fef3c7; color:#b45309; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.8rem;">🥉 3° Posto</span>'
            card_class = "card-container"
        else:
            badge_html = f'<span style="background:#f8fafc; color:#64748b; padding:3px 10px; border-radius:12px; font-weight:600; font-size:0.8rem;">#{i+1} Posizione</span>'
            card_class = "card-container"

        if ship_info["costo_sped"] == 0:
            ship_html = '<div class="shipping-box" style="color:#15803d;"><b>🚚 Spedizione GRATUITA!</b></div>'
        else:
            ship_html = f'<div class="shipping-box"><p style="color:#b91c1c;"><b>🚚 Spedizione: +{ship_info["costo_sped"]:.2f} €</b></p><p style="color:#64748b;">Soglia gratuita: {ship_info["soglia"]:.2f} €</p><p style="color:#d97706;"><b>⚠️ Mancano {ship_info["mancanti"]:.2f} €</b></p></div>'

        logo_html = f'<img src="{info["logo"]}">'

        card_content = f'<div class="{card_class}"><div style="text-align:left; margin-bottom:10px;">{badge_html}</div><div class="pharm-header">{logo_html}<div class="pharm-name">{pharm_name}</div></div><div class="pharm-price">{tot_val:.2f} €</div><div style="font-size:0.85rem; color:#64748b;">Prodotti: {prod_val:.2f} €</div>{ship_html}<a href="{info["url"]}" target="_blank" class="btn-buy">🛒 Vai alla Farmacia</a></div>'

        col_idx = i % 3
        with cols_cards[col_idx]:
            st.html(card_content)
