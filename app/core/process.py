from core.utils import TaskUtility
from yt_dlp import YoutubeDL
from typing import Optional
import streamlit as st
import subprocess
import mimetypes
import glob
import time
import os


tU = TaskUtility()
class AudioProcess:
    SAVE_DIR = ".\\data\\media"

    """[RESAMPLING] -> Reduce audio to mono-channel, resample to 16kHz audio for downstream diarization. (.OGG or .mp3)"""
    @staticmethod
    def mono_resample(input_file_path: str) -> Optional[str]:
        base_name, _ = os.path.splitext(input_file_path)
        output_path = f"{base_name}.OGG"
        ffmpeg_cmds = ["ffmpeg", "-i", input_file_path, "-ar", "16000", "-ac", "1", output_path]
        try:
            subprocess.run(ffmpeg_cmds, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Converted {input_file_path} to mono channel, resampled at 16kHz.")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            return
        except subprocess.TimeoutExpired:
            print(f"FFmpeg command timed out for file: {input_file_path}")
            return
        return output_path

    """[AUDIO FROM VIDEO URL] -> Extract, convert audio from video"""
    def extract_audio(self, video_url: str) -> tuple[str, float]:
        start_time = time.time()

        # Extract and save relevant video info in json
        info_dict, key_info = {}, ['id', 'title', 'webpage_url', 'language', 'thumbnail', 'description', 'uploader', 'uploader_url', 'upload_date']
        with YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            yt_dict = ydl.extract_info(url=video_url, download=False)
        for key in key_info:
            if key in yt_dict:
                info_dict[key] = yt_dict[key]

        video_title = tU.sanitize_name(info_dict.get('title', 'audio'))
        MEDIA_PATH = Path(self.SAVE_DIR) / video_title
        os.makedirs(MEDIA_PATH, exist_ok=True)
        info_file = MEDIA_PATH / "info.json"
        with open(file=info_file, mode='w', encoding='utf-8') as inf:
            json.dump(info_dict, inf, ensure_ascii=True)

        # Check if audio file already exists in the folder
        audio_files = list(MEDIA_PATH.glob('audio*.OGG'))
        if audio_files:
            AUDIO_FILE = str(audio_files[0])
            st.toast(body="Existing audio file found!", icon="✔")
            return AUDIO_FILE, time.time() - start_time
        else:
            # Extract and download audio, convert to mono and resample to 16kHz for Pyannote ingestion
            ytdl_options = {
                'format': 'worstaudio/worst',
                'outtmpl': os.path.join(MEDIA_PATH, 'audio.%(ext)s'),
            }
            try:
                with YoutubeDL(ytdl_options) as ytdl:
                    result = ytdl.extract_info(url=video_url, download=True)
                    AUDIO_PATH = ytdl.prepare_filename(result)
                processed_audio = self.mono_resample(AUDIO_PATH)
                return processed_audio, time.time() - start_time
            except Exception as e:
                raise Exception(f"Error extracting audio: {e}")


    """[AUDIO FROM UPLOAD] -> Identify, then process upload file for audio extraction"""
    def process_upload(self, file_path: str) -> tuple[str, float]:
        start_time = time.time()
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith("audio"):
            processed_audio = self.mono_resample(file_path)
            return processed_audio, time.time() - start_time
        elif mime_type and mime_type.startswith("video"):
            return self.extract_audio(file_path)
        else:
            raise ValueError("Unsupported file type")


from pyannote.audio import Pipeline
from core.utils import TaskUtility
from langcodes import Language
from pathlib import Path
import whisper
import openai
import torch
import json


class AudioTransform:
    tU = TaskUtility()
    devices = torch.device("cuda" if tU.has_cuda() else "cpu")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=st.session_state['hf_access_token'])

    """[SPEAKER DIARIZATION] => Partition audio stream to id speaker segments, generate rich transcription time marked (RTTM)
    Note: Use 'speaker-diarization@2.1' as a fallback. Version 3.1 can now utilize cuda devices (GPU)."""
    def diarize_audio(self, audio_path) -> tuple[str, float]:
        start_time = time.time()
        MEDIA_DIR = Path(audio_path).parent
        rttm_output = MEDIA_DIR / "speakers.rttm"
        # Check if RTTM file already exists
        if rttm_output.exists():
            st.toast(body="Existing RTTM found!", icon="✔")
            return rttm_output, time.time() - start_time
        else:
            try:
                self.pipeline.to(self.devices)
                diarization = self.pipeline(audio_path)
                with open(rttm_output, "w") as rttm:
                    diarization.write_rttm(rttm)
                return rttm_output, time.time() - start_time
            except Exception as e:
                st.error(body=f"Error during diarization: {e}")
                raise Exception(f"Error during diarization: {e}")


    """[RTTM PARSING] -> Isolate speaker_ids and timestamps"""
    @staticmethod
    def parse_rttm(file_path: str) -> tuple[list, float]:
        start = time.time()

        with open(file_path, "r") as rttm:
            lines = rttm.readlines()

        rttm_log = []
        for line in lines:
            part = line.strip().split()
            speaker, time_start, duration = part[7], part[3], part[4]
            rttm_log.append((speaker, time_start, duration))

        return rttm_log, time.time() - start

    """"[LANGUAGE ID] -> Converts language code to full language name"""
    @staticmethod
    def get_full_language(lang_code: str) -> str:
        language = Language.get(lang_code)
        return language.display_name()

    """[WHISPER TRANSCRIBING] -> Use OpenAI's whisper model to transcribe (+/- translate) audio to readable text"""
    def scribe_audio(self, file_path: str, model_name: str, translate: bool) -> tuple[dict, float]:
        start_time = time.time()
        SCRIPT_PATH = os.path.join(os.path.dirname(file_path), 'transcript.json')
        # Load or initialize list of transcripts
        try:
            with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
                transcripts = json.load(f)
            if not isinstance(transcripts, list):
                transcripts = []
        except (FileNotFoundError, json.JSONDecodeError):
            transcripts = []
        # Check for existing transcripts
        for entry in transcripts:
            if entry['model'] == model_name:
                return entry['full_script'], time.time() - start_time
        # Whisper transcription setup parameters
        whisper_model = whisper.load_model(name=model_name, device=self.devices)
        decode_lang = 'translate' if translate else None
        script = whisper_model.transcribe(audio=file_path, word_timestamps=True, task=decode_lang)
        lang = script['language'] if translate else None
        new_script = {
            'model': model_name,
            'translated': lang,
            'full_script': script,
        }
        transcripts.append(new_script)
        # Write updated transcripts back to transcript.json file
        with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
            json.dump(transcripts, f, ensure_ascii=True)
        return script, time.time() - start_time


    """[TRANSCRIPT ALIGNMENT] -> Synchronize, then align timestamps with speaker_ids + text
    Note: Whisper's generated timestamps are often times inaccurate and differ from their Pyannote counterpart.
    This is just a quick and dirty method of generating more accurate timestamps through comparisons, tempered by tolerance level."""
    def align_script(self, transcript: dict, rttm_data: list, tolerance: float = 1.5) -> tuple[list, float]:
        exec_start = time.time()
        sentences = []
        for segment in transcript['segments']:
            script_start = round(float(segment['start']), 2)
            top_speaker = None

            for speaker_id, start_time, duration in rttm_data:
                rttm_start = round(float(start_time), 2)
                rttm_end = round((float(start_time) + float(duration)), 2)

                if rttm_start - tolerance <= script_start <= rttm_end + tolerance:
                    top_speaker = speaker_id
                    break
            if top_speaker is not None:
                hms_time = tU.format_timestamp(script_start if abs(abs(script_start - rttm_start) - tolerance) > 0.5 else rttm_start)
                sentences.append(f":gray[({hms_time})] **{top_speaker}**: {segment['text']}")
        return sentences, time.time() - exec_start

    """[SUMMARIZATION] -> Generate a summary in JSON format via a gpt model from full transcript text"""
    def summarize(self,transcript_text: str) -> str:
        client = openai.OpenAI(api_key=st.session_state['openai_api_key'])
        context = "You are skilled in summarizing ideas/concepts from audio/video transcripts in JSON output: { 'summary': <summary here> }"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": f"Summarize the following text:\n{transcript_text}"}
            ],
            max_tokens=300,
        )
        json_res = response.choices[0].message.content
        summary = json.loads(json_res)['summary']
        return summary
