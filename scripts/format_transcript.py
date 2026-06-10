import os
import re
from pathlib import Path


SENTENCES_PER_PARAGRAPH = 5
SPEAKER_LABEL_PATTERN = re.compile(r"\b(SPEAKER [A-Z]+:)")
ABBREVIATIONS = {
    "a.m.",
    "p.m.",
    "mr.",
    "mrs.",
    "ms.",
    "dr.",
    "bro.",
    "sr.",
    "jr.",
    "st.",
    "vs.",
    "etc.",
}


def word_count(text):
    return len(re.findall(r"\S+", text))


def split_speaker_sections(text):
    parts = SPEAKER_LABEL_PATTERN.split(text)
    sections = []
    pending_text = parts[0].strip()

    if pending_text:
        sections.append(pending_text)

    index = 1
    while index < len(parts):
        label = parts[index].strip()
        body = parts[index + 1].strip() if index + 1 < len(parts) else ""
        sections.append(f"{label} {body}".strip())
        index += 2

    return sections


def is_abbreviation(sentence_fragment):
    words = sentence_fragment.strip().lower().split()
    return bool(words and words[-1] in ABBREVIATIONS)


def split_sentences(text):
    sentences = []
    start = 0

    for match in re.finditer(r"[.?!]+(?=\s+|$)", text):
        end = match.end()
        fragment = text[start:end].strip()

        if not fragment:
            start = end
            continue

        if is_abbreviation(fragment):
            continue

        sentences.append(fragment)
        start = end

    remaining = text[start:].strip()
    if remaining:
        sentences.append(remaining)

    return sentences


def group_sentences(sentences):
    paragraphs = []
    for index in range(0, len(sentences), SENTENCES_PER_PARAGRAPH):
        paragraph = " ".join(sentences[index : index + SENTENCES_PER_PARAGRAPH]).strip()
        if paragraph:
            paragraphs.append(paragraph)
    return paragraphs


def format_transcript(raw_text):
    paragraphs = []

    for section in split_speaker_sections(raw_text):
        sentences = split_sentences(section)
        paragraphs.extend(group_sentences(sentences))

    return paragraphs


def print_paragraphs(title, paragraphs):
    print(title)
    if not paragraphs:
        print("(none)")
        return

    for number, paragraph in enumerate(paragraphs, start=1):
        print(f"{number}. {paragraph}")


def raw_transcript_name(sermon_id):
    return f"{sermon_id}_raw_transcript.txt"


def readable_transcript_name(sermon_id):
    return f"{sermon_id}_readable_transcript.txt"


def main():
    project_root = Path(__file__).resolve().parent.parent
    sermon_id = os.environ.get("SERMON_ID", "sermon_1_video")
    input_path = project_root / "transcripts" / raw_transcript_name(sermon_id)
    output_path = project_root / "transcripts" / readable_transcript_name(sermon_id)

    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")

    if not input_path.exists():
        print("Raw transcript was not found. No files were changed.")
        return

    raw_text = input_path.read_text(encoding="utf-8")
    paragraphs = format_transcript(raw_text)
    readable_text = "\n\n".join(paragraphs) + "\n"

    output_path.write_text(readable_text, encoding="utf-8")

    print(f"Raw word count: {word_count(raw_text)}")
    print(f"Readable paragraph count: {len(paragraphs)}")
    print()
    print_paragraphs("First 5 paragraphs:", paragraphs[:5])
    print()
    print_paragraphs("Last 3 paragraphs:", paragraphs[-3:])
    print()
    print("The raw transcript was not modified or deleted.")


if __name__ == "__main__":
    main()
