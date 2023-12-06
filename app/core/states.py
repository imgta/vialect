import streamlit as st
import time

class KeyStates:
    OPENAI_PREFIX = "sk-"
    HUGGING_PREFIX = "hf_"
    WHISPER_DEFAULT_MODEL = "tiny"
    MODEL_OPTIONS = ['whisp','param0', 'param1', 'speed0', 'speed1']
    PROCESS_STATES = ['english', 'translate', 'url', 'upload', 'attached', 'url_btn', 'upload_btn', 'processing', 'audio', 'diarize', 'rttm', 'transcript', 'openai_api_key', 'openai_updated', 'hf_access_token', 'hf_updated']
    MEDIA_STATES = ['select_audio_offset', 'select_media', 'media_summary', 'select_whisper']

    def __init__(self, model_select):
        self.model_select = model_select
        self.init_states()

    def init_states(self):
        self._init_process_states()
        self._init_model_states()
        self._init_media_states()


    def _init_model_states(self):
        default_model = st.session_state.get('whisp', self.WHISPER_DEFAULT_MODEL)
        for state in self.MODEL_OPTIONS:
            if state not in st.session_state:
                if state == 'whisp':
                    st.session_state[state] = self.WHISPER_DEFAULT_MODEL
                elif state in ['param0', 'param1']:
                    st.session_state[state] = self.model_select.model_params(default_model)
                elif state in ['speed0', 'speed1']:
                    st.session_state[state] = self.model_select.model_speeds(default_model)

    def _init_process_states(self):
        for state in self.PROCESS_STATES:
            if state not in st.session_state:
                st.session_state[state] = False

    def _init_media_states(self):
        for state in self.MEDIA_STATES:
            if state not in st.session_state:
                if state == 'select_audio_offset':
                    st.session_state['select_audio_offset'] = 0
                elif state == 'select_whisper':
                    st.session_state['select_whisper'] = None
                elif state in ['select_media', 'media_summary']:
                    st.session_state[state] = False

    def _get_secret_key(self, key_name: str):
        key = st.secrets[key_name]
        return key if key else False

    def set_openai_key(self, openai_input: str = None):
        if not openai_input and self.has_secret_openai():
            st.session_state['openai_api_key'] = self._get_secret_key('OPENAI_API_KEY')
            # st.info(body="Secret OpenAI API key!", icon="✔")
        elif openai_input:
            if openai_input.startswith(self.OPENAI_PREFIX):
                if not st.session_state['openai_updated']:
                    st.session_state['openai_api_key'] = openai_input
                    openai_loaded = st.success(body="OpenAI API Key loaded!", icon="✔")
                    time.sleep(1.00)
                    openai_loaded.empty()
                    st.session_state['openai_updated'] = True
            else:
                st.session_state['openai_updated'] = False
                st.error(body="Invalid OpenAI API Key.")

    def set_hf_token(self, hf_input: str = None):
        if not hf_input and self.has_secret_hf_token():
            st.session_state['hf_access_token'] = self._get_secret_key('HUGGING_FACE_TOKEN')
            # st.info(body="Secret HuggingFace Token!", icon="✔")
        elif hf_input:
            if hf_input.startswith(self.HUGGING_PREFIX):
                if not st.session_state['hf_updated']:
                    st.session_state['hf_access_token'] = hf_input
                    hf_loaded = st.success(body="HuggingFace Token loaded!", icon="✔")
                    time.sleep(1.00)
                    hf_loaded.empty()
                    st.session_state['hf_updated'] = True
            else:
                st.session_state['hf_updated'] = False
                st.error(body="Invalid HuggingFace Token.")


    def openai_placeholder(self) -> str:
        if self.has_secret_openai():
            return "✔ API Key imported from 'secrets.toml'"
        else:
            return "Paste your OpenAI API key here (sk-...)"

    def hf_placeholder(self) -> str:
        if self.has_secret_hf_token():
            return "✔ Token imported from 'secrets.toml'"
        else:
            return "Paste your HF access token here (hf_...)"


    def has_secret_openai(self) -> bool:
        return 'OPENAI_API_KEY' in st.secrets and st.secrets['OPENAI_API_KEY'].startswith(self.OPENAI_PREFIX) and not st.secrets['OPENAI_API_KEY'].endswith("...")

    def has_secret_hf_token(self) -> bool:
        return 'HUGGING_FACE_TOKEN' in st.secrets and st.secrets['HUGGING_FACE_TOKEN'].startswith(self.HUGGING_PREFIX) and not st.secrets['HUGGING_FACE_TOKEN'].endswith("...")
