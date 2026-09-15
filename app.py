# ---------------------------------------------------------
# 11. RISULTATI COMPARAZIONE (PULITI E SENZA BUG DI RENDERING)
# ---------------------------------------------------------
if st.session_state.carrello:
    st.markdown("---")
    st.markdown("### 📊 Risultato Comparazione Spesa Completa")
    
    risultati = []
    lista_minsan = [str(item['MINSAN']) for item in st.session_state.carrello]
    
    for farmacia, info in FARMACIE.items():
        totale_prodotti = 0.0
        disponibili = 0
        
        for item in st.session_state.carrello:
            if farmacia in item and pd.notna(item[farmacia]):
                try:
                    totale_prodotti += float(item[farmacia])
                    disponibili += 1
                except ValueError:
                    pass
                
        if disponibili == len(st.session_state.carrello):
            spese_spedizione = 0.0 if totale_prodotti >= info['soglia_gratis'] else info['spedizione_base']
            mancante_gratis = max(0.0, info['soglia_gratis'] - totale_prodotti)
            totale_complessivo = totale_prodotti + spese_spedizione
            
            primo_minsan = st.session_state.carrello[0]['MINSAN']
            target_url = f"{info['search_url']}{urllib.parse.quote(primo_minsan)}"
            
            risultati.append({
                "farmacia": farmacia,
                "totale_prodotti": totale_prodotti,
                "spese_spedizione": spese_spedizione,
                "soglia_gratis": info['soglia_gratis'],
                "totale_complessivo": totale_complessivo,
                "mancante_gratis": mancante_gratis,
                "url": target_url
            })
            
    risultati = sorted(risultati, key=lambda x: x['totale_complessivo'])
    
    if risultati:
        cols_podium = st.columns(min(3, len(risultati)))
        badges = ["🥇 1° Posto - Più Economico", "🥈 2° Posto", "🥉 3° Posto"]
        
        for i in range(min(3, len(risultati))):
            res = risultati[i]
            
            with cols_podium[i]:
                # Card contenitore
                with st.container(border=True):
                    st.caption(f"**{badges[i]}**")
                    st.subheader(res['farmacia'])
                    
                    # Prezzo Totale in grande
                    st.metric(
                        label="TOTALE SPESA", 
                        value=f"€ {res['totale_complessivo']:.2f}"
                    )
                    
                    st.divider()
                    
                    # Dettaglio sequenziale chiaro
                    st.markdown(f"🛍️ **Prezzo prodotti:** € {res['totale_prodotti']:.2f}")
                    if res['spese_spedizione'] == 0:
                        st.markdown("🚚 **Spedizione:** :green[GRATIS]")
                    else:
                        st.markdown(f"🚚 **Spedizione:** + € {res['spese_spedizione']:.2f}")
                    
                    st.divider()
                    
                    # Box soglia spedizione
                    if res['spese_spedizione'] > 0:
                        st.warning(
                            f"💡 **Soglia spedizione gratis:** Aggiungi ancora **€ {res['mancante_gratis']:.2f}** "
                            f"di prodotti per azzerare la spedizione (soglia a € {res['soglia_gratis']:.2f})."
                        )
                    else:
                        st.success("🎉 **Spedizione gratuita sbloccata!**")
                        
                    # Pulsante e Disclaimer
                    st.link_button(
                        label=f"↗️ Acquista su {res['farmacia']}", 
                        url=res['url'], 
                        type="primary", 
                        use_container_width=True
                    )
                    st.caption("ℹ️ *Verrai reindirizzato sul sito ufficiale della farmacia per selezionare e acquistare i tuoi prodotti.*")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📊 Guarda la classifica completa di tutte le farmacie"):
            df_res = pd.DataFrame(risultati)[['farmacia', 'totale_prodotti', 'spese_spedizione', 'soglia_gratis', 'totale_complessivo']]
            df_res.columns = ['Farmacia', 'Totale Prodotti (€)', 'Spedizioni (€)', 'Soglia Gratis (€)', 'Totale Carrello (€)']
            st.dataframe(df_res.style.format({'Totale Prodotti (€)': '{:.2f}', 'Spedizioni (€)': '{:.2f}', 'Soglia Gratis (€)': '{:.2f}', 'Totale Carrello (€)': '{:.2f}'}), use_container_width=True)
