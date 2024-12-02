# ask for system: windows or linux
# activate virtual environment
# install requirements.txt
# streamlit run app.py

import os
import sys

is_linux = sys.platform == 'linux'

def check_if_requirements_installed():
    try:
        import streamlit
        import pandas
        import numpy
        import ultralytics
        return True
    except ImportError:
        return False


def install_requirements():
    if not check_if_requirements_installed():
        os.system('python -m pip install -r requirements.txt')


def activate_virtual_environment():
    if not is_linux:
        os.system('.venv\\Scripts\\activate')
    else:
        os.system('source .venv/bin/activate')
        
def run_streamlit():
    os.system('python -m streamlit run app.py')


if __name__ == '__main__':
    activate_virtual_environment()
    install_requirements()
    run_streamlit()
