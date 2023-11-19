import streamlit as st

models = ["tiny", "base", "small", "medium", "large"]
vrams = ["1 GB", "1 GB", "2 GB", "5 GB", "10 GB"]
display_models = [f"{model} ({vram})" for model, vram in zip(models, vrams)]

def whisper_map(model: str, use_english: bool) -> str:
    base_model, *vram = model.replace('.en', '').split(maxsplit=1)
    return f"{base_model}{'.en' if use_english else ''} {''.join(vram)}"

def update_display():
    global display_models
    display_models = [f"{model}{'.en' if st.session_state.english else ''} ({vram})" for model, vram in zip(models, vrams)]

def toggle_en():
    st.session_state.english = not st.session_state.english
    if st.session_state.english:
        if st.session_state.translate:
            st.session_state.translate = False
    update_display()
    st.session_state.w_model = whisper_map(st.session_state.w_model, st.session_state.english)

def toggle_trans():
    st.session_state.translate = not st.session_state.translate
    if st.session_state.translate:
        if st.session_state.english:
            toggle_en()

def model_params(model: str) -> (int | None):
    base_model = model.split(maxsplit=1)[0].replace('.en', '')
    params = {
        'tiny': 39,
        'base': 74,
        'small': 244,
        'medium': 769,
        'large': 1550,
    }
    return params.get(base_model)

def model_param_delta() -> (str | None):
    delta = st.session_state.param1 - st.session_state.param0
    return f"{delta} M" if delta != 0 else None

def model_speeds(model: str) -> (str | None):
    base_model = model.split(maxsplit=1)[0].replace('.en', '')
    speeds = {
        'tiny': 32,
        'base': 16,
        'small': 6,
        'medium': 2,
        'large': 1,
    }
    return speeds.get(base_model)

def model_speed_delta() -> (str | None):
    delta = st.session_state.speed1 - st.session_state.speed0
    return f"{delta}x" if delta != 0 else None

def model_switch():
    st.session_state.whisp = whisper_map(st.session_state.w_model, st.session_state.english)
    st.session_state.param0, st.session_state.speed0  = st.session_state.param1, st.session_state.speed1
    st.session_state.param1, st.session_state.speed1 = model_params(st.session_state.whisp), model_speeds(st.session_state.whisp)
