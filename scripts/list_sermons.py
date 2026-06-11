import json
from pathlib import Path


PRIVACY_KEYWORDS = ("privacy", "minor", "full name", "baptism name")
PRIVACY_FIELD_NAMES = (
    "privacy_review_needed",
    "privacy_flag",
    "privacy",
    "needs_privacy_review",
    "privacy_review",
    "sensitive_content_flag",
)
TRUE_PRIVACY_VALUES = ("true", "yes", "needed")
FALSE_PRIVACY_VALUES = ("false", "no", "not needed")
COLUMNS = [
    ("sermon_id", "Sermon ID", 18),
    ("sermon_title", "Title", 34),
    ("preacher_name", "Preacher", 12),
    ("main_scripture_passage", "Main Scripture", 24),
    ("main_topic_or_theme", "Theme", 42),
    ("transcript_confidence", "Confidence", 24),
    ("privacy_review_needed", "Privacy", 8),
]


def truncate(value, width):
    text = "" if value is None else str(value)
    if len(text) <= width:
        return text
    return text[: max(0, width - 3)] + "..."


def privacy_value_to_bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        cleaned_value = value.strip().lower()
        if cleaned_value in TRUE_PRIVACY_VALUES:
            return True
        if cleaned_value in FALSE_PRIVACY_VALUES:
            return False

    return None


def transcript_issues_need_privacy_review(metadata):
    issues = metadata.get("transcript_issues", [])
    if not isinstance(issues, list):
        return None

    for issue in issues:
        issue_text = str(issue).lower()
        if any(keyword in issue_text for keyword in PRIVACY_KEYWORDS):
            return True

    return None


def needs_privacy_review(metadata):
    found_false_value = False

    for field_name in PRIVACY_FIELD_NAMES:
        privacy_value = privacy_value_to_bool(metadata.get(field_name))
        if privacy_value is True:
            return True
        if privacy_value is False:
            found_false_value = True

    if found_false_value:
        return False

    return transcript_issues_need_privacy_review(metadata)


def load_metadata(metadata_path):
    with metadata_path.open(encoding="utf-8") as metadata_file:
        metadata = json.load(metadata_file)

    return {
        "sermon_id": metadata.get("source_file") or metadata_path.stem.removesuffix(
            "_metadata"
        ),
        "sermon_title": metadata.get("sermon_title"),
        "preacher_name": metadata.get("preacher_name"),
        "main_scripture_passage": metadata.get("main_scripture_passage"),
        "main_topic_or_theme": metadata.get("main_topic_or_theme"),
        "transcript_confidence": metadata.get("transcript_confidence"),
        "privacy_review_needed": needs_privacy_review(metadata),
    }


def print_table(rows):
    headers = [
        truncate(header, width).ljust(width) for _, header, width in COLUMNS
    ]
    separator = ["-" * width for _, _, width in COLUMNS]

    print(" | ".join(headers))
    print("-+-".join(separator))

    for row in rows:
        cells = [
            truncate(row[key], width).ljust(width) for key, _, width in COLUMNS
        ]
        print(" | ".join(cells))


def main():
    project_root = Path(__file__).resolve().parent.parent
    metadata_folder = project_root / "metadata"
    metadata_files = sorted(metadata_folder.glob("*_metadata.json"))

    if not metadata_files:
        print("No sermon metadata files found yet.")
        return

    rows = []
    for metadata_path in metadata_files:
        try:
            rows.append(load_metadata(metadata_path))
        except json.JSONDecodeError as error:
            print(f"Skipping invalid JSON file: {metadata_path.name}")
            print(f"Error: {error}")

    if not rows:
        print("No valid sermon metadata files found yet.")
        return

    print_table(rows)


if __name__ == "__main__":
    main()
