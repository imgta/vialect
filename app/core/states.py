from core.models import ModelSelect
import streamlit as st


def init_session_states() -> None:
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

def set_openai_key(api_key: str) -> None:
    st.session_state['OPENAI_API_KEY'] = api_key
