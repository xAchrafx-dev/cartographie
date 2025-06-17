
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Titre
st.set_page_config(layout="wide")
st.title("Cartographie interactive des 12 régions du Maroc")
st.markdown("**Données 2024 – CA, VA, LA, RA**")

# Charger les données Excel
df = pd.read_excel("donnees_régions.xlsx")

# Charger le fichier GeoJSON
with open("regions_maroc.json", encoding="utf-8") as f:
    geojson = json.load(f)

# Carte interactive
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Région",
    featureidkey="properties.name",
    color="CA",
    hover_data=["CA", "VA", "LA", "RA"],
    projection="mercator",
    color_continuous_scale="YlGnBu"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

# Sélection et affichage
region_choisie = st.selectbox("Sélectionnez une région :", df["Région"].unique())

st.subheader(f"Indicateurs pour : {region_choisie}")
ligne = df[df["Région"] == region_choisie]
st.dataframe(ligne.reset_index(drop=True))
