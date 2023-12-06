<h1 align="center">👾 V/ALect</h1>

<div align="center">
    <a href="https://github.com/imgta/vialect/search?l=python" target="_blank">
        <img src="https://img.shields.io/github/languages/top/imgta/vialect" alt="Top Language"/>
    </a>
    <a href="https://github.com/imgta/vialect/commits/main" target="_blank">
        <img src="https://img.shields.io/github/last-commit/imgta/vialect" alt="Last Commit"/>
    </a>
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/imgta/vialect?label=size&color=6d3fc0">
</div>
<p align="center"><strong><em>ViaLect</strong> streamlines your media intake by transforming audio into workable text and generated summaries!</em></p>
<div align="center">
    
$`\textcolor{gray}{\textit{Toward words unheard,}}`$<br>
$`\textcolor{gray}{\textit{traverse digital oceans}}`$<br>
$`\textcolor{gray}{\textit{for treasures unseen.}}`$

</div>

## Features:
**Key Packages:**  [OpenAI Whisper](https://github.com/openai/whisper), [PyTorch (CUDA v11.8)](https://pytorch.org/get-started/locally/), [pyannote.audio](https://github.com/pyannote/pyannote-audio), [yt-dlp](https://github.com/yt-dlp/yt-dlp), [Streamlit](https://github.com/streamlit/streamlit)

>📡 **Audio Extraction:** Pull from various video platforms  
🛸 **ASR & Diarization:** ID speakers with timestamps  
🌎 **Translation:** Detect and translate languages to English  
🤖 **Transcribing:** Speech-to-text from extracted audio  
💬 **Summarization:** Generate summaries based on transcript  
🚀 **Intuitive UI:** Seamless frontend layout via Streamlit

![vialect_ss](https://github.com/imgta/vialect/assets/126015138/bed7b8c4-2994-4a2f-82e4-ee2636194d22)

## Setup:
1. Git clone this repository:
```console
git clone https://github.com/imgta/vialect.git
```
2. Install ffmpeg and requirements:
```console
sudo apt install ffmpeg
pip install -r requirements.txt
```
3. Obtain Hugging Face [token/access](https://huggingface.co/pyannote/speaker-diarization-3.1), obtain [OpenAI API Key](https://platform.openai.com/api-keys)
4. Create and update `.streamlit/secrets.toml` (example provided)
5. Launch streamlit app:
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
