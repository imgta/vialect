from layout.ui import HTMLInterface
from config import STYLES_DIR
import streamlit as st

def mark_newlines(num_lines: int) -> None:
    newlines = num_lines
    while newlines > 0:
        st.markdown(body="\n", unsafe_allow_html=True)
        newlines -= 1

class RenderUI:
    def __init__(self, key_states, html_ui: HTMLInterface = HTMLInterface()):
        self.key_states = key_states
        self.html_ui = html_ui


    @staticmethod
    def import_css():
        try:
            with open(STYLES_DIR / "global.css") as global_css, open(STYLES_DIR / "button.css") as btn_css, open(STYLES_DIR / "waves.css") as waves_css, open(STYLES_DIR / "media.css") as media_css:
                styles = global_css.read() + "\n" + btn_css.read() + "\n" + waves_css.read() + "\n" + media_css.read()
                st.markdown(f'<style>{styles}</style>' , unsafe_allow_html= True)
        except FileNotFoundError as e:
            print(f"Error loading CSS styling: {e}")
            st.error(body=f"Error loading CSS styling: {e}")

    def set_sidebar(self):
        with st.sidebar:
            st.markdown(self.html_ui.via_sidebar(), unsafe_allow_html=True)

            side_L, side_R = st.columns([0.72, 0.28])
            with side_L:
                mark_newlines(2)
                with st.expander(label="SECRET KEYS DRAWER"):
                    openai_key_input = st.text_input(
                            label="OpenAI API Key:",
                            key="openai_key_input",
                            type="password",
                            placeholder=self.key_states.openai_placeholder(),
                            disabled=self.key_states.has_secret_openai(),
                            help="Visit https://platform.openai.com/api-keys"
                        )
                    self.key_states.set_openai_key(openai_key_input)

                    hf_token_input = st.text_input(
                        label="HuggingFace Token:",
                        key="hf_token_input",
                        type="password",
                        placeholder=self.key_states.hf_placeholder(),
                        disabled=self.key_states.has_secret_hf_token(),
                        help="Visit https://huggingface.co/settings/tokens"
                    )
                    self.key_states.set_hf_token(hf_token_input)

            with side_R:
                st.markdown(self.html_ui.social_btns(), unsafe_allow_html=True)

    def set_header(self):
        st.markdown(self.html_ui.via_header(), unsafe_allow_html=True)

    def show_cuda(self):
        st.markdown(self.html_ui.cuda_info(), unsafe_allow_html=True)
        mark_newlines(2)

    def set_layout(self):
        self.import_css()
        self.set_header()
        self.set_sidebar()

    def set_test(self):
        self.import_css()
