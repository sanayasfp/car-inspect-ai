import streamlit as st

st.set_page_config(
    page_title="Car Inspect AI",
    page_icon="🚗",
)


views = lambda x: f"views/{x}.py"
icon = lambda x: f":material/{x}:"

# Page Setup
home = st.Page(
    page=views("home"),
    title="Accueil",
    icon=icon("home"),
    default=True,
)

train_model = st.Page(
	page=views("train_model"),
	title="Entraîner un modèle",
	icon=icon("build"),
)

get_cars_info = st.Page(
    page=views("get_cars_info"),
    title="Enregistrer une voiture",
    icon=icon("directions_car"),
)

brouillon = st.Page(
    page=views("draft"),
    title="Brouillons",
    icon=icon("build"),
)

pg = st.navigation(pages=[
	home,
	get_cars_info,
	train_model,
    brouillon,
])

pg.run()
