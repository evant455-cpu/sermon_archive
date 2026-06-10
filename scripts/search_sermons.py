import json
import sys
from pathlib import Path


FIELD_ALIASES = {
    "Sermon ID": ["source_file", "sermon_id"],
    "Title": ["sermon_title", "title", "suggested_title"],
    "Preacher": ["preacher_name", "preacher", "speaker"],
    "Main Scripture": ["main_scripture_passage", "main_scripture"],
    "Theme": ["main_topic_or_theme", "theme", "main_topic_theme"],
    "Summary": ["short_summary", "summary"],
    "Call To Action": ["call_to_action", "call_to_action_theme"],
    "Privacy Review Needed": ["privacy_review_needed"],
    "Privacy Notes": ["privacy_review_notes", "privacy_notes"],
}

SEARCH_LIST_HINTS = (
    "topic",
    "keyword",
    "scripture",
    "reference",
    "issue",
    "quote",
)


def usage():
    print("Usage:")
    print(r".\.venv\Scripts\python.exe scripts\search_sermons.py <search terms>")


def first_value(metadata, keys):
    for key in keys:
        value = metadata.get(key)
        if value not in (None, ""):
            return value
    return None


def value_to_text(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    if isinstance(value, list):
        return " ".join(value_to_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(
            f"{key} {value_to_text(child_value)}"
            for key, child_value in value.items()
        )
    return str(value)


def collect_search_fields(metadata):
    fields = {}

    for label, keys in FIELD_ALIASES.items():
        value = first_value(metadata, keys)
        if value not in (None, ""):
            fields[label] = value_to_text(value)

    for key, value in metadata.items():
        if isinstance(value, list) and any(hint in key.lower() for hint in SEARCH_LIST_HINTS):
            label = key.replace("_", " ").title()
            fields.setdefault(label, value_to_text(value))

    return fields


def load_metadata(metadata_path):
    with metadata_path.open(encoding="utf-8") as metadata_file:
        metadata = json.load(metadata_file)

    sermon_id = first_value(
        metadata,
        ["source_file", "sermon_id"],
    ) or metadata_path.stem.removesuffix("_metadata")

    return sermon_id, metadata


def find_matches(metadata, query):
    query_text = query.lower()
    fields = collect_search_fields(metadata)
    matching_fields = [
        label
        for label, value in fields.items()
        if query_text in f"{label} {value}".lower()
    ]
    return fields, matching_fields


def display_value(fields, label, fallback):
    value = fields.get(label)
    if value in (None, ""):
        return fallback
    return value


def print_match(sermon_id, fields, matching_fields):
    print(f"Sermon ID: {sermon_id}")
    print(f"Title: {display_value(fields, 'Title', '(unknown)')}")
    print(f"Preacher: {display_value(fields, 'Preacher', '(unknown)')}")
    print(f"Main Scripture: {display_value(fields, 'Main Scripture', '(none listed)')}")
    print(f"Theme: {display_value(fields, 'Theme', '(none listed)')}")
    print(
        "Privacy Review Needed: "
        f"{display_value(fields, 'Privacy Review Needed', '(not specified)')}"
    )
    print(f"Matching fields: {', '.join(matching_fields)}")
    print()


def main():
    if len(sys.argv) < 2:
        usage()
        return

    query = " ".join(sys.argv[1:]).strip()
    if not query:
        usage()
        return

    project_root = Path(__file__).resolve().parent.parent
    metadata_folder = project_root / "metadata"
    metadata_files = sorted(metadata_folder.glob("*_metadata.json"))

    if not metadata_files:
        print("No sermon metadata files found yet.")
        return

    matches = []
    for metadata_path in metadata_files:
        try:
            sermon_id, metadata = load_metadata(metadata_path)
        except json.JSONDecodeError as error:
            print(f"Skipping invalid JSON file: {metadata_path.name}")
            print(f"Error: {error}")
            continue

        fields, matching_fields = find_matches(metadata, query)
        if matching_fields:
            matches.append((sermon_id, fields, matching_fields))

    if not matches:
        print(f"No sermons found matching: {query}")
        return

    print(f"Found {len(matches)} sermon(s) matching: {query}")
    print()
    for sermon_id, fields, matching_fields in matches:
        print_match(sermon_id, fields, matching_fields)


if __name__ == "__main__":
    main()
