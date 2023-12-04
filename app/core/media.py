from streamlit_player import st_player
from streamlit_extras.grid import grid
from core.utils import TaskUtility
from config import MEDIA_LIB
import streamlit as st
import json
import os


def show_meta(media):
    media_tags = ''
    tag_count = 0
    if media.get('tags', []):
        for tag in media.get('tags', []):
            if " " in tag:
                continue
            media_tags += f"#{tag} "
            tag_count += 1
            if tag_count == 3:
                break
    elif media.get('categories', []):
        media_tags = media.get('categories', [])[0]
    return media_tags

def display_media(media):
    st.markdown(f"""
    <div class="library-con">
    <div class="card-media">
        <!-- MEDIA CONTAINER -->
        <div class="card-media-object-container">
            <div class="card-media-object" style="background-image: url({media.get('thumbnail')});"></div>
            <span class="card-media-object-tag subtle"></span>
        </div>
        <!-- CARD BODY -->
        <div class="card-media-body">
            <div class="card-media-body-top">
                <div class="card-media-body-top-icons u-float-right">
                    <!-- <span class="subtle">{media.get('extract_date')}</span> -->
                    <svg fill="#888888" height="16" viewBox="0 0 24 24" width="16" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
                        <path d="M0 0h24v24H0z" fill="none"/>
                    </svg>
                </div>
                <span class="card-media-body-heading">{TaskUtility().truncate_str(media.get('title'), 50)}</span>
                <div class="subtle">{media.get('uploader')}</div>
                <!-- <div class="subtle-info">{f"{media.get('view_count'):,}"} views</div> -->
                <div class="subtle-info">Extracted: {media.get('extract_date')}</div>
            </div>
        <!-- <span class="card-media-body-heading">{media.get('title')}</span> -->
            <div class="card-media-body-supporting-bottom">
                <span class="card-media-body-supporting-bottom-text subtle">{media.get('extractor_key')}</span>
                <span class="card-media-body-supporting-bottom-text subtle u-float-right">{media.get('extract_date')}</span>
            </div>
            <div class="card-media-body-supporting-bottom card-media-body-supporting-bottom-reveal">
                <span class="card-media-body-supporting-bottom-text subtle">{show_meta(media)}</span>
                <a href="#/" class="card-media-body-supporting-bottom-text card-media-link u-float-right">DETAILS</a>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)




def list_media():
    for media in os.listdir(MEDIA_LIB):
        MEDIA_PATH = os.path.join(MEDIA_LIB, media)
        if os.path.isdir(MEDIA_PATH):
            media_info = os.path.join(MEDIA_PATH, 'info.json')

            if os.path.isfile(media_info):
                with open(media_info, 'r') as file:
                    info = json.load(file)
                display_media(info)

                # c0, c1 = st.columns([3, 3])
                # with c0:
                #     st.write("**Title:**", info.get('title'))
                #     st.write("**Uploader:**", info.get('uploader'))
                #     st.write("**Source:**", info.get('extractor_key'))
                #     st.write("**Upload Date:**", TaskUtility().format_date(info.get('upload_date')))
                # with c1:
                #     st_player(url=info['webpage_url'], height=250)

                # st.divider()
