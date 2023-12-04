from typing import Callable, Literal, Any
from datetime import datetime
from threading import Thread
import streamlit as st
import validators
import base64
import GPUtil
import torch
import time


class TaskUtility:
    gpu_device = GPUtil.getGPUs()[0]

    @staticmethod
    def has_cuda():
        return torch.cuda.is_available()

    @staticmethod
    def threaded_task(func: Callable, args: tuple, result_dict: dict[str, Any]) -> None:
        """[THREADING TASKS] -> Execute tasks in parallel and asynchronously collect results."""
        try:
            result, duration = func(*args)
            result_dict["result"], result_dict["duration"] = result, duration
        except Exception as e:
            result_dict["error"] = str(e)
            print(f"Error in threaded_task: {e}")

    @staticmethod
    def progress_bar(
        task_thread: Thread, task_text: str, update_interval: float = 0.1
    ) -> None:
        """[PROGRESS DISPLAY] -> Create and manage Streamlit progress bar for better processing feedback."""
        bar = st.progress(0, text=task_text)
        percent = 0
        while task_thread.is_alive():
            time.sleep(update_interval)
            percent += 1
            bar.progress(min(percent, 100), text=task_text)
        bar.empty()

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """[TIMESTAMP FORMATTING] -> Converts diarized speaker timestamps from seconds into a more readable min:sec:ms timestamp format."""
        minute = int(seconds // 60)
        whole_sec = int(seconds)
        millisec = int((seconds - whole_sec) * 1000)
        return f"{minute:02d}:{whole_sec % 60:02d}:{millisec:03d}"

    @staticmethod
    def sanitize_name(title: str, max_length: int = 200) -> str:
        """[SANITIZE DIRECTORY NAME] -> Replace all non-alphanumeric characters with _, limit character length."""
        sanitized = "".join("_" if not char.isalnum() else char for char in title)
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        return sanitized

    @staticmethod
    def img_base64(img_path: str) -> str:
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    @staticmethod
    def format_upload_date(date_str: str):
        return datetime.strptime(date_str, "%Y%m%d").strftime("%B %d, %Y")

    @staticmethod
    def truncate_str(str, max_len):
        return (f"{str[:max_len]}...") if len(str) > max_len else str

class Inputs:
    """"[URL ADDRESS VALIDATION]"""
    @staticmethod
    def url_change(url: str) -> bool:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return validators.url(url)

    @staticmethod
    def url_submit() -> None:
        st.session_state.upload_btn = False
        st.session_state.url_btn = True

    @staticmethod
    def upload_change() -> None:
        st.session_state.attached = not st.session_state.attached

    @staticmethod
    def upload_label() -> Literal['visible', 'collapsed']:
        return "visible" if not st.session_state.attached else "collapsed"

    @staticmethod
    def upload_submit() -> None:
        st.session_state.url_btn = False
        st.session_state.upload_btn = True
