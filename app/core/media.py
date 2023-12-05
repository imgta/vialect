from streamlit_player import st_player
from core.utils import TaskUtility
from config import MEDIA_LIB
import streamlit as st
import json
import os
import re

tU = TaskUtility()

def get_tags(media_info, tag_limit):
    media_tags = ''
    tag_count = 0
    if media_info.get('tags', []):
        for tag in media_info.get('tags', []):
            if " " in tag:
                continue
            media_tags += f"#{tag} "
            tag_count += 1
            if tag_count == tag_limit:
                return media_tags
    return media_tags

def get_category(media_info, cat_limit):
    media_cats = ''
    cat_count = 0
    if media_info.get('categories', []):
        for cat in media_info.get('categories', []):
            media_cats += cat
            cat_count += 1
            if cat_count == cat_limit:
                return media_cats
    return media_cats

def show_media_details(media_info):
    st.markdown(body=f"""
<div class="details-con">
    <div class="detail-header">
        <div class="detail-heading">Title: <a href={media_info.get('webpage_url', '#')} class="detail-info">{media_info.get('title', '')}</a></div>
        <div class="detail-subtle">{media_info.get('duration_string', '')} duration</div>
    </div>
    <div class="detail-header">
        <div class="detail-heading">Channel: <a href={media_info.get('uploader_url', '#')} class="detail-info">{media_info.get('uploader', '')}</a></div>
        <div class="detail-subtle">{get_category(media_info, 3)}</div>
    </div>
    <div class="detail-header">
        <div class="detail-heading">Source: <span class="detail-info">{media_info.get('extractor_key', '')}</span></div>
        <div class="detail-subtle">{get_tags(media_info, 4)}</div>
    </div>
    <div class="detail-header">
        <div class="detail-heading">Uploaded: <span class="detail-info">{tU.format_upload_date(media_info.get('upload_date', ''))}</span></div>
        <div class="detail-subtle">extracted {media_info.get('extract_date', '')}</div>
    </div>
</div>
""", unsafe_allow_html=True)


def display_media_info(media_info):
    media_id = media_info.get('id')

    st.markdown('<span id="media-click"></span>', unsafe_allow_html=True)
    details_btn = st.button(label="", key=media_id)

    html_code = f"""
<div class="library-con">
    <div class="card-media">
        <!-- MEDIA CONTAINER -->
        <div class="card-media-object-container">
            <div class="card-media-object" style="background-image: url({media_info.get('thumbnail', '')});"></div>
            <span class="card-media-object-tag subtle"></span>
        </div>
        <!-- CARD BODY -->
        <div class="card-media-body">
            <div class="card-media-body-top">
                <div class="card-media-body-top-icons u-float-right">
                    <svg fill="#888888" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                </div>
                <div class="card-media-body-heading">{tU.truncate_str(media_info.get('title'), 50)}</div>
                <div class="subtle">{media_info.get('uploader')} <span class="subtle-info">&mdash; {get_category(media_info, 1)}</span></div>
                <div class="subtle-info">{f"{media_info.get('view_count', ''):,}"} views</div>
                <!-- <a href={media_info.get('webpage_url')} class="subtle-info">SOURCE</a> -->
            </div>
            <div class="card-media-body-supporting-bottom">
                <span class="card-media-body-supporting-bottom-text subtle">{media_info.get('extractor_key')}</span>
                <span class="card-media-body-supporting-bottom-text subtle u-float-right">{media_info.get('extract_date')}</span>
            </div>
            <div class="card-media-body-supporting-bottom card-media-body-supporting-bottom-reveal">
                <span class="card-media-body-supporting-bottom-text subtle-info">{get_tags(media_info, 3)}</span>
                <a href="#" class="card-media-body-supporting-bottom-text card-media-link u-float-right">DETAILS</a>
            </div>
        </div>
    </div>
</div>
"""
    st.markdown(body=html_code, unsafe_allow_html=True)
    if details_btn:
        st.session_state['select_media'] = media_info
        st.rerun()


def list_media(select_model):
    for media in os.listdir(MEDIA_LIB):
        MEDIA_PATH = os.path.join(MEDIA_LIB, media)

        if os.path.isdir(MEDIA_PATH):
            media_info = os.path.join(MEDIA_PATH, 'info.json')

            if os.path.isfile(media_info):
                with open(media_info, 'r') as inf:
                    info = json.load(inf)
                display_media_info(info)

    if 'select_media' in st.session_state and st.session_state['select_media']:
        with st.sidebar:
            st.markdown(body="\n")
            selected = st.session_state['select_media']

            # Embeded video and audio player for selected media
            st_player(
                url=selected['webpage_url'],
                key=f"select-{selected['id']}",
                height=250)

            AUDIO_PATH = os.path.join(MEDIA_LIB, selected['title_dir'], 'audio.OGG')
            st.audio(data=AUDIO_PATH)

        RTTM_PATH = os.path.join(MEDIA_LIB, selected['title_dir'], 'speakers.rttm')
        if os.path.isfile(RTTM_PATH):
            with open(RTTM_PATH, 'r') as rttm:
                media_rttm = json.load(rttm)

        SCRIPT_PATH = os.path.join(MEDIA_LIB, selected['title_dir'], 'transcript.json')
        if os.path.isfile(SCRIPT_PATH):
            with open(SCRIPT_PATH, 'r') as scrip:
                media_script = json.load(scrip)

            for entry in media_script:
                if entry['model'] == select_model:
                    if 'summary' in entry:
                        st.session_state['media_summary'] = entry['summary']['gpt-3.5-turbo-1106']

        if 'media_summary' in st.session_state and st.session_state.media_summary:
            with st.sidebar:

                m0, m1, m2 = st.tabs(['DETAILS', 'SUMMARY', 'TRANSCRIPT'])

                with m0:
                    show_media_details(info)
                    st.markdown(body="\n")
                    st.markdown(body="\n")
                    with st.expander(label="Description", expanded=False):
                        clean_description = info['description'].replace("\n\n ","\n")
                        st.caption(body=clean_description, unsafe_allow_html=True)

                with m1:
                    with st.expander(label=f"Whisper {st.session_state.w_model.split(maxsplit=1)[0]} & GPT-3.5"):
                        st.caption(body=st.session_state['media_summary'])

                # with m2:
                #     st.caption(body=media_rttm)
