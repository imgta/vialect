import os
import torch
import openai
import threading

import streamlit as st
import streamlit_antd_components as sac
import streamlit.components.v1 as components
from streamlit_extras.row import row
from streamlit_player import st_player
from streamlit_extras.grid import grid
from streamlit.runtime.scriptrunner import get_script_run_ctx

from config import fetch_page_cfg
from logic.utils import threaded_task, progress_bar, gpu
from logic.submit import url_change, url_submit, upload_change, upload_label, upload_submit
from logic.models import display_models, update_display, toggle_en, toggle_trans, model_params, model_speeds, model_switch, model_param_delta, model_speed_delta
from logic.process import save_path, extract_audio, process_upload, audio_length, diarize_audio, parse_rttm, scribe_audio, get_full_language, align_script, summarize
openai.api_key = st.secrets["OPENAI_API_KEY"]

####################################################################################################
for state in ['english', 'translate', 'url', 'upload', 'attached', 'url_btn', 'upload_btn', 'processing', 'audio', 'diarize', 'rttm', 'transcript']:
    if state not in st.session_state:
        st.session_state[state] = False

if 'whisp' not in st.session_state:
    st.session_state['whisp'] = 'tiny'

for state in ['param0', 'param1']:
    if state not in st.session_state:
        st.session_state[state] = model_params(st.session_state.whisp)

for state in ['speed0', 'speed1']:
    if state not in st.session_state:
        st.session_state[state] = model_speeds(st.session_state.whisp)

####################################################################################################
st.set_page_config(**fetch_page_cfg())

with open( "app\style.css" ) as css:
    st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with st.sidebar:
    sac.buttons([
        sac.ButtonsItem(label='GitHub', icon='github', href='https://github.com/imgta'),
        sac.ButtonsItem(label='LinkedIn', icon='linkedin', href='https://www.linkedin.com/in/gordonta/'),
        ], size='middle', align='center', type='text')


####################################################################################################
top = row([5], vertical_align="bottom")
t0, t1 = top.columns([4.15, 1])
st.markdown("""
            <div class="heading-con">
            <p class="home-header">V<p><div class="header-i">|</div><p class="home-header">A.Lect</p>
            <span class="header-motto">Traversing digital oceans, <br> for treasures unseen.</span>
            </div>
            <hr>
            """, unsafe_allow_html=True)
# t0.write("👾 V/A.Lect: Traverse digital oceans for treasures unseen.")
# t0.subheader(body="👾 V/A.Lect: Traverse digital oceans for treasures unseen.", divider=None, anchor=False)
# top.divider()

# h0 = row([1.65, 1.22, 1, 0.85], vertical_align="top")
h0 = row([5], vertical_align="top")
d0, d1, d2, d3 = h0.columns([1.65, 1.22, 1, 0.85])

d0.caption(f"**Device:** :green[{gpu.name}]")
d1.caption(f"**CUDA Available:** :green[{torch.cuda.is_available()}]")
d2.caption(f"**VRAM:** :green[{gpu.memoryFree//1024}] / {gpu.memoryTotal//1024} GB")


h1 = row([5], vertical_align="bottom")
c0, c1, c2, c3 = h1.columns([4.1, 0.25, 1.4, 2.5])
h2 = row([1, 4], vertical_align="top")

update_display()
whisper_model = c0.selectbox(
    label="Whisper model :gray[(req. VRAM)]:",
    options=display_models,
    key="w_model",
    on_change=model_switch,
    help="Smaller models are faster, but larger models offer more accuracy.",
)

en_mode = h2.checkbox(
    label="English",
    value=st.session_state.english,
    on_change=toggle_en,
    help="Noticeable performance bumps when using tiny.en or base.en in English-only use cases.",
)
lang_mode = h2.checkbox(
    label="Translate",
    value=st.session_state.translate,
    on_change=toggle_trans,
    help="Detects and translates language to English.",
)

c1.empty()
c2.metric(
    label="Parameters",
    value=f"{model_params(st.session_state.whisp)}M",
    delta=model_param_delta(),
    help="High parameter counts can lead to higher accuracy.",
)
c3.metric(
    label="Speed",
    value=f"{model_speeds(st.session_state.whisp)}x",
    delta=model_speed_delta(),
    help="Inference speeds (relative) decrease as model sizes grow.",
)

g1 = grid([4,1], [4,1], [4,1], [4,1], vertical_align="bottom")
video_url = g1.text_input(label="Enter a video URL:", placeholder="YouTube, Vimeo, Dailymotion, etc.") if not st.session_state.upload_btn else g1.empty()
if video_url:
    if url_change(video_url):
        url_btn = g1.button(label="Submit URL", on_click=url_submit, use_container_width=True)
    else:
        g1.empty()
else:
    g1.empty()

if st.session_state.url:
    st.session_state.url_btn = True
    st_player(url=video_url)

upload_file = g1.file_uploader(label="Upload video or audio:", type=['wav', 'mp3', 'ogg', 'mp4', 'mkv', 'avi', 'mov', 'flv'], on_change=upload_change, label_visibility=upload_label()) if not st.session_state.url_btn else g1.empty()
if upload_file and not st.session_state.url_btn:
    g1.empty()
    upload_btn = g1.button(label="Submit File", on_click=upload_submit, use_container_width=True)
