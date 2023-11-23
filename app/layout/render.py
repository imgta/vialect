from layout.ui import STYLES_DIR, via_header, via_sidebar, coffee_btn, social_btns, waves
import streamlit as st

def css_import():
    with open(STYLES_DIR / "global.css") as global_css, open(STYLES_DIR / "button.css") as btn_css, open(STYLES_DIR / "waves.css") as waves_css:
        styles = global_css.read() + "\n" + btn_css.read()+ "\n" + waves_css.read()
        st.markdown(f'<style>{styles}</style>' , unsafe_allow_html= True)

def set_header():
    st.markdown(via_header(), unsafe_allow_html=True)

from core.states import set_openai_key
def set_sidebar():
    with st.sidebar:
        st.markdown(via_sidebar(), unsafe_allow_html=True)
        st.markdown(social_btns(), unsafe_allow_html=True)
        openai_key_input = st.text_input(
            label="OpenAI API Key:",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="Visit https://platform.openai.com/api-keys",
            value=st.session_state.get('OPEN_API_KEY', ''),
        )
        if openai_key_input:
            set_openai_key(openai_key_input)

        st.markdown(coffee_btn(), unsafe_allow_html=True)

def set_layout():
    css_import()
    set_header()
    set_sidebar()


def set_test():
    css_import()
    st.markdown(waves(), unsafe_allow_html=True)
