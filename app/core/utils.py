from typing import Callable, Literal, Any
from threading import Thread
import streamlit as st
import validators
import GPUtil
import torch
import time


class TaskUtility:
    gpu_device = GPUtil.getGPUs()[0]

    @staticmethod
    def has_cuda():
        return torch.cuda.is_available()

    """[THREADING TASKS] -> Execute tasks in parallel and asynchronously collect results."""
    @staticmethod
    def threaded_task(func: Callable, args: tuple, result_dict: dict[str, Any]) -> None:
        try:
            result, duration = func(*args)
            result_dict["result"], result_dict["duration"] = result, duration
        except Exception as e:
            result_dict["error"] = str(e)
            print(f"Error in threaded_task: {e}")

    """[PROGRESS DISPLAY] -> Create and manage Streamlit progress bar for better processing feedback."""
    @staticmethod
    def progress_bar(
        task_thread: Thread, task_text: str, update_interval: float = 0.1
    ) -> None:
        bar = st.progress(0, text=task_text)
        percent = 0
        while task_thread.is_alive():
            time.sleep(update_interval)
            percent += 1
            bar.progress(min(percent, 100), text=task_text)
        bar.empty()

    """[TIMESTAMP FORMATTING] -> Converts seconds into a more readable min:sec:ms timestamp format."""
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        minute = int(seconds // 60)
        whole_sec = int(seconds)
        millisec = int((seconds - whole_sec) * 1000)
        return f"{minute:02d}:{whole_sec % 60:02d}:{millisec:03d}"

    """[SANITIZE DIRECTORY NAME] -> Replace all non-alphanumeric characters with _, limit character length."""
    @staticmethod
    def sanitize_name(title: str, max_length: int = 200) -> str:
        sanitized = "".join("_" if not char.isalnum() else char for char in title)
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        return sanitized


class Inputs:
    """"[URL ADDRESS VALIDATION]"""
    @staticmethod
    def url_change(url: str) -> bool:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return validators.url(url)

    @staticmethod
    def url_submit() -> None:
        st.session_state.url = True

    @staticmethod
    def upload_change() -> None:
        st.session_state.attached = not st.session_state.attached

    @staticmethod
    def upload_label() -> Literal['visible', 'collapsed']:
        return "visible" if not st.session_state.attached else "collapsed"

    @staticmethod
    def upload_submit() -> None:
        st.session_state.upload = True
