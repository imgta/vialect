from streamlit_player import st_player
from core.utils import TaskUtility
from layout.render import mark_newlines
from config import MEDIA_LIB
import streamlit as st
import json
import os

tU = TaskUtility()

priority_hash = {
        'large.en': 10, 'large': 9,
        'medium.en': 8, 'medium': 7,
        'small.en': 6, 'small': 5,
        'base.en': 4, 'large': 3,
        'tiny.en': 2, 'large': 1,
    }

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

def get_whispers(transcript):
    whisper_models = []
    for entry in transcript:
        model = entry.get('model')
        if model:
            whisper_models.append(model)

    return whisper_models


def set_media_lib():
    for media in os.listdir(MEDIA_LIB):
        MEDIA_PATH = os.path.join(MEDIA_LIB, media)
        if os.path.isdir(MEDIA_PATH):

            media_script = os.path.join(MEDIA_PATH, 'transcript.json')
            if os.path.isfile(media_script):
                with open(media_script, 'r') as mscript:
                    transcript = json.load(mscript)

            media_json = os.path.join(MEDIA_PATH, 'info.json')
            if os.path.isfile(media_json):
                with open(media_json, 'r') as mjson:
                    media_info = json.load(mjson)

                media_id = media_info['id']
                st.markdown('<span id="media-click"></span>', unsafe_allow_html=True)
                details_btn = st.button(label="", key=media_id)

                html_code = f"""
<div class="library-con">
    <div class="card-media">
        <!-- MEDIA CONTAINER -->
        <div class="card-media-obj-container">
            <div class="card-media-obj" style="background-image: url({media_info.get('thumbnail', '')});"></div>
            <span class="card-media-obj-tag subtle"></span>
        </div>
        <!-- CARD BODY -->
        <div class="card-media-body">
            <div class="card-media-body-top">
                <div class="card-media-body-top-icons u-float-right">
                    <svg fill="#888888" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
                    <path d="M0 0h24v24H0z" fill="none"/></svg>
                </div>
                <div class="card-media-body-heading">{tU.truncate_str(media_info.get('title'), 50)}</div>
                <div class="subtle">{media_info.get('uploader')} <span class="subtle-info">&mdash; {get_category(media_info, 1)}</span></div>
                <div class="subtle-info">{f"Whispers: {', '.join(get_whispers(transcript))}"}</div>
            </div>
            <div class="card-media-body-supporting-bottom">
                <span class=".card-media-body-bottom-text subtle">{media_info.get('extractor_key')}</span>
                <span class=".card-media-body-bottom-text subtle u-float-right">{media_info.get('extract_date')}</span>
            </div>
            <div class="card-media-body-supporting-bottom card-media-body-supporting-bottom-reveal">
                <span class=".card-media-body-bottom-text subtle-info">{get_tags(media_info, 3)}</span>
                <a href="#" class=".card-media-body-bottom-text card-media-link u-float-right">DETAILS</a>
            </div>
        </div>
    </div>
</div>"""
                st.markdown(body=html_code, unsafe_allow_html=True)
                if details_btn:
                    st.session_state['select_media'] = media_info
                    st.session_state['media_summary'], _ = get_transcript(media_info)
                    st.rerun()

    return st.session_state['select_media']

def get_media_details(media_info):
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
        <div class="detail-subtle">🧪 {media_info.get('extract_date', '')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

def get_transcript(select_media):
    GPT_MODEL = 'gpt-3.5-turbo-1106'
    SCRIPT_PATH = os.path.join(MEDIA_LIB, select_media['title_dir'], 'transcript.json')
    if os.path.isfile(SCRIPT_PATH):
        with open(SCRIPT_PATH, 'r') as script:
            media_script = json.load(script)

        top_summary = None
        top_priority = 0
        top_model = None

        for entry in media_script:
            model = entry.get('model')

            if model in priority_hash:
                priority = priority_hash[model]

                if priority > top_priority and entry.get('summary'):
                    top_summary = entry['summary'][GPT_MODEL]
                    top_priority = priority
                    top_model = entry['model']

        st.session_state['media_summary'] = top_summary
        return st.session_state['media_summary'], top_model
    return None


def get_timestamps(select_media):
    STAMPS_PATH = os.path.join(MEDIA_LIB, select_media['title_dir'], 'stamps.json')
    if os.path.isfile(STAMPS_PATH):
        with open(STAMPS_PATH, 'r') as stamp:
            media_stamps = json.load(stamp)

        top_timestamps = None
        top_priority = 0

        for entry in media_stamps:
            model = entry.get('model')
            if model in priority_hash:
                priority = priority_hash[model]
                if priority > top_priority and entry.get('timestamps'):
                    top_timestamps = entry['timestamps']
                    top_priority = priority

        return top_timestamps
    return None

def list_media():
    selected = set_media_lib()
    if 'select_media' in st.session_state and st.session_state['select_media']:
        AUDIO_PATH = os.path.join(MEDIA_LIB, selected['title_dir'], 'audio.OGG')
        timestamps = get_timestamps(selected)
        summary, summary_whisp = get_transcript(selected)

        # VIDEO AND AUDIO PLAYER
        with st.sidebar:
            mark_newlines(2)
            st_player(
                url=selected['webpage_url'],
                key=f"select-{selected['id']}",
                height=250)

            if os.path.isfile(AUDIO_PATH):
                st.audio(data=AUDIO_PATH, start_time=st.session_state['select_audio_offset'])

        if 'media_summary' in st.session_state and st.session_state['media_summary']:
            with st.sidebar:
                m0, m1, m2 = st.tabs(['DETAILS', 'SUMMARY', 'TRANSCRIPT'])

                with m0:
                    get_media_details(selected)
                    mark_newlines(2)

                    # Consolidate/reduce double newlines for cleaner markdown format
                    clean_description = selected['description'].replace("\n\n ","\n")
                    st.caption(body=clean_description, unsafe_allow_html=True)

                with m1:
                    st.markdown(body=f"""
                    <div class="detail-heading">Via whisper {summary_whisp} and GPT-3.5:</div>
                    <div class="detail-subtle">{summary}</div>
                """, unsafe_allow_html=True)

                with m2:
                    st.caption("Buttons seek to corresponding timestamps.")

                    m2a, m2b = st.columns([1.5,4])
                    for log in timestamps:
                        with m2a:
                            audio_offset =  st.button(label=f"▶ &nbsp;{log['start']}", key=f"play-{log['start']}")
                            mark_newlines(1)
                            if audio_offset != 0:
                                st.session_state['select_audio_offset'] = tU.floor_timestamp_sec(log['start'])
                                st.rerun()

                        m2b.caption(body=f"{log['speaker']}: {log['text']}")
