import os
import threading

import streamlit as st
from streamlit_extras.row import row
from streamlit_player import st_player
from streamlit_extras.grid import grid
from streamlit.runtime.scriptrunner import get_script_run_ctx

from config import page_cfg
from layout.render import set_layout
from core.models import ModelSelect
from core.utils import TaskUtility, Inputs
from core.states import init_session_states
from core.process import AudioProcess, AudioTransform
tU, inP, mS, aP, aT = TaskUtility(), Inputs(), ModelSelect(), AudioProcess(), AudioTransform()

####################################################################################################
st.set_page_config(**page_cfg())
set_layout()
init_session_states()

####################################################################################################
h1 = row([5], vertical_align="bottom")
c0, c1, c2, c3 = h1.columns([4.1, 0.25, 1.4, 2.5])
h2 = row([1, 4], vertical_align="top")

whisper_model = c0.selectbox(
    label="Whisper model :gray[(req. VRAM)]:",
    options=mS.update_display(),
    key="w_model",
    on_change=mS.model_switch,
    help="Smaller models are faster, but larger models offer more accuracy.",
)

en_mode = h2.checkbox(
    label="English",
    value=st.session_state.english,
    on_change=mS.toggle_en,
    help="Noticeable performance bumps when using tiny.en or base.en in English-only use cases.",
)
lang_mode = h2.checkbox(
    label="Translate",
    value=st.session_state.translate,
    on_change=mS.toggle_trans,
    help="Detects and translates language to English.",
)

c1.empty()
c2.metric(
    label="Parameters",
    value=f"{mS.model_params(st.session_state.whisp)}M",
    delta=mS.model_param_delta(),
    help="High parameter counts can lead to higher accuracy.",
)
c3.metric(
    label="Speed",
    value=f"{mS.model_speeds(st.session_state.whisp)}x",
    delta=mS.model_speed_delta(),
    help="Inference speeds (relative) decrease as model sizes grow.",
)

g1 = grid([4,1], [4,1], [4,1], [4,1], vertical_align="bottom")
video_url = g1.text_input(label="Enter a video URL:", placeholder="YouTube, Vimeo, Dailymotion, etc.") if not st.session_state.upload_btn else g1.empty()
if video_url:
    if inP.url_change(video_url):
        url_btn = g1.button(label="Submit URL", on_click=inP.url_submit, use_container_width=True)
    else:
        g1.empty()
else:
    g1.empty()

if st.session_state.url:
    st.session_state.url_btn = True
    st_player(url=video_url)

upload_file = g1.file_uploader(label="Upload video or audio:", type=['wav', 'mp3', 'ogg', 'mp4', 'mkv', 'avi', 'mov', 'flv'], on_change=inP.upload_change, label_visibility=inP.upload_label()) if not st.session_state.url_btn else g1.empty()
if upload_file and not st.session_state.url_btn:
    g1.empty()
    upload_btn = g1.button(label="Submit File", on_click=inP.upload_submit, use_container_width=True)
else:
    g1.empty()

if st.session_state.upload:
    st.session_state.upload_btn = True
    max_size_mb = 200
    file_size_mb = upload_file.size / (1024**2)
    if file_size_mb > max_size_mb:
        st.error(f"File size exceeds the maximum limit of {max_size_mb} MB.")
    else:
        upload_path = os.path.join(aP.SAVE_DIR, upload_file.name)
        with open(upload_path, "wb") as f:
            f.write(upload_file.getbuffer())

