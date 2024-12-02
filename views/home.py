import os
import streamlit as st
import constants

# Load the README.md file

# EN_US -> EN
lang = constants.LANG.upper().split("_")[0]
lang = "FR" # TODO: Remove this line
readme = f"README_{lang}.md" if lang != "EN" else "README.md"

with open(os.path.join(readme), "r", encoding="utf-8") as file:
    content = file.read()
    st.markdown(content)
