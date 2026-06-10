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

Use the stage-based naming pattern for new sermons:

```text
incoming/sermon_004_raw_video.mp4
```

The sermon ID is the stable base name before the stage suffix:

```text
sermon_004
```

Sermons 1-3 used the older `sermon_#_video` pattern and remain supported. Do not manually rename those older files until the scripts support a full migration.

## Step 2: Run the One-Command Pipeline

The recommended normal workflow is:

```powershell
$env:SERMON_ID="sermon_004"
.\.venv\Scripts\python.exe scripts\run_full_pipeline.py
```

This runs the full local archive pipeline for the selected sermon only:

1. `process_sermon.py`
2. `analyze_transcript_claude.py`
3. `list_sermons.py`

`process_sermon.py` handles:

- audio extraction
- Speechmatics transcription
- readable transcript formatting
- manual prompt package creation in `working/`

`analyze_transcript_claude.py` uses the Claude API to generate:

```text
summaries/sermon_004_summary.md
metadata/sermon_004_metadata.json
```

`list_sermons.py` then prints the local catalog so the new sermon can be checked immediately.

## Step 3: Review Outputs

Review:

```text
extracted_audio/sermon_004_extracted_audio.mp3
transcripts/sermon_004_raw_transcript.txt
transcripts/sermon_004_readable_transcript.txt
summaries/sermon_004_summary.md
metadata/sermon_004_metadata.json
```

## Step 4: Validate Metadata JSON

Validate the metadata JSON before using it:

```powershell
.\.venv\Scripts\python.exe -m json.tool metadata\sermon_004_metadata.json
```

If validation fails, fix the JSON syntax before moving on.

## Step 5: List Local Sermon Catalog

Run:

```powershell
.\.venv\Scripts\python.exe scripts\list_sermons.py
```

## Search Local Sermon Metadata

Use `scripts/search_sermons.py` to search the local metadata JSON files in `metadata/`:

```powershell
.\.venv\Scripts\python.exe scripts\search_sermons.py grace
.\.venv\Scripts\python.exe scripts\search_sermons.py John
.\.venv\Scripts\python.exe scripts\search_sermons.py "Holy Spirit"
.\.venv\Scripts\python.exe scripts\search_sermons.py privacy
```

This searches metadata fields such as title, preacher, scripture, theme, summary, call to action, quotes/issues/references lists, and privacy fields when present.

This is a simple Phase 3 metadata search. It does not use SQLite or search full transcript text yet.

## Manual Analysis Fallback

If Claude API analysis fails or needs manual review, use the manual Claude/Gemini workflow as a fallback. Paste the readable transcript into the manual analysis prompt, save the full response in `working/`, then split the Markdown summary and JSON metadata into `summaries/` and `metadata/`.

See `docs/manual_claude_analysis_workflow.md` for the detailed manual analysis rules, uncertainty corrections, and expected archive fields.

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
