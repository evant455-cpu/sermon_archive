# Naming Convention

## Why Stage-Based Names Are Clearer

Stage-based file names make each artifact's role obvious at a glance. A sermon can move through several stages: raw video, extracted audio, raw transcript, readable transcript, summary, and metadata. Naming each file by both sermon ID and processing stage reduces confusion about which file is safe to edit, which file is generated, and which file belongs to the original source.

The current `sermon_#_video` style identifies the original video-oriented sermon record, but it does not clearly describe later processing outputs. As the archive grows, stage-based names will make scripts easier to reason about and will reduce the risk of mixing raw inputs with cleaned or generated outputs.

## Recommended Future Pattern

Future files should use a stable sermon ID followed by an explicit stage name:

```text
sermon_001_raw_video.mp4
sermon_001_extracted_audio.mp3
sermon_001_raw_transcript.txt
sermon_001_readable_transcript.txt
sermon_001_summary.md
sermon_001_metadata.json
```

The recommended base sermon ID is:

```text
sermon_001
```

Scripts should eventually accept or derive a `SERMON_ID` like `sermon_001`, then append the appropriate stage suffix automatically.

## Folder-Specific Examples

```text
incoming/sermon_001_raw_video.mp4
extracted_audio/sermon_001_extracted_audio.mp3
transcripts/sermon_001_raw_transcript.txt
transcripts/sermon_001_readable_transcript.txt
summaries/sermon_001_summary.md
metadata/sermon_001_metadata.json
```

## Existing Sermons

Sermons 1-3 currently use the older `sermon_#_video` pattern:

```text
sermon_1_video
sermon_2_video
sermon_3_video
```

Those existing names should remain in place for now. We should not manually rename old files until the scripts support migration, because manual renames could break references between media files, transcripts, summaries, metadata, and any script assumptions.

## Migration Guidance

New scripts should eventually be updated to work from a canonical `SERMON_ID`, such as:

```text
SERMON_ID=sermon_001
```

From that base ID, scripts can generate stage-specific paths automatically:

```text
incoming/{SERMON_ID}_raw_video.mp4
extracted_audio/{SERMON_ID}_extracted_audio.mp3
transcripts/{SERMON_ID}_raw_transcript.txt
transcripts/{SERMON_ID}_readable_transcript.txt
summaries/{SERMON_ID}_summary.md
metadata/{SERMON_ID}_metadata.json
```

This keeps the sermon identity stable while allowing each processing stage to have a clear, predictable file name.
