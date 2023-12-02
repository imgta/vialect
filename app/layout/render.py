from layout.ui import STYLES_DIR, via_header, via_sidebar, coffee_btn, social_btns, waves
from core.states import KeyStates
import streamlit as st
kS = KeyStates()

def css_import():
    with open(STYLES_DIR / "global.css") as global_css, open(STYLES_DIR / "button.css") as btn_css, open(STYLES_DIR / "waves.css") as waves_css:
        styles = global_css.read() + "\n" + btn_css.read()+ "\n" + waves_css.read()
        st.markdown(f'<style>{styles}</style>' , unsafe_allow_html= True)


def set_header():
    st.markdown(via_header(), unsafe_allow_html=True)


def set_sidebar():
    with st.sidebar:
        st.markdown(via_sidebar(), unsafe_allow_html=True)
        st.markdown(social_btns(), unsafe_allow_html=True)
        k0, k1 = st.columns([2, 2])
        openai_key_input = st.text_input(
                label="OpenAI API Key:",
                key="openai_key_input",
                type="password",
                placeholder=kS.openai_placehold(),
                disabled=kS.has_secret_openai(),
                help="Visit https://platform.openai.com/api-keys"
            )
        with k0:
            kS.set_openai_key(openai_key_input)

        hf_token_input = st.text_input(
            label="HuggingFace Token:",
            key="hf_token_input",
            type="password",
            placeholder=kS.hf_placehold(),
            disabled=kS.has_secret_hf_token(),
            help="Visit https://huggingface.co/settings/tokens"
        )
        with k1:
            kS.set_hf_token(hf_token_input)

        st.markdown(coffee_btn(), unsafe_allow_html=True)


def set_layout():
    css_import()
    set_header()
    set_sidebar()


def set_test():
    css_import()
    st.markdown(waves(), unsafe_allow_html=True)
