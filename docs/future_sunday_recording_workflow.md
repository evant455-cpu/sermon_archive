# Future Sunday Recording Workflow

## Purpose

Facebook should not be treated as the sermon archive.

Older Facebook Live videos may disappear, become unavailable, or be deleted. Going forward, the local OBS recording is the source of truth. Facebook can still be used for livestreaming, but the archive depends on the local recording file.

## Sunday Recording Checklist

- Start OBS/local recording before the service or sermon begins.
- Confirm audio is coming from the dedicated mic or soundboard source.
- Confirm the Facebook livestream separately if it is needed.
- Stop recording after the service or sermon ends.
- Verify the local video file exists before leaving.

## After-Service Processing Checklist

1. Copy the video into `incoming/`.
2. Rename it using the current convention:

```powershell
incoming/sermon_005_raw_video.mp4
```

3. Set `SERMON_ID`:

```powershell
$env:SERMON_ID="sermon_005"
```

4. Run the full pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_full_pipeline.py
```

5. Run the catalog listing:

```powershell
.\.venv\Scripts\python.exe scripts\list_sermons.py
```

6. Run metadata search:

```powershell
.\.venv\Scripts\python.exe scripts\search_sermons.py "search term"
```

## Backup Rule

- Keep raw videos out of Git.
- Copy raw recordings to an external drive or backup location.
- Generated transcripts and metadata stay ignored by Git.

## Notes About Historical Backlog

Older Facebook Live videos were checked and appear unavailable or deleted.

If any old videos are found later, they can still be processed manually. Do not block the project waiting for old videos.
