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

    coord_prix['Prix Gazole'] = carb['Prix Gazole']
    coord_prix['Prix SP95'] = carb['Prix SP95']
    coord_prix['Prix E85'] = carb['Prix E85']
    coord_prix['Prix GPlc'] = carb['Prix GPLc']
    coord_prix['Prix E10'] = carb['Prix E10']
    coord_prix['Prix SP98'] = carb['Prix SP98']


    
    return coord_prix

st.title("Prix des carburants en temps réel")

download_activation = True

coord_prix = preparer_donnees(download_activation)

st.write("Localisez-moi pour trouver les stations :")
loc = streamlit_geolocation()

if loc['latitude'] is None or loc['longitude'] is None:
    st.info("👆 Veuillez cliquer sur le bouton de localisation pour afficher la carte.")
    st.stop()

lat_init = loc['latitude']
long_init = loc['longitude']
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

type_carburant = st.sidebar.selectbox("Carburant", ("Gazole", "SP95", "E85", "GPLc", "E10", "SP98"))

"""nbr_stations = st.number_input(
    "Nombre de stations",
    min_value=1,
    max_value=100,
    value=20,
    step=1
)"""
nbr_stations = 50

rayon_km = st.number_input(
    "Rayon de recherches (en km)",
    min_value=1.0,
    max_value=100.0,
    value=10.0,
    step=1.0
)

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
                       popup = f"{str(coord_prix[f"Prix {type_carburant}"].iloc[i])}€"
                       )).add_to(map_init)
        
        compteur += 1

LocateControl(
    auto_start=True,    
    flyTo=True,        
    keepCurrentZoomLevel=True
).add_to(map_init)
        
#map_dlst
folium_static(map_init, width=800, height=600)
