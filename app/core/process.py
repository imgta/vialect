from moviepy.editor import AudioFileClip
from core.utils import TaskUtility
from pydub import AudioSegment
from yt_dlp import YoutubeDL
from typing import Optional
import subprocess
import mimetypes
import glob
import time
import os


tU = TaskUtility()
class AudioProcess:
    SAVE_DIR = ".\\data\\media"
    """[WAV CONVERT] -> Convert an audio file to WAV format (for pyannote.audio) using ffmpeg."""
    @staticmethod
    def convert_to_wav(input_file_path: str) -> Optional[str]:
        base_file, _ = os.path.splitext(input_file_path)
        wav_file_path = base_file + ".wav"
        ffmpeg_cmds = ["ffmpeg", "-i", input_file_path, "-ar", "16000", "-ac", "1", wav_file_path]
        try:
            subprocess.run(ffmpeg_cmds, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Converted {input_file_path} to {wav_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")
            return None
        return wav_file_path

    """[AUDIO FROM VIDEO URL] -> Extract, convert audio from video"""
    def extract_audio(self, url: str, save_dir: str = SAVE_DIR) -> tuple[str, float]:
        start_time = time.time()
        # Fetch video info without downloading
        with YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
        # Sanitize video title, create folder path
        video_title = tU.sanitize_name(info_dict.get('title', 'audio'))
        audio_folder_path = os.path.join(save_dir, video_title)
        os.makedirs(audio_folder_path, exist_ok=True)
        # Check if an audio file already exists in the folder
        existing_files = glob.glob(os.path.join(audio_folder_path, 'audio.wav'))
        if existing_files:
            audio_file_path = existing_files[0]
            duration = time.time() - start_time
            return audio_file_path, duration
        # Download audio file from video
        audio_file_path_template = os.path.join(audio_folder_path, 'audio.%(ext)s')
        with YoutubeDL({'format': 'worstaudio/worst', 'outtmpl': audio_file_path_template}) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict)
        # Convert audio to WAV if not already in WAV format
        if not audio_file_path.endswith('.wav'):
            audio_file_path = self.convert_to_wav(audio_file_path)
        duration = time.time() - start_time
        return audio_file_path, duration

    """[AUDIO FROM UPLOAD] -> Identify, then process upload file for audio extraction"""
    def process_upload(self, file_path: str) -> tuple[str, float]:
        start_time = time.time()
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith("audio"):
            audio = AudioSegment.from_file(file_path)
            wav_file = file_path.rsplit('.', 1)[0] + '.wav'
            audio.export(wav_file, format='wav')
            duration = time.time() - start_time
            return wav_file, duration
        elif mime_type and mime_type.startswith("video"):
            return self.extract_audio(file_path)
        else:
            raise ValueError("Unsupported file type")

    """[AUDIO LENGTH] -> Fetch duration of audio"""
    @staticmethod
    def audio_length(file_path: str) -> float:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
        clip = AudioFileClip(file_path)
        return clip.duration


from pyannote.audio import Pipeline
from langcodes import Language
import streamlit as st
import openai
import whisper
import torch
import json


class AudioTransform:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    hf_token = st.secrets["HUGGING_FACE_TOKEN"]
    devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token).to(devices)

    """[SPEAKER DIARIZATION] => Partition audio stream into speaker_id segments, generate rich transcription time marked (RTTM)
    Note: Use 'speaker-diarization@2.1' as a fallback. Version 3.1 can now utilize cuda devices (GPU)."""
    def diarize_audio(self, file_path: str) -> tuple[str, float]:
        start_time = time.time()
        # Perform speaker diarization
        diarization = self.pipeline(file_path, num_speakers=2)
        # Generate RTTM output path
        audio_folder_path = os.path.dirname(file_path)
        rttm_output = os.path.join(audio_folder_path, "speakers.rttm")
        # Check if RTTM has already been generated
        existing_rttm = glob.glob(os.path.join(audio_folder_path, 'speakers.rttm'))
        if existing_rttm:
            duration = time.time() - start_time
            return rttm_output, duration
        with open(rttm_output, "w") as rttm_file:
            diarization.write_rttm(rttm_file)
        duration = time.time() - start_time
        return rttm_output, duration

    """[RTTM PARSING] -> Isolate speaker_ids and timestamps"""
    @staticmethod
    def parse_rttm(file_path: str) -> tuple[list, float]:
        start = time.time()
        with open(file_path, "r") as rttm:
            lines = rttm.readlines()
        rttm_log = []
        for line in lines:
            parts = line.strip().split()
            speaker_id = parts[7]
            start_time = parts[3]
            duration = parts[4]
            rttm_log.append((speaker_id, start_time, duration))
        end_time = time.time() - start
        return rttm_log, end_time

    """"[LANGUAGE ID] -> Converts language code to full language name"""
    @staticmethod
    def get_full_language(lang_code: str) -> str:
        language = Language.get(lang_code)
        return language.display_name()

    """[WHISPER TRANSCRIBING] -> Use OpenAI's whisper model to transcribe (+/- translate) audio to readable text"""
    def scribe_audio(self, file_path: str, model_name: str, translate: bool) -> tuple[dict, float]:
        start_time = time.time()
        model = whisper.load_model(name=model_name, device=self.devices)
        script = model.transcribe(audio=file_path, word_timestamps=True)
        if translate and script['language'] != 'en':
            script = model.transcribe(
                audio=file_path,
                word_timestamps=True,
                task="translate",
                )
        new_transcript_entry = {
            'model': model_name,
            'text': script['text'].strip()
        }
        transcript_path = os.path.join(os.path.dirname(file_path), 'transcript.json')
        try: # Load or initialize list of transcripts
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcripts = json.load(f)
                if not isinstance(transcripts, list):
                    raise ValueError("Invalid format in transcript.json")
        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            transcripts = []
        for entry in transcripts: # Update or append new transcript entry
            if entry['model'] == model_name:
                entry['text'] = new_transcript_entry['text']
                break
        else:
            transcripts.append(new_transcript_entry)
        # Write transcript data to JSON
        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(transcripts, f, ensure_ascii=False, indent=4)
        duration = time.time() - start_time
        return script, duration

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
                hms_rttm = tU.format_timestamp(rttm_start)
                hms_script = tU.format_timestamp(script_start)
                if abs(abs(script_start - rttm_start) - tolerance) < 0.5:
                    sentences.append(f":gray[({hms_rttm})] **{top_speaker}**: {segment['text']}")
                else:
                    sentences.append(f":gray[({hms_script})] **{top_speaker}**: {segment['text']}")
        duration = time.time() - exec_start
        return sentences, duration

    """[SUMMARIZATION] -> Generate a summary via a gpt model based on the full transcript"""
    def summarize(self,transcript_text: str) -> str:
        client = openai.OpenAI()
        context = "You are an instructive assistant, skilled in summarizing ideas/concepts from audio/video transcripts in JSON output: { 'summary': <summary here> }"
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
