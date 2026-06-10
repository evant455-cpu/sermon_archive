# New Sermon Processing Checklist

## Before You Start

- Choose a clean sermon ID, example: `sermon_004`
- Confirm `.env` exists and contains `SPEECHMATICS_API_KEY`
- Confirm `.env` exists and contains `ANTHROPIC_API_KEY`
- Confirm Git status is clean before starting

Sermons 1-3 used the older `sermon_#_video` pattern and remain supported. Do not manually rename those older files until the scripts support a full migration.

## Step 1: Add Source Video

Rename or copy the source video to:

```text
incoming/sermon_004_raw_video.mp4
```

## Step 2: Set SERMON_ID

```powershell
$env:SERMON_ID="sermon_004"
```

## Step 3: Run Full Pipeline

Command:

```powershell
.\.venv\Scripts\python.exe scripts\run_full_pipeline.py
```

The pipeline runs:

- `process_sermon.py`
- `analyze_transcript_claude.py`
- `list_sermons.py`

Expected outputs:

```text
extracted_audio/sermon_004_extracted_audio.mp3
transcripts/sermon_004_raw_transcript.txt
transcripts/sermon_004_readable_transcript.txt
summaries/sermon_004_summary.md
metadata/sermon_004_metadata.json
```

## Step 4: Review Summary and Metadata

Review the generated summary and metadata for accuracy, uncertainty, and privacy concerns:

```text
summaries/sermon_004_summary.md
metadata/sermon_004_metadata.json
```

## Step 5: Validate Metadata

Command:

```powershell
.\.venv\Scripts\python.exe -m json.tool metadata\sermon_004_metadata.json
```

## Step 6: List Sermons

Command:

```powershell
.\.venv\Scripts\python.exe scripts\list_sermons.py
```

## Manual Analysis Fallback

If the Claude API step fails or needs manual review, use `docs/manual_claude_analysis_workflow.md` as the fallback process.

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
