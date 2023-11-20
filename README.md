# 👾V/A.Lect
> _**Traversing digital oceans, for treasures unseen.**_

**Vialect** *transforms audio into workable text (e.g. generate summaries from video links).*

_**Tech Pipelines:**_  [Pyannote Audio](https://github.com/pyannote/pyannote-audio), [OpenAI Whisper](https://github.com/openai/whisper), [YoutubeDL](https://github.com/yt-dlp/yt-dlp)


### SETUP:
1. Install ffmpeg and requirements:
```console
sudo apt install ffmpeg
pip install -r requirements.txt
```
2. Obtain [huggingface token](https://huggingface.co/pyannote/speaker-diarization) and [OpenAI API Key](https://platform.openai.com/api-keys)
3. Create and update `.streamlit/secrets.toml` with keys (example provided)
4. Launch streamlit app:
```console
streamlit run app/Home.py
```

### USAGE:
1. Select whisper model and options
2. Input or upload video/audio file
3. Submit for transcription

### TODO:
- [ ] ASR/Diarization for timestamps => reduced sliding window
- [ ] Overlap stress test and translation test => Anime subbing
- [ ] Realtime ASR
