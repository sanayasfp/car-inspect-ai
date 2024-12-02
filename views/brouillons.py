import streamlit as st

# view jupyter notebook

file_path = 'draft/car_part_detection.py'

def load_notebook(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()

header = st.container()
header.title("Jupyter Notebook Viewer")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

### Custom CSS for the sticky header
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: #a97400;
        z-index: 999;
        text-align: center;
    }
    .fixed-header {
        border-bottom: 1px solid black;
    }
</style>
    """,
    unsafe_allow_html=True
)
# st.title('Jupyter Notebook Viewer')
st.code(load_notebook(file_path), language='python')
