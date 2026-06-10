import os
import subprocess
import sys
from pathlib import Path


PIPELINE_STEPS = [
    ("Process sermon media/transcript", "process_sermon.py"),
    ("Analyze readable transcript with Claude", "analyze_transcript_claude.py"),
    ("List sermon catalog", "list_sermons.py"),
]


def run_step(project_root, sermon_id, title, script_name):
    print()
    print(f"=== {title} ===", flush=True)

    env = os.environ.copy()
    env["SERMON_ID"] = sermon_id
    command = [sys.executable, str(project_root / "scripts" / script_name)]
    result = subprocess.run(command, cwd=project_root, env=env)

    if result.returncode != 0:
        print()
        print(f"Pipeline stopped because {script_name} failed.")
        sys.exit(result.returncode)


def main():
    sermon_id = os.environ.get("SERMON_ID")
    if not sermon_id:
        print("SERMON_ID is missing. Set it before running this script.")
        print('Example: $env:SERMON_ID="sermon_004"')
        sys.exit(1)

    project_root = Path(__file__).resolve().parent.parent

    print(f"Target SERMON_ID: {sermon_id}", flush=True)
    for title, script_name in PIPELINE_STEPS:
        run_step(project_root, sermon_id, title, script_name)

    print()
    print("Full sermon pipeline complete.")
    print(f"Summary output: summaries/{sermon_id}_summary.md")
    print(f"Metadata output: metadata/{sermon_id}_metadata.json")


if __name__ == "__main__":
    main()
