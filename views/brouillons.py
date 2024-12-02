import streamlit as st

# view jupyter notebook

file_path = 'car_part_detection.ipynb'

def load_notebook(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()
      

st.markdown(load_notebook(file_path), unsafe_allow_html=True)
