

import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Page config
st.set_page_config(page_title="Cartographie Maroc 2024", layout="wide")

st.markdown("""
# 🗺️ Cartographie interactive des 12 régions du **Maroc**
### 📊 Données 2024 : *Chiffre d'affaires (CA), Valeur ajoutée (VA), Liquidité (LA), Résultat (RA)*
""")

# ======= 1. Importation des données Excel ou Google Sheet par défaut =======
uploaded_file = st.file_uploader("📂 Importez votre fichier Excel :", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Fichier importé avec succès.")
else:
    sheet_id = "TON_ID_SHEET"  # Remplace si besoin
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        df = pd.read_csv(sheet_url)
        st.info("ℹ️ Données chargées automatiquement depuis Google Sheets.")
    except:
        st.error("ℹ️ Merci d’importer un fichier.")
        st.stop()

# ======= 2. Chargement GeoJSON =======
with open("regions_maroc.json", encoding="utf-8") as f:
    geojson = json.load(f)

# ======= 3. Indicateur à afficher =======
indicateur = st.selectbox("📌 Choisissez l'indicateur à afficher :", ["CA", "VA", "LA", "RA"])

# ======= 4. Cartes de synthèse =======
st.markdown("## 📑 Totaux nationaux")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 CA total", f"{df['CA'].sum():,.0f} DH")
col2.metric("🏭 VA totale", f"{df['VA'].sum():,.0f} DH")
col3.metric("💧 LA totale", f"{df['LA'].sum():,.0f} DH")
col4.metric("📈 RA total", f"{df['RA'].sum():,.0f} DH")

# ======= 5. Carte interactive =======
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Région",
    featureidkey="properties.name",
    color=indicateur,
    hover_data=["CA", "VA", "LA", "RA"],
    projection="mercator",
    color_continuous_scale="Blues"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=550)
st.plotly_chart(fig, use_container_width=True)

# ======= 6. Répartition camembert =======
st.markdown("## 🥧 Répartition par région")
fig_pie = px.pie(
    df,
    names="Région",
    values=indicateur,
    title=f"Répartition du total national de {indicateur} par région",
    hole=0.4
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie, use_container_width=True)

# ======= 7. Sélection région / affichage détaillé / barres =======
st.markdown("---")
col5, col6 = st.columns([1, 2])

with col5:
    region_choisie = st.selectbox("🔍 Sélectionnez une région :", df["Région"].unique())
    ligne = df[df["Région"] == region_choisie].reset_index(drop=True)
    st.markdown(f"### 📌 Données pour : **{region_choisie}**")
    st.dataframe(ligne)

with col6:
    st.markdown(f"### 📈 Classement des régions par {indicateur}")
    fig_bar = px.bar(
        df.sort_values(indicateur, ascending=False),
        x="Région",
        y=indicateur,
        color=indicateur,
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(height=400, margin={"t":30})
    st.plotly_chart(fig_bar, use_container_width=True)

