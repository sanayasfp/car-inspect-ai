import streamlit as st
import constants
from db.manager import Manager as DBManager
from db.models import TrainLogsModel
import pandas as pd
from ml.car_parts_detection.main import main as train_model
import os

db_manager = DBManager(check_same_thread=False)
DEFAULT_MODELS = ["yolo11n"]

st.title("Entraîner un modèle")


def list_previous_model(write: bool = True):
    models_info = db_manager.select(
        TrainLogsModel.get_table_name(TrainLogsModel),
        columns=["id", "name", "path", "completed", "created_at"],
        condition="ORDER BY created_at DESC",
        verbose=True,
    )
    df = pd.DataFrame(models_info)
    if write:
        st.write("Liste des modèles précédents")
        st.write(df)
    
    return df


previous_model = list_previous_model()

selected_model = st.selectbox(
    "Choisir un modèle",
    [*DEFAULT_MODELS, *previous_model["name"]],
    placeholder="Choisir un modèle",
)

selected_model = selected_model.casefold()
if selected_model in DEFAULT_MODELS:
  model_path = os.path.join(constants.TMP_DIR, f"{selected_model}.pt")
else:
  selected_model_path = previous_model.query(f"name == '{selected_model}' and completed == 'True'").to_dict("records")[0]["path"]
  print(selected_model_path)
  model_path = os.path.join(selected_model_path, "last.pt").replace("\\", "/")

st.write("Détails du modèle:")
st.write(f"Nom: {selected_model}")

if st.button("Entraîner"):
  if model_path:
    try:
      train_model(model_path)
    except Exception as e:
      st.error(f"Erreur: {e}")
  else:
    st.error("Aucun modèle n'a été trouvé.")
