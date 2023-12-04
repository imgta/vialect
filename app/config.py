import pathlib

# Streamlit App and Project folder structure
APP_DIR = pathlib.Path(__file__).parent.absolute()
PROJ_DIR = APP_DIR.parent.absolute()

# Data directory for processed files
DATA_DIR = PROJ_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Media directory for extracted, transformed data
MEDIA_LIB = DATA_DIR / "media"
MEDIA_LIB.mkdir(exist_ok=True)

# UI components and rendering directories
LAYOUT_DIR = APP_DIR / "layout"
IMG_DIR = LAYOUT_DIR / "imgs"
STYLES_DIR = LAYOUT_DIR / "styles"


def page_cfg(page_name: str = "", layout: str = "wide") -> dict[str, str]:
    return {
        "page_title": f"{page_name}ViaLect",
        "page_icon": "👾",
        "layout": layout,
        "initial_sidebar_state": "expanded"
        }
