import os
import time
import GPUtil
import streamlit as st

gpu = GPUtil.getGPUs()[0]

def threaded_task(func, args, result_dict):
    try:
        result, duration = func(*args)
        result_dict['result'], result_dict['duration'] = result, duration
    except Exception as e:
        result_dict['error'] = str(e)
        print(f"Error in threaded_task: {e}")


def progress_bar(task_thread, task_text, update_interval=0.1):
    bar = st.progress(0, text=task_text)
    percent = 0
    while task_thread.is_alive():
        time.sleep(update_interval)
        percent += 1
        bar.progress(min(percent, 100), text=task_text)
    bar.empty()


def format_timestamp(seconds):
    minute = int(seconds // 60)
    whole_sec = int(seconds)
    millisec = int((seconds - whole_sec) * 1000)
    return f"{minute:02d}:{whole_sec % 60:02d}:{millisec:03d}"


def delete_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
