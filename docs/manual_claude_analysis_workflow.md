# Manual Claude Analysis Workflow

This documents the current manual Phase 1C workflow for turning a readable sermon transcript into archive-ready summary and metadata files.

This is a temporary manual path. Do not process sermon 2 yet.

## Inputs

Start with a readable transcript in `transcripts/`.

Expected input pattern:

```text
transcripts/<sermon_id>_readable_transcript.txt
```

Example:

```text
transcripts/sermon_1_video_readable_transcript.txt
```

## Manual Analysis Steps

1. Open the Claude app.
2. Paste the Claude sermon analysis prompt.
3. Paste the readable transcript.
4. Save Claude's full response into:

```text
working/claude_analysis_<sermon_id>.txt
```

Example:

```text
working/claude_analysis_sermon_1_video.txt
```

5. Split Claude's response into:

```text
summaries/<sermon_id>_summary.md
metadata/<sermon_id>_metadata.json
```

Example:

```text
summaries/sermon_1_video_summary.md
metadata/sermon_1_video_metadata.json
```

6. Use the Markdown summary section for the summary file.
7. Use the JSON metadata section for the metadata file.
8. Correct metadata uncertainty fields before treating the JSON as archive-ready.
9. Validate the JSON.

## Metadata Corrections

Apply these corrections whenever Claude infers uncertain fields:

- `date_preached` should be `null` if the actual date is not known.
- Use `date_note` for inferred date clues, such as "late May" based on transcript language.
- `preacher_name` should contain only the name, not the explanation.
- Use `preacher_name_confidence` for confidence, such as `"uncertain"`.
- Use `preacher_name_note` to explain uncertainty, including whether no formal introduction was given.

## Expected Archive Outputs

Each analyzed sermon should produce both a Markdown summary and JSON metadata with these archive fields:

- sermon title
- `title_was_suggested`
- `date_preached` and `date_note`
- preacher name, confidence, and note
- main scripture
- other Bible references
- theme
- short summary
- detailed outline
- key quotes
- call to action
- transcript confidence and issues
- service content notes

## JSON Validation

Validate metadata before using it:

```powershell
.\.venv\Scripts\python.exe -m json.tool metadata\<sermon_id>_metadata.json
```

If validation fails, fix the JSON syntax before moving on.

## Do Not Commit

Do not commit generated or private working files unless the project policy changes.

Do not commit:

- generated summaries
- generated metadata
- transcripts
- sermon media files
- files in `working/`
- `.env`
- API keys

The current `.gitignore` should keep these outputs out of Git, but always check with:

```powershell
git status --short
```
