# Sermon Archive

A local-first Python pipeline that turns church sermon videos into a searchable archive. Drop a video in, run one command, and get extracted audio, a transcript, a summary, and structured metadata.

## What it produces for each sermon

- Extracted audio
- Raw and readable transcripts
- A sermon summary
- Metadata JSON (title, preacher, main scripture, theme, call to action, and a privacy-review flag)
- An entry in a local catalog you can list and search

## How it works

```
incoming/ (video) -> extract audio -> transcribe (Speechmatics)
                  -> readable transcript -> analyze (Claude API)
                  -> summary + metadata JSON -> local catalog / search
```

Run the whole pipeline for one sermon:

```powershell
$env:SERMON_ID="sermon_004"
python scripts\run_full_pipeline.py
```

Other scripts in [`scripts/`](scripts/) handle each stage on its own (`extract_audio.py`, `transcribe_audio.py`, `format_transcript.py`, `analyze_transcript_claude.py`), list the catalog (`list_sermons.py`), and search it (`search_sermons.py <terms>`). An OpenAI-based analysis script is included as an alternative.

## Docs

- [`docs/current_workflow.md`](docs/current_workflow.md): step-by-step usage
- [`docs/naming_convention.md`](docs/naming_convention.md): how sermon files and IDs are named
- [`docs/new_sermon_checklist.md`](docs/new_sermon_checklist.md): checklist for each new sermon
- [`docs/future_sunday_recording_workflow.md`](docs/future_sunday_recording_workflow.md): recording going forward

## Privacy

Sermon media, transcripts, summaries and metadata stay on the local machine and are git-ignored. Only the code and docs are in this repository. The analysis step flags sermons that may need a privacy review before anything is shared.

## Setup

```bash
pip install -r requirements.txt
```

Needs `ffmpeg` for audio extraction, plus API keys for Speechmatics and Claude (or OpenAI), stored in a git-ignored `.env` file.

## Stack

Python, Speechmatics speech-to-text, Claude API, OpenAI API (optional), ffmpeg.
