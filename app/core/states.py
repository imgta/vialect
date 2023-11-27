from core.models import ModelSelect
import streamlit as st


def init_session_states() -> None:
    if 'OPENAI_API_KEY' in st.secrets:
        if st.secrets['OPENAI_API_KEY'].startswith("sk-"):
            st.session_state['openai_api_key'] = st.secrets['OPENAI_API_KEY']
    else:
        st.session_state['openai_api_key'] = False

    if 'HUGGING_FACE_TOKEN' in st.secrets:
        if st.secrets['HUGGING_FACE_TOKEN'].startswith("hf_"):
            st.session_state['hf_access_token'] = st.secrets['HUGGING_FACE_TOKEN']
    else:
        st.session_state['hf_access_token'] = False


    initial_states = ['english', 'translate', 'url', 'upload', 'attached', 'url_btn', 'upload_btn', 'processing', 'audio', 'diarize', 'rttm', 'transcript', 'whisp', 'param0', 'param1', 'speed0', 'speed1']
    mS = ModelSelect()

    for state in initial_states:
        if state not in st.session_state:
            if state in ['param0', 'param1']:
                st.session_state[state] = mS.model_params(st.session_state.get('whisp', 'tiny'))
            elif state in ['speed0', 'speed1']:
                st.session_state[state] = mS.model_speeds(st.session_state.get('whisp', 'tiny'))
            elif state == 'whisp':
                st.session_state[state] = 'tiny'
            else:
                st.session_state[state] = False

class KeyStates:
    @staticmethod
    def has_secret_openai() -> bool:
        return 'OPENAI_API_KEY' in st.secrets and st.secrets['OPENAI_API_KEY'].startswith("sk-") and not st.secrets['OPENAI_API_KEY'].endswith("...")

    @staticmethod
    def has_secret_hf_token() -> bool:
        return 'HUGGING_FACE_TOKEN' in st.secrets and st.secrets['HUGGING_FACE_TOKEN'].startswith("hf_") and not st.secrets['HUGGING_FACE_TOKEN'].endswith("...")

    def openai_placehold(self) -> str:
        if self.has_secret_openai():
            return "API Key imported from 'secrets.toml'"
        else:
            return "Paste your OpenAI API key here (sk-...)"

    def hf_placehold(self) -> str:
        if self.has_secret_hf_token():
            return "Token imported from 'secrets.toml'"
        else:
            return "Paste your HF access token here (hf_...)"

    def set_openai_key(self, openai_input: str):
        if not openai_input and self.has_secret_openai():
            st.session_state['openai_api_key'] = st.secrets['OPENAI_API_KEY']
            st.info(body="Secret OpenAI API key!", icon="✔")
        elif openai_input:
            if openai_input.startswith("sk-"):
                st.session_state['openai_api_key'] = openai_input
                return st.success(body="Your OpenAI API Key has been loaded!", icon="✔")
            else:
                return st.error(body="Invalid key format, please try again.", icon="❌")

    def set_hf_token(self, hf_input: str):
        if not hf_input and self.has_secret_hf_token():
            st.session_state['hf_access_token'] = st.secrets['HUGGING_FACE_TOKEN']
            st.info(body="Secret HuggingFace Token!", icon="✔")
        elif hf_input:
            if hf_input.startswith("hf_"):
                st.session_state['hf_access_token'] = hf_input
                return st.success(body="Your HuggingFace Token has been loaded!", icon="✔")
            else:
                return st.error(body="Invalid token, please try again.", icon="❌")