else:
    g1.empty()

if st.session_state.upload:
    st.session_state.upload_btn = True
    max_size_mb = 200
    file_size_mb = upload_file.size / (1024**2)
    if file_size_mb > max_size_mb:
        st.error(f"File size exceeds the maximum limit of {max_size_mb} MB.")
    else:
        upload_path = os.path.join(save_path, upload_file.name)
        with open(upload_path, "wb") as f:
            f.write(upload_file.getbuffer())

g2 = grid([4.35, 1.15], [1.1, 1.35, 1.2, 1.4], [5], [5], 1, 1, 1, vertical_align="center")
if st.session_state.url_btn or st.session_state.upload_btn:
    if st.session_state.url_btn:
        url_dict = {}
        task_extract = threading.Thread(
            target=threaded_task,
            args=(extract_audio, [video_url], url_dict),
            )
        get_script_run_ctx(task_extract)
        task_extract.start()
        progress_bar(task_extract, "Processing URL...")
        task_extract.join()
        if 'error' in url_dict:
            st.error(f"Error processing audio: {url_dict['error']}")
        audio_file, extract_time = url_dict['result'], url_dict['duration']
        audio_duration = audio_length(audio_file)
        st.session_state.audio = True

    if st.session_state.upload_btn:
        upload_dict = {}
        task_upload = threading.Thread(
            target=threaded_task,
            args=(process_upload, [upload_path], upload_dict),
            )
        get_script_run_ctx(task_upload)
        task_upload.start()
        progress_bar(task_upload, "Processing upload...")
        task_upload.join()
        audio_file, extract_time = upload_dict['result'], upload_dict['duration']
        audio_duration = audio_length(audio_file)
        st.session_state.audio = True

    if st.session_state.audio:
        g2.audio(audio_file)
        g2.caption(f"**Audio Length:** *:green[{audio_duration:.2f}s]*")
        g2.caption(f"**Audio Extraction:** *:blue[{extract_time:.2f}s]*")

        diarize_dict = {}
        task_diarize = threading.Thread(
            target=threaded_task,
            args=(diarize_audio, [audio_file], diarize_dict),
            )
        get_script_run_ctx(task_diarize)
        task_diarize.start()
        progress_bar(task_diarize, "Diarizing audio...")
        task_diarize.join()
        diarize_script, diarize_time = diarize_dict['result'], diarize_dict['duration']
        st.session_state.diarize = True

        if st.session_state.diarize:
            rttm_dict = {}
            scribe_dict = {}
            select_model = st.session_state.w_model.split(maxsplit=1)[0]
            translating = st.session_state.translate
            task_rttm = threading.Thread(
                target=threaded_task,
                args=(parse_rttm, [diarize_script], rttm_dict),
                )
            task_scribe = threading.Thread(
                    target=threaded_task,
                    args=(scribe_audio, [audio_file, select_model, translating], scribe_dict),
                    )
            get_script_run_ctx(task_rttm)
            get_script_run_ctx(task_scribe)
            task_rttm.start()
            task_scribe.start()
            progress_bar(task_rttm, "Generating RTTM...")
            progress_bar(task_scribe, "Whisper transcribing...")
            task_rttm.join()
            task_scribe.join()
            rttm_data, rttm_time = rttm_dict['result'], rttm_dict['duration']
            st.session_state.rttm = rttm_data is not None
            transcript, scribe_time = scribe_dict['result'], scribe_dict['duration']
            language = get_full_language(transcript['language'])
            st.session_state.transcript = True

            if st.session_state.transcript:
                g2.caption(f"**Speaker Diarization:** *:blue[{diarize_time:.2f}s]*")
                align_dict = {}
                task_align = threading.Thread(
                    target=threaded_task,
                    args=(align_script, [transcript, rttm_data, 1.5], align_dict),
                    )
                get_script_run_ctx(task_align)
                task_align.start()
                progress_bar(task_align, "Synchronizing timestamps, aligning text...")
                task_align.join()
                dialogues, align_time = align_dict['result'], align_dict['duration']
                g2.caption(f"**Language:** *:green[{language}]*")
                g2.caption(f"**Whisper Transcription:** *:blue[{scribe_time:.2f}s]*")
                with g2.expander(label="Aligned Transcript:"):
                    for log in dialogues:
                        st.caption(f"{log}\n")
                with g2.expander(label=f"Full Transcript [{select_model}]:"):
                    st.text_area(label=" ", value=transcript['text'].strip(), height=250)
                st.session_state.url_btn, st.session_state.upload_btn = False, False
                with st.expander(label="Summary:"):
                    prompt_text = transcript['text'].strip()
                    st.text_area(label="", value=summarize(prompt_text), height=250)

else:
    if video_url and not url_change(video_url):
        st.error("Invalid URL address.", icon="❗")
    elif not st.session_state.url and not st.session_state.upload:
        st.info("Submit a video URL or upload file to get started!", icon="ℹ️")


####################################################################################################
# with open( "app\style.css" ) as css:
#     st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# Streamlit page declarations
# from st_pages import Page, add_page_title, show_pages
# show_pages(
#     [
#         Page(path="app/Home.py", name="Home", icon="🚀"),
#         Page(path="app/sidebar/tester.py", name="Tester", icon="🔬"),
#     ]
# )
