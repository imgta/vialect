<h1 align="center">👾 V/ALect</h1>

<div align="center">
    <a href="https://github.com/imgta/vialect/search?l=python" target="_blank">
        <img src="https://img.shields.io/github/languages/top/imgta/vialect" alt="Top Language"/>
    </a>
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/imgta/vialect?label=commits&color=6d3fc0">
    <a href="https://github.com/imgta/vialect/commits/main" target="_blank">
        <img src="https://img.shields.io/github/last-commit/imgta/vialect" alt="Last Commit"/>
    </a>
</div>
<p align="center"><strong><em>ViaLect</strong> streamlines your media intake by transforming audio into workable text and generated summaries!</em></p>
<div align="center">
    
$`\textcolor{gray}{\textit{Toward words unheard,}}`$<br>
$`\textcolor{gray}{\textit{traverse digital oceans}}`$<br>
$`\textcolor{gray}{\textit{for treasures unseen.}}`$

</div>

## Features:
> [!TIP]
> 📡 **Audio Extraction &rarr;** Pull from various media platforms or uploads  
> 🛸 **ASR & Diarization &rarr;** Identify and align speakers to timestamped dialogues  
> 🌎 **Translation &rarr;** Detect languages and translate to English  
> 🤖 **Speech-to-Text &rarr;** Accurately transcribe text from extracted audio  
> 💬 **Summarization &rarr;** Focus on key concepts with transcript-based summaries  
> 🔊 **Text-to-Speech &rarr;** Have your generated summaries read back to you  
> 📚 **Media Collection &rarr;** Locally store and navigate your transformed data  
> 🚀 **Intuitive UI &rarr;** Seamless frontend layout via Streamlit  
> > ![vialect_0](https://github.com/imgta/vialect/assets/126015138/38ad4715-e942-4ff1-bc9c-34b8bc102d81)  
> > <details><summary>more</summary>
> > 
> > ![vialect_medias](https://github.com/imgta/vialect/assets/126015138/6f44a528-0b6f-485f-9ed2-91269810a1ad)
> > 
> > </details>


## Setup:
> [!IMPORTANT]
> _**Key Packages:**  [OpenAI Whisper](https://github.com/openai/whisper), [PyTorch (CUDA v11.8)](https://pytorch.org/get-started/locally/), [pyannote.audio](https://github.com/pyannote/pyannote-audio), [yt-dlp](https://github.com/yt-dlp/yt-dlp), [Streamlit](https://github.com/streamlit/streamlit)_  
> 
> **1. Git clone this repository:**
> ```console
> git clone https://github.com/imgta/vialect.git
> ```
> **2. Install ffmpeg and requirements:**
> ```console
> sudo apt install ffmpeg
> pip install -r requirements.txt
> ```
> **3. Obtain Hugging Face** [_token/access_](https://huggingface.co/pyannote/speaker-diarization-3.1)**, obtain** [_OpenAI API Key_](https://platform.openai.com/api-keys)  
> **4. Create and update** _.streamlit/secrets.toml'_ (Optional: input keys in Secret Keys Drawer after launch)  
> **5. Launch streamlit app:**
> ```console
> streamlit run app/Home.py
> ```

## Usage:
> [!NOTE]
> __1. Select whisper model and options__  
> __2. Input or upload video/audio file__  
> __3. Submit for transcription__

<details>
  <summary><h2>Roadmap:</h2></summary>
    
- [x] Generate summary based on transcript text
- [ ] Create and store text embeddings in vector DB for RAG querying
- [ ] ASR/Diarization for timestamps => reduced sliding window
- [ ] Partition overlap + translation stress test _(Anime subbing?)_
- [ ] Realtime ASR
</details>