g2 = grid([5], [1.1, 1.35, 1.2, 1.4], [5], [5], 1, 1, 1, vertical_align="center")
if st.session_state.url_btn or st.session_state.upload_btn:
    if st.session_state.url_btn:
        url_dict = {}
        task_extract = threading.Thread(
            target=tU.threaded_task,
            args=(aP.extract_audio, [video_url], url_dict),
            )
        get_script_run_ctx(task_extract)
        task_extract.start()
        tU.progress_bar(task_extract, "Processing URL...")
        task_extract.join()
        if 'error' in url_dict:
            st.error(f"Error processing audio: {url_dict['error']}")
        audio_file, extract_time = url_dict['result'], url_dict['duration']
        audio_duration = aP.audio_length(audio_file)
        st.session_state.audio = True

    if st.session_state.upload_btn:
        upload_dict = {}
        task_upload = threading.Thread(
            target=tU.threaded_task,
            args=(aP.process_upload, [upload_path], upload_dict),
            )
        get_script_run_ctx(task_upload)
        task_upload.start()
        tU.progress_bar(task_upload, "Processing upload...")
        task_upload.join()
        audio_file, extract_time = upload_dict['result'], upload_dict['duration']
        audio_duration = aP.audio_length(audio_file)
        st.session_state.audio = True

    if st.session_state.audio:
        g2.audio(audio_file)
        g2.caption(f"**Audio Extraction:** *:blue[{extract_time:.2f}s]*")

        diarize_dict = {}
        task_diarize = threading.Thread(
            target=tU.threaded_task,
            args=(aT.diarize_audio, [audio_file], diarize_dict),
            )
        get_script_run_ctx(task_diarize)
        task_diarize.start()
        tU.progress_bar(task_diarize, "Diarizing audio...")
        task_diarize.join()
        diarize_script, diarize_time = diarize_dict['result'], diarize_dict['duration']
        st.session_state.diarize = True

        if st.session_state.diarize:
            rttm_dict = {}
            scribe_dict = {}
            select_model = st.session_state.w_model.split(maxsplit=1)[0]
            translating = st.session_state.translate
            task_rttm = threading.Thread(
                target=tU.threaded_task,
                args=(aT.parse_rttm, [diarize_script], rttm_dict),
                )
            task_scribe = threading.Thread(
                    target=tU.threaded_task,
                    args=(aT.scribe_audio, [audio_file, select_model, translating], scribe_dict),
                    )
            get_script_run_ctx(task_rttm)
            get_script_run_ctx(task_scribe)
            task_rttm.start()
            task_scribe.start()
            tU.progress_bar(task_rttm, "Generating RTTM...")
            tU.progress_bar(task_scribe, "Whisper transcribing...")
            task_rttm.join()
            task_scribe.join()
            rttm_data, rttm_time = rttm_dict['result'], rttm_dict['duration']
            st.session_state.rttm = rttm_data is not None
            transcript, scribe_time = scribe_dict['result'], scribe_dict['duration']
            language = aT.get_full_language(transcript['language'])
            st.session_state.transcript = True

            if st.session_state.transcript:
                g2.caption(f"**Speaker Diarization:** *:blue[{diarize_time:.2f}s]*")
                align_dict = {}
                task_align = threading.Thread(
                    target=tU.threaded_task,
                    args=(aT.align_script, [transcript, rttm_data, 1.5], align_dict),
                    )
                get_script_run_ctx(task_align)
                task_align.start()
                tU.progress_bar(task_align, "Synchronizing timestamps, aligning text...")
                task_align.join()
                dialogues, align_time = align_dict['result'], align_dict['duration']
                g2.caption(f"**Language:** *:green[{language}]*")
                g2.caption(f"**Whisper Transcription:** *:blue[{scribe_time:.2f}s]*")
                with g2.expander(label="Aligned Transcript:"):
                    for log in dialogues:
                        st.caption(f"{log}\n")
                with g2.expander(label=f"Full Transcript [{select_model}]:"):
                    st.text_area(label=" ", value=transcript['text'].strip(), height=250)
                with st.expander(label="Summary:"):
                    prompt_text = transcript['text'].strip()
                    st.text_area(label="", value=aT.summarize(prompt_text), height=250)

else:
    if video_url and not inP.url_change(video_url):
        st.error("Invalid URL address.", icon="❗")
    elif not st.session_state.url and not st.session_state.upload:
        st.info("Submit a video URL or upload file to get started!", icon="ℹ️")
####################################################################################################
