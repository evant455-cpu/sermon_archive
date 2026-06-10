import json
import os
import re
import sys
from pathlib import Path

from format_transcript import readable_transcript_name


MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 8192
SUMMARY_MARKER = "SERMON_SUMMARY_MARKDOWN"
METADATA_MARKER = "METADATA_JSON"
REQUIRED_METADATA_KEYS = [
    "sermon_title",
    "title_was_suggested",
    "date_preached",
    "date_note",
    "preacher_name",
    "preacher_name_confidence",
    "preacher_name_note",
    "source_file",
    "main_scripture_passage",
    "other_bible_references",
    "main_topic_or_theme",
    "short_summary",
    "detailed_outline",
    "key_quotes",
    "call_to_action",
    "transcript_confidence",
    "transcript_issues",
    "service_content_notes",
    "privacy_review_needed",
    "privacy_review_notes",
]


def hide_secret(message, secret):
    if not secret:
        return message
    return message.replace(secret, "[hidden]")


def load_environment(project_root):
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        print("python-dotenv is not installed for this Python.")
        print("Install project dependencies with: python -m pip install -r requirements.txt")
        return False

    load_dotenv(project_root / ".env")
    return True


def ensure_anthropic_available():
    try:
        from anthropic import Anthropic
    except ModuleNotFoundError:
        print(r".\.venv\Scripts\python.exe -m pip install anthropic")
        return None

    return Anthropic


def build_prompt(transcript_text, sermon_id):
    return f"""
Analyze this readable church sermon transcript for archive use.

Source file / SERMON_ID: {sermon_id}

Focus on the sermon itself. Ignore or non-prioritize announcements, worship, offering, baptisms, and closing reminders unless they are relevant to archive notes, transcript issues, privacy review, or service context.

Rules:
- Do not invent title, date, preacher, scripture, or historical claims.
- Use null for unknown values.
- If no title is explicitly stated and you suggest one, set title_was_suggested to true.
- Keep preacher_name simple. Put uncertainty in preacher_name_confidence and preacher_name_note.
- Put inferred date clues in date_note, not date_preached. Use date_preached only when the actual date is explicit or certain.
- Keep key quotes close to transcript wording.
- Flag privacy concerns: minors, baptisms, testimonies, prayer requests, medical/family details, and full names.
- Ensure metadata source_file is exactly "{sermon_id}".

Return exactly two sections with these markers and no extra sections:

{SUMMARY_MARKER}

<Markdown summary for archive use>

{METADATA_MARKER}

<valid JSON object>

The metadata JSON must include exactly these archive fields:
- sermon_title
- title_was_suggested
- date_preached
- date_note
- preacher_name
- preacher_name_confidence
- preacher_name_note
- source_file
- main_scripture_passage
- other_bible_references
- main_topic_or_theme
- short_summary
- detailed_outline
- key_quotes
- call_to_action
- transcript_confidence
- transcript_issues
- service_content_notes
- privacy_review_needed
- privacy_review_notes

TRANSCRIPT START
{transcript_text}
TRANSCRIPT END
""".strip()


def call_claude(anthropic_class, api_key, prompt):
    client = anthropic_class(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    parts = []
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)

    return "\n".join(parts).strip()


def strip_json_fence(metadata_text):
    text = metadata_text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def extract_sections(raw_response):
    summary_index = raw_response.find(SUMMARY_MARKER)
    metadata_index = raw_response.find(METADATA_MARKER)

    if summary_index == -1 or metadata_index == -1 or metadata_index < summary_index:
        raise ValueError("Claude response did not contain the expected section markers.")

    summary_start = summary_index + len(SUMMARY_MARKER)
    metadata_start = metadata_index + len(METADATA_MARKER)
    summary_markdown = raw_response[summary_start:metadata_index].strip()
    metadata_text = strip_json_fence(raw_response[metadata_start:].strip())

    if not summary_markdown:
        raise ValueError("Claude response did not include summary Markdown.")

    return summary_markdown, metadata_text


def validate_metadata(metadata, sermon_id):
    missing_keys = [key for key in REQUIRED_METADATA_KEYS if key not in metadata]
    if missing_keys:
        raise ValueError(f"Metadata JSON is missing required keys: {', '.join(missing_keys)}")

    if metadata.get("source_file") != sermon_id:
        raise ValueError(
            f"Metadata source_file must be {sermon_id!r}, got {metadata.get('source_file')!r}."
        )


def save_failed_response(project_root, sermon_id, raw_response):
    working_folder = project_root / "working"
    working_folder.mkdir(exist_ok=True)
    failed_path = working_folder / f"claude_failed_{sermon_id}.txt"
    failed_path.write_text(raw_response, encoding="utf-8")
    print(f"Raw Claude output saved to: {failed_path}")


def main():
    sermon_id = os.environ.get("SERMON_ID")
    if not sermon_id:
        print("SERMON_ID is missing. Set it before running this script.")
        print('Example: $env:SERMON_ID="sermon_004"')
        sys.exit(1)

    project_root = Path(__file__).resolve().parent.parent
    transcript_path = project_root / "transcripts" / readable_transcript_name(sermon_id)
    summary_path = project_root / "summaries" / f"{sermon_id}_summary.md"
    metadata_path = project_root / "metadata" / f"{sermon_id}_metadata.json"

    print(f"Target SERMON_ID: {sermon_id}")
    print(f"Input transcript: {transcript_path}")

    if not transcript_path.exists():
        print("Readable transcript was not found.")
        print("No summary or metadata files were created.")
        sys.exit(1)

    if not load_environment(project_root):
        sys.exit(1)

    anthropic_class = ensure_anthropic_available()
    if anthropic_class is None:
        print("No summary or metadata files were created.")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY is missing.")
        print("No summary or metadata files were created.")
        sys.exit(1)

    transcript_text = transcript_path.read_text(encoding="utf-8")
    prompt = build_prompt(transcript_text, sermon_id)

    print(f"Analysis model: {MODEL}")
    print("Sending transcript to Claude for summary and metadata...")

    try:
        raw_response = call_claude(anthropic_class, api_key, prompt)
    except Exception as error:
        print("Claude analysis failed.")
        print(f"Error: {hide_secret(str(error), api_key)}")
        print("No summary or metadata files were created.")
        sys.exit(1)

    try:
        summary_markdown, metadata_text = extract_sections(raw_response)
        metadata = json.loads(metadata_text)
        validate_metadata(metadata, sermon_id)
    except (json.JSONDecodeError, ValueError) as error:
        print("Claude response could not be converted into valid archive outputs.")
        print(f"Error: {error}")
        save_failed_response(project_root, sermon_id, raw_response)
        print("No summary or metadata files were created.")
        sys.exit(1)

    summary_path.parent.mkdir(exist_ok=True)
    metadata_path.parent.mkdir(exist_ok=True)

    summary_path.write_text(summary_markdown.rstrip() + "\n", encoding="utf-8")
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("Claude analysis complete.")
    print(f"Summary saved to: {summary_path}")
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()
