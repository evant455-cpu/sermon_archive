# New Sermon Processing Checklist

## Before You Start

- Choose a clean sermon ID, example: `sermon_004`
- Put the video file in `incoming/`
- Confirm `.env` exists and contains `SPEECHMATICS_API_KEY`
- Confirm Git status is clean before starting

Sermons 1-3 used the older `sermon_#_video` pattern and remain supported. Do not manually rename those older files until the scripts support a full migration.

## Step 1 — Extract Audio

Command:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\extract_audio.py
```

Expected output:

```text
extracted_audio/sermon_004_extracted_audio.mp3
```

## Step 2 — Transcribe Audio

Command:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\transcribe_audio_speechmatics.py
```

Expected output:

```text
transcripts/sermon_004_raw_transcript.txt
```

## Step 3 — Format Readable Transcript

Command:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\format_transcript.py
```

Expected output:

```text
transcripts/sermon_004_readable_transcript.txt
```

## Step 4 — Manual Claude Analysis

- Use the prompt from `docs/manual_claude_analysis_workflow.md`
- Paste the readable transcript
- Save Claude's full response to:

```text
working/claude_analysis_sermon_004.txt
```

## Step 5 — Save Archive Outputs

Expected outputs:

```text
summaries/sermon_004_summary.md
metadata/sermon_004_metadata.json
```

## Step 6 — Validate Metadata

Command:

```powershell
.\.venv\Scripts\python.exe -m json.tool metadata\sermon_004_metadata.json
```

## Step 7 — List Sermons

Command:

```powershell
.\.venv\Scripts\python.exe scripts\list_sermons.py
```

## Privacy Review

Check for:

- minors' names
- baptism/testimony details
- prayer requests
- medical/family details
- full names of private individuals

## Git Rules

Do commit:

- scripts
- docs
- `.gitignore`

Do not commit:

- `incoming/`
- `extracted_audio/`
- `transcripts/`
- `summaries/`
- `metadata/`
- `working/`
- `.env`
- API keys
