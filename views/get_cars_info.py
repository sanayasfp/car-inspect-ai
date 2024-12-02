import streamlit as st
from predict import predict

st.title("Enregistrer une voiture")

image_types = ["jpg", "png", "jpeg"]

# Utiliser `st.session_state` pour suivre les erreurs.
if "errors" not in st.session_state:
    st.session_state.errors = {}

def show_error(field):
    """Afficher un message d'erreur pour un champ spécifique."""
    if field in st.session_state.errors:
        st.error(st.session_state.errors[field])
        
def set_error(field, message):
    """Définir un message d'erreur pour un champ spécifique."""
    st.session_state.errors[field] = message

def has_errors(*fields):
    """Vérifier si des erreurs existent."""
    
    if fields:
        return any(field in st.session_state.errors for field in fields)
    
    return bool(st.session_state.errors)

def clear_errors(*fields):
    """Effacer tous les messages d'erreur."""
    
    for field in fields:
        if field in st.session_state.errors:
            del st.session_state.errors[field]
    
    if not fields:
        st.session_state.errors = {}
    pass

st.write("Veuillez télécharger les images de la voiture")
front_image = st.file_uploader("Avant de la voiture", type=image_types, on_change=lambda: clear_errors("front_image"))
show_error("front_image")
back_image = st.file_uploader("Arrière de la voiture", type=image_types, on_change=lambda: clear_errors("back_image"))
show_error("back_image")
left_image = st.file_uploader("Côté gauche de la voiture", type=image_types, on_change=lambda: clear_errors("left_image"))
show_error("left_image")
right_image = st.file_uploader("Côté droit de la voiture", type=image_types, on_change=lambda: clear_errors("right_image"))
show_error("right_image")

st.write("Veuillez entrer la couleur principale de la voiture")
main_color = st.text_input("Couleur principale", on_change=lambda: clear_errors("main_color"), help="Exemple: Rouge, Bleu, Blanc")
show_error("main_color")

st.write("Veuillez entrer le numéro de plaque de la voiture", help="Exemple: 1234ABC", on_change=lambda: clear_errors("plate_number"))
plate_number = st.text_input("Numéro de plaque")
show_error("plate_number")

if st.button("Enregistrer"):
    # Réinitialiser les erreurs
    clear_errors()

    # Vérifier chaque champ et ajouter des erreurs si nécessaire
    images_fields = {
        "front_image": front_image,
        # "back_image": back_image,
        # "left_image": left_image,
        # "right_image": right_image,
    }
    
    for field, image in images_fields.items():
        if image is None:
            set_error(field, "Ce champ est requis.")
    
    if not main_color:
        set_error("main_color", "Ce champ est requis.")
    
    # if not plate_number:
    #     set_error("plate_number", "Ce champ est requis.")

    # Afficher un message global si des erreurs existent
    if has_errors():
        st.error("Remplissez tous les champs correctement.")
    else:
        predict(front_image, back_image, left_image, right_image, main_color, plate_number)
        st.success("Voiture enregistrée avec succès")
        st.balloons()
