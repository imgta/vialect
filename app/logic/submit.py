import validators
import streamlit as st


def url_change(url: str) -> bool:
    # URL address validation
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return validators.url(url)


def url_submit():
    st.session_state.url = True


def upload_change():
    st.session_state.attached = not st.session_state.attached


def upload_label():
    return "visible" if not st.session_state.attached else "collapsed"


def upload_submit():
    st.session_state.upload = True
