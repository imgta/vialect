<h1 align="center">👾 V/ALect</h1>

<div align="center">
    <a href="https://github.com/imgta/vialect/search?l=python" target="_blank">
        <img src="https://img.shields.io/github/languages/top/imgta/vialect" alt="Top Language"/>
    </a>
        <a href="https://github.com/imgta/vialect/commits/main" target="_blank">
        <img src="https://img.shields.io/github/last-commit/imgta/vialect" alt="Last Commit"/>
    </a>
</div>

<p align="center"><em>Streamline your media by transforming audio into workable text and summaries!</em></p>

><div align="center"><em>To whispers unheard,<br>traverse digital oceans<br>for treasures unseen.</em></div>


## Features:
**Processing Pipeline:**  [yt-dlp](https://github.com/yt-dlp/yt-dlp), [Pyannote Audio](https://github.com/pyannote/pyannote-audio), [OpenAI Whisper](https://github.com/openai/whisper)

📡 **Audio Extraction:** Pull from various video platforms  
🛸 **ASR & Diarization:** ID speakers with timestamps  
🌎 **Translation:** Detect and translate languages to English  
🤖 **Transcribing:** Speech-to-text from extracted audio  
💬 **Summarization:** Generate summaries based on transcript  

## Setup:
1. Install ffmpeg and requirements:
```console
sudo apt install ffmpeg
pip install -r requirements.txt
```
2. Obtain Hugging Face [token/access](https://huggingface.co/pyannote/speaker-diarization-3.1), obtain [OpenAI API Key](https://platform.openai.com/api-keys)
3. Create and update `.streamlit/secrets.toml` (example provided)
4. Launch streamlit app:
```console
streamlit run app/Home.py
```

## Usage:
1. Select whisper model and options
2. Input or upload video/audio file
3. Submit for transcription

### Roadmap:
- [x] Generate summary based on transcript text
- [ ] Create and store text embeddings in vector DB for RAG querying
- [ ] ASR/Diarization for timestamps => reduced sliding window
- [ ] Partition overlap + translation stress test _(Anime subbing?)_
- [ ] Realtime ASR
