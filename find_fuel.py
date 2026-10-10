import pandas as pd
import os
import numpy as np
import folium as fl
from folium.plugins import LocateControl
import streamlit as st
from streamlit_folium import st_folium

st.title("Prix des carburants en temps réel")

print("Dossier de travail actuel :", os.getcwd())
print("Fichiers vus par Jupyter :", os.listdir('.'))
url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B"

# carb = pd.read_csv('Donnees/carburant.csv', sep=',', on_bad_lines='skip')
carb = pd.read_csv(url, sep=';', on_bad_lines='skip')
#carb.to_csv('carb.csv', sep=',', index=False)

# Afficher les 5 premières lignes
print(carb.head())

print(type(carb))
coord_prix = pd.DataFrame()
coord_prix[0] = carb.iloc[: , 1] # On stocke les latitudes
coord_prix[1] = carb.iloc[: , 2] # On stocke les longitudes
coord_prix[2] = carb.iloc[: , 13] # On stocke les prix du gazole
print(coord_prix.head())

lat_init = 45.1916697
long_init = 5.7652909

map_dlst = fl.Map(
    location=[lat_init, long_init],
    zoom_start=15
)

map_dlst = fl.Map(
    location=[lat_init, long_init],
    zoom_start=5
)
map_dlst

nbr_station = len(coord_prix.iloc[: ,0])
compteur = 0
nbr_stations = 20

rayon_km = 10.0
rayon_degré = rayon_km / 111.0

for i in range(nbr_station):
    lat_i = coord_prix.iloc[i,0]
    long_i = coord_prix.iloc[i,1]

    if pd.isna(lat_i) or pd.isna(long_i):
        continue
    
    if (lat_i > 90):
        lat_i = lat_i / 100000
    if (long_i > 90):
        long_i = long_i / 100000
        
    distance = ((long_i - long_init)**2 + (lat_i - lat_init)**2)**(1/2)
    
    if ((distance <= rayon_degré) and (compteur < nbr_stations)):
        (fl.Marker(location = [lat_i, long_i],
                       popup = str(coord_prix.iloc[i,2])
                       )).add_to(map_dlst)
        
        compteur += 1

LocateControl(
    auto_start=True,      # Ne lance pas la recherche automatiquement au chargement
    flyTo=True,           # Anime le déplacement vers la position
    keepCurrentZoomLevel=False
).add_to(map_dlst)
        
#map_dlst
st_folium(map_dlst, width=800, height=600)
