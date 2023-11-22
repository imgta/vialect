# 👾 V/ALect
![Top Language](https://img.shields.io/github/languages/top/imgta/vialect)
![Last Commit](https://img.shields.io/github/last-commit/imgta/vialect)

**Vialect** _transforms video/audio media into workable, transcribed text._

> <div style="text-align: center; font-style: italic;">
With whispers unheard,<br>
traverse digital oceans<br>
for treasures unseen.
</div>

## Features
**Processing Pipeline:**  [yt-dlp](https://github.com/yt-dlp/yt-dlp), [Pyannote Audio](https://github.com/pyannote/pyannote-audio), [OpenAI Whisper](https://github.com/openai/whisper)
- Audio extraction from various video platforms
- ASR + Diarization for speaker identification
- Language detection and translation
- Speech-to-text audio transcribing
- Transcription-based summary generation

### Setup:
1. Install ffmpeg and requirements:
```console
sudo apt install ffmpeg
pip install -r requirements.txt
```
2. Obtain Hugging Face [token/access](https://huggingface.co/pyannote/speaker-diarization-3.1), obtain [OpenAI API Key](https://platform.openai.com/api-keys)
3. Create and update `.streamlit/secrets.toml` with keys (example provided)
4. Launch streamlit app:
```console
streamlit run app/Home.py
```

### Usage:
1. Select whisper model and options
2. Input or upload video/audio file
3. Submit for transcription

### TODO:
- [x] Generate summary based on transcript text
- [ ] ASR/Diarization for timestamps => reduced sliding window
- [ ] Partition overlap + translation stress test _(Anime subbing?)_
- [ ] Realtime ASR
