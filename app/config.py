import pathlib

# Streamlit App and Project folder structure
APP_DIR = pathlib.Path(__file__).parent.absolute()
PROJ_DIR = APP_DIR.parent.absolute()

# Data directory for processed files
DATA_DIR = PROJ_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Media directory for extracted, transformed data
MEDIA_BIN = DATA_DIR / "media"
MEDIA_BIN.mkdir(exist_ok=True)

def page_cfg(page_name="", layout="wide"):
    return {
        "page_title": f"{page_name}V/A.Lect",
        "page_icon": "🧪",
        "layout": layout,
        "initial_sidebar_state": "expanded"
        }
