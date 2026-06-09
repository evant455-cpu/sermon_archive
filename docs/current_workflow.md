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
sermon_3_video.mp4
```

The sermon ID is the file name without the extension:

```text
sermon_3_video
```

## Step 2: Extract Audio

Run:

```powershell
$env:SERMON_ID="sermon_3_video"
.\.venv\Scripts\python.exe scripts\extract_audio.py
```

Output:

```text
extracted_audio/sermon_3_video.mp3
```

## Step 3: Transcribe With Speechmatics

Run:

```powershell
$env:SERMON_ID="sermon_3_video"
.\.venv\Scripts\python.exe scripts\transcribe_audio_speechmatics.py
```

Output:

```text
transcripts/sermon_3_video_raw_transcript.txt
```

## Step 4: Format Readable Transcript

Run:

```powershell
$env:SERMON_ID="sermon_3_video"
.\.venv\Scripts\python.exe scripts\format_transcript.py
```

Output:

```text
transcripts/sermon_3_video_readable_transcript.txt
```

## Step 5: Manual Claude Analysis

Paste the readable transcript into Claude using the manual sermon analysis prompt.

Save Claude's full response into:

```text
working/claude_analysis_sermon_3.txt
```

Split Claude's output into:

```text
summaries/sermon_3_video_summary.md
metadata/sermon_3_video_metadata.json
```

See `docs/manual_claude_analysis_workflow.md` for the detailed manual analysis rules, uncertainty corrections, and expected archive fields.

## Step 6: Validate Metadata JSON

Validate the metadata JSON before using it:

```powershell
.\.venv\Scripts\python.exe -m json.tool metadata\sermon_3_video_metadata.json
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
