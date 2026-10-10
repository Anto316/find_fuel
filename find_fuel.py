import pandas as pd
import os
import numpy as np
import folium as fl
from folium.plugins import LocateControl
import streamlit as st
from streamlit_folium import folium_static
from streamlit_geolocation import streamlit_geolocation

@st.cache_data
def preparer_donnees(download_actif):

    url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B"
    # os.chdir(r"/home/antonin/Documents/L2/Projet")


    # carb = pd.read_csv('Donnees/carburant.csv', sep=',', on_bad_lines='skip')
    if (download_actif):
        carb = pd.read_csv(url, sep=';', on_bad_lines='skip')
        carb.to_csv('carb.csv', sep=';', index=False)
    else:
        carb = pd.read_csv('carb.csv', sep=';', on_bad_lines='skip')

    coord_prix = pd.DataFrame()

    coord_prix[0] = pd.to_numeric(carb['latitude'], errors='coerce')
    coord_prix[1] = pd.to_numeric(carb['longitude'], errors='coerce')

    coord_prix[2] = carb['Prix Gazole']
    
    return coord_prix

st.title("Prix des carburants en temps réel")

download_activation = True

coord_prix = preparer_donnees(download_activation)

st.write("Localisez-moi pour trouver les stations :")
loc = streamlit_geolocation()

if loc['latitude'] is not None:
    lat_init = loc['latitude']
    long_init = loc['longitude']
    st.stop()
    # st.success(f"Position trouvée : {lat_init}, {long_init}")
#else :
 #   lat_init = 45.1916697
  #  long_init = 5.7652909


map_init = fl.Map(
    location=[lat_init, long_init],
    zoom_start=12
)

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
                       popup = str(coord_prix.iloc[i,2]) + " €"
                       )).add_to(map_init)
        
        compteur += 1

LocateControl(
    auto_start=True,      # Ne lance pas la recherche automatiquement au chargement
    flyTo=True,           # Anime le déplacement vers la position
    keepCurrentZoomLevel=True
).add_to(map_init)
        
#map_dlst
folium_static(map_init, width=800, height=600)
