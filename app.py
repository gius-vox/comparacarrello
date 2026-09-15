# ---------------------------------------------------------
# 3. DESIGN SYSTEM - LOGO CENTRATO + BANNER SLOGAN (RESPONSIVE)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    
    /* SEZIONE BRAND CENTRATA IN ALTO */
    .brand-hero-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px 10px;
        background: transparent;
    }

    .brand-hero-logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 6px;
        width: 100%;
    }

    .brand-hero-img {
        height: 65px;
        width: auto;
        object-fit: contain;
    }

    .brand-hero-title {
        font-size: clamp(1.6rem, 6vw, 2.8rem); /* Si ridimensiona automaticamente sui telefoni */
        font-weight: 800;
        color: #047857;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
        white-space: nowrap; /* Impedisce di spezzare la parola a metà */
    }

    .brand-hero-title span {
        color: #ea580c;
    }

    .brand-hero-tagline {
        color: #475569;
        font-size: clamp(0.85rem, 3vw, 1.05rem);
        font-weight: 600;
        margin-top: 6px;
        padding: 0 10px;
    }

    /* BARRA VERDE CON SLOGAN */
    .value-green-bar {
        background: linear-gradient(90deg, #047857 0%, #10b981 100%);
        margin-left: -5rem;
        margin-right: -5rem;
        padding: 12px 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(4, 120, 87, 0.15);
        border-bottom: 3px solid #ea580c;
        margin-bottom: 20px;
        color: #ffffff;
    }

    .value-slogan-main {
        font-size: clamp(0.95rem, 3.5vw, 1.15rem);
        font-weight: 800;
        color: #ffffff;
    }

    .value-slogan-sub {
        font-size: clamp(0.8rem, 2.8vw, 0.95rem);
        font-weight: 600;
        color: #ecfdf5;
        margin-top: 4px;
    }

    /* REGOLE SPECIFICHE PER SMARTPHONE */
    @media (max-width: 640px) {
        .brand-hero-logo-box {
            flex-direction: column; /* Dispone Logo e Titolo in verticale su schermi piccoli */
            gap: 8px;
        }
        .brand-hero-img {
            height: 55px;
        }
        .value-green-bar {
            margin-left: -1rem;
            margin-right: -1rem;
            padding: 10px 10px;
        }
    }

    /* BARRA FARMACIE MONITORATE */
    .pharmacy-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 15px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .pharmacy-bar-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .pharmacy-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        align-items: center;
    }

    .pharmacy-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.78rem;
        color: #334155;
    }
    .pharmacy-chip img {
        width: 14px;
        height: 14px;
        border-radius: 50%;
    }

    /* CARD RISULTATI COMPATTE */
    .result-card {
        background: white;
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.03);
        text-align: center;
    }
    .result-card.first {
        border: 2px solid #ea580c;
        background: #fffbf7;
        box-shadow: 0 6px 16px rgba(234, 88, 12, 0.12);
    }
    .badge-rank {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .badge-rank.gold { background-color: #fef3c7; color: #92400e; }
    .badge-rank.silver { background-color: #f1f5f9; color: #475569; }
    .badge-rank.bronze { background-color: #ffedd5; color: #9a3412; }

    .price-tag {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin: 2px 0;
    }

    .ship-info-box {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 6px;
        margin: 8px 0;
        font-size: 0.75rem;
        color: #475569;
        border: 1px dashed #cbd5e1;
    }

    .ship-badge {
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        display: inline-block;
    }
    .ship-free { background-color: #dcfce7; color: #166534; }
    .ship-paid { background-color: #fef9c3; color: #854d0e; }

    .minsan-tag {
        background-color: #f1f5f9;
        color: #0f766e;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-family: monospace;
        font-weight: 700;
    }

    .stButton>button[kind="primary"] {
        background-color: #ea580c !important;
        border-color: #ea580c !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)
