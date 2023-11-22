import streamlit as st
from st_audiorec import st_audiorec


# Trying out different voice recording components
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(data=wav_audio_data, format='audio/wav')
