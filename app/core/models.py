from typing import Optional
import streamlit as st


class ModelSelect:
    models = ["tiny", "base", "small", "medium", "large"]
    vrams = ["1 GB", "1 GB", "2 GB", "5 GB", "10 GB"]

    def __init__(self) -> None:
        self.selection = [f"{model} ({vram})" for model, vram in zip(self.models, self.vrams)]

    def whisper_map(self, model: str, use_english: bool) -> str:
        base_model, *vram = model.replace('.en', '').split(maxsplit=1)
        return f"{base_model}{'.en' if use_english else ''} {''.join(vram)}"

    def update_display(self) -> list[str]:
        global selection
        selection = [f"{model}{'.en' if st.session_state.english else ''} ({vram})" for model, vram in zip(self.models, self.vrams)]
        return selection

    def toggle_en(self) -> None:
        st.session_state.english = not st.session_state.english
        if st.session_state.english:
            if st.session_state.translate:
                st.session_state.translate = False
        self.update_display()
        st.session_state.w_model = self.whisper_map(st.session_state.w_model, st.session_state.english)

    def toggle_trans(self) -> None:
        st.session_state.translate = not st.session_state.translate
        if st.session_state.translate:
            if st.session_state.english:
                self.toggle_en()

    @staticmethod
    def model_params(model: str) -> Optional[int]:
        base_model = model.split(maxsplit=1)[0].replace('.en', '')
        params = {
            'tiny': 39,
            'base': 74,
            'small': 244,
            'medium': 769,
            'large': 1550,
        }
        return params.get(base_model)

    @staticmethod
    def model_param_delta() -> Optional[str]:
        delta = st.session_state.param1 - st.session_state.param0
        return f"{delta} M" if delta != 0 else None

    @staticmethod
    def model_speeds(model: str) -> Optional[str]:
        base_model = model.split(maxsplit=1)[0].replace('.en', '')
        speeds = {
            'tiny': 32,
            'base': 16,
            'small': 6,
            'medium': 2,
            'large': 1,
        }
        return speeds.get(base_model)

    @staticmethod
    def model_speed_delta() -> Optional[str]:
        delta = st.session_state.speed1 - st.session_state.speed0
        return f"{delta}x" if delta != 0 else None

    def model_switch(self) -> None:
        st.session_state.whisp = self.whisper_map(st.session_state.w_model, st.session_state.english)
        st.session_state.param0, st.session_state.speed0  = st.session_state.param1, st.session_state.speed1
        st.session_state.param1, st.session_state.speed1 = self.model_params(st.session_state.whisp), self.model_speeds(st.session_state.whisp)
