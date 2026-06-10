# Sermon Archive Phase Plan

## Practical Finish Line Definition

The project is considered functionally complete when it can support real church use without needing to redesign the system every week.

For V1, the practical finish line is reached when the project can:

- accept sermon video/audio files
- extract clean audio
- transcribe sermons
- create readable transcripts
- create summaries
- create metadata JSON
- validate metadata
- list/search sermons locally
- preserve a repeatable workflow for future sermons
- handle historical/backlog sermons
- flag privacy/sensitive content
- keep media/transcripts/outputs out of Git
- document the process clearly enough for one person to run it

This does not need to be a perfect or final system. V1 should be useful, repeatable, and safe enough to keep using while future improvements are added later.

## Phase 0 - Project Setup and Guardrails

Status: Complete

Completed work:

- local project folder
- Git repo
- `.gitignore`
- folder structure
- `docs/` folder
- no media/API keys committed

The project has the basic safety rails in place: source code and docs can be committed, while sermon media, generated transcripts, summaries, metadata, working files, `.env`, and API keys stay out of Git.

## Phase 1 - Manual Proof of One Sermon

Status: Complete

Completed work:

- video to audio
- audio to transcript
- readable transcript
- Claude/manual summary
- metadata JSON
- first catalog listing

This proved the core idea: one sermon can move from raw video to a useful archive record.

## Phase 2 - Repeatability Across Multiple Sermons

Status: Complete

Completed work:

- configurable `SERMON_ID`
- process sermons 1-3
- verify same workflow works more than once
- create current workflow documentation
- create checklist for each new sermon
- support the new stage-based naming convention while preserving the older `sermon_#_video` pattern
- create a working automated pipeline runner: `scripts/run_full_pipeline.py`

Completed exit criteria:

- process 3 sermons end-to-end with the same documented workflow

This phase proved the workflow is repeatable. The project now has a one-command runner that processes one selected `SERMON_ID`, calls Claude analysis, and prints the local catalog.

## Phase 3 - Local Catalog and Search

Status: Active / Next

Planned work:

- improve `list_sermons.py`
- export CSV
- search by title, scripture, theme, preacher, privacy flag
- optionally create SQLite database later, but not yet
- process sermon 4 under the new naming convention (`SERMON_ID=sermon_004`)

Exit criteria:

- user can find sermons by scripture/topic from local metadata

Keep this simple first. A useful local search script is enough before considering a database or dashboard.

## Phase 4 - Backlog Processing Workflow

Status: Blocked / Limited

Planned work:

- decide naming convention for historical sermons
- download/extract audio from older Facebook/YouTube/OBS recordings
- process batches carefully
- keep manual review checkpoints

Exit criteria:

- at least 10 historical sermons processed and listed

Historical Facebook videos appear deleted or unavailable. If old videos are found later, they can still be processed manually, but this phase should not block current work.

## Phase 5 - Future Sunday Workflow

Status: Current Priority

Planned work:

- OBS recording habit
- save Sunday recording locally
- process after service
- create summary/metadata
- optionally export PDF for sharing
- follow `docs/future_sunday_recording_workflow.md`

Exit criteria:

- one new Sunday sermon processed using the workflow without redesigning the system

The goal is a normal weekly habit: record, process, review, archive.

## Phase 6 - Privacy and Publishing Rules

Status: Not Started

Planned work:

- flag minors' names
- baptism/testimony sensitivity
- decide what can be public vs private
- decide whether PDFs are for internal archive only or church sharing

Exit criteria:

- each sermon has a `privacy_review_needed` flag and notes before sharing

This matters before anything becomes public. Baptisms, testimonies, children's names, prayer needs, and personal details need review before sharing outside the archive.

## Phase 7 - Practical V1 Completion

Status: Not Started

Planned work:

- process several sermons
- list/search them
- docs are complete
- workflow is repeatable
- no critical manual mystery steps remain

Exit criteria:

- the system is useful even if no new features are added

This is the V1 finish line. The project does not need to be automated end-to-end yet. It needs to be understandable, safe, repeatable, and genuinely useful.

## Future Versions / Improvements

Possible future improvements:

- better transcription provider
- speaker diarization
- sermon-only trimming
- automatic AI analysis API
- web dashboard
- SQLite full-text search
- scripture reference validation
- PDF generation
- backups
- church-facing searchable archive

These are future upgrades, not V1 requirements. The first win is a local archive workflow that one person can run without overbuilding.
