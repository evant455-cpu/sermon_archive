import json
import os
import re
from pathlib import Path


MODEL = "gpt-4o-mini"


def build_prompt(transcript_text, source_file):
    return f"""
Analyze this church service transcript for a sermon archive proof of concept.

The transcript may include announcements, worship lyrics, sermon content, and service closing.
Do not pretend those sections are absent. If you detect them, mention them in the issues/notes.

Return one JSON object with exactly these top-level keys:
- summary_markdown: a human-readable Markdown summary
- metadata_json: a structured JSON object

The Markdown summary should include:
- suggested sermon title
- speaker/preacher if known
- date preached if known, otherwise unknown
- source file
- main scripture passage
- other Bible references
- main topic/theme
- short summary
- detailed outline
- key quotes
- call to action / altar call theme
- transcript confidence/issues

The metadata_json object should include:
- suggested_title
- speaker
- date_preached
- source_file
- main_scripture_passage
- other_bible_references
- main_topic_theme
- short_summary
- detailed_outline
- key_quotes
- call_to_action_theme
- transcript_confidence_issues
- includes_announcements_worship_or_closing

Use null when a value is genuinely unknown.

Source file: {source_file}

Transcript:
{transcript_text}
""".strip()


def safe_error_message(error, api_key):
    message = str(error)
    if api_key:
        message = message.replace(api_key, "[hidden]")
    message = re.sub(
        r"Incorrect API key provided: .*?\. You can",
        "Incorrect API key provided. You can",
        message,
    )
    return message


def load_environment(project_root):
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        print("python-dotenv is not installed for this Python.")
        print("Install dependencies with: python -m pip install -r requirements.txt")
        return False

    load_dotenv(project_root / ".env")
    return True


def request_analysis(api_key, transcript_text, source_file):
    from openai import OpenAI, OpenAIError

    client = OpenAI(api_key=api_key)
    prompt = build_prompt(transcript_text, source_file)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful sermon archive assistant. "
                        "Return valid JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
    except OpenAIError as error:
        print("OpenAI analysis failed.")
        print(f"Error: {safe_error_message(error, api_key)}")
        print("No summary or metadata files were created.")
        return None

    content = response.choices[0].message.content
    try:
        analysis = json.loads(content)
    except json.JSONDecodeError as error:
        print("OpenAI returned a response that was not valid JSON.")
        print(f"Error: {error}")
        print("No summary or metadata files were created.")
        return None

    if "summary_markdown" not in analysis or "metadata_json" not in analysis:
        print("OpenAI response did not include the expected output fields.")
        print("No summary or metadata files were created.")
        return None

    return analysis


def main():
    project_root = Path(__file__).resolve().parent.parent
    transcript_path = (
        project_root / "transcripts" / "sermon_1_video_readable_transcript.txt"
    )
    summaries_folder = project_root / "summaries"
    metadata_folder = project_root / "metadata"
    summary_path = summaries_folder / "sermon_1_video_summary.md"
    metadata_path = metadata_folder / "sermon_1_video_metadata.json"

    print("Starting OpenAI transcript analysis...")
    print(f"Input transcript: {transcript_path}")
    print(f"Summary output: {summary_path}")
    print(f"Metadata output: {metadata_path}")

    if not transcript_path.exists():
        print("Readable transcript was not found.")
        print("No summary or metadata files were created.")
        return

    if not load_environment(project_root):
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is missing.")
        print("No summary or metadata files were created.")
        return

    transcript_text = transcript_path.read_text(encoding="utf-8")
    print(f"Transcript words: {len(transcript_text.split())}")
    print(f"Analysis model: {MODEL}")
    print("Sending transcript to OpenAI for summary and metadata...")

    analysis = request_analysis(
        api_key=api_key,
        transcript_text=transcript_text,
        source_file=transcript_path.name,
    )
    if analysis is None:
        return

    summaries_folder.mkdir(exist_ok=True)
    metadata_folder.mkdir(exist_ok=True)

    summary_text = analysis["summary_markdown"].strip() + "\n"
    metadata = analysis["metadata_json"]

    summary_path.write_text(summary_text, encoding="utf-8")
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("Analysis complete.")
    print(f"Summary saved to: {summary_path}")
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()
