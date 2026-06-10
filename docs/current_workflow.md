# Sermon Archive Current Workflow

## Purpose

A local-first workflow for turning church sermon videos into:

- extracted audio
- raw transcript
- readable transcript
- sermon summary
- metadata JSON
- local catalog listing

## Current Folder Flow

```text
incoming/
extracted_audio/
transcripts/
summaries/
metadata/
working/
```

## Step 1: Add Sermon Video

Place sermon video files in `incoming/`.

Use a clean sermon ID naming pattern when possible:

```text
sermon_004_raw_video.mp4
```

The sermon ID is the stable base name before the stage suffix:

```text
sermon_004
```

Sermons 1-3 used the older `sermon_#_video` pattern and remain supported. Do not manually rename those older files until the scripts support a full migration.

## Step 2: Extract Audio

Run:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\extract_audio.py
```

Output:

```text
extracted_audio/sermon_004_extracted_audio.mp3
```

## Step 3: Transcribe With Speechmatics

Run:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\transcribe_audio_speechmatics.py
```

Output:

```text
transcripts/sermon_004_raw_transcript.txt
```

## Step 4: Format Readable Transcript

Run:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\format_transcript.py
```

Output:

```text
transcripts/sermon_004_readable_transcript.txt
```

## Step 5: Manual Claude Analysis

Paste the readable transcript into Claude using the manual sermon analysis prompt.

Save Claude's full response into:

```text
working/claude_analysis_sermon_004.txt
```

Split Claude's output into:

```text
summaries/sermon_004_summary.md
metadata/sermon_004_metadata.json
```

See `docs/manual_claude_analysis_workflow.md` for the detailed manual analysis rules, uncertainty corrections, and expected archive fields.

## Step 6: Validate Metadata JSON

Validate the metadata JSON before using it:

```powershell
.\.venv\Scripts\python.exe -m json.tool metadata\sermon_004_metadata.json
```

If validation fails, fix the JSON syntax before moving on.

## Step 7: List Local Sermon Catalog

Run:

```powershell
.\.venv\Scripts\python.exe scripts\list_sermons.py
```

## Git Rules

Do commit:

- scripts
- docs
- `.gitignore` changes

Do not commit:

- incoming media
- extracted audio
- transcripts
- summaries
- metadata
- working files
- `.env`
- API keys
