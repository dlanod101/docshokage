"""Scan a project directory and combine text files into a single markdown file."""

from pathlib import Path

# Default config
DEFAULT_TEXT_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".jsx", ".tsx",
    ".html", ".css", ".json", ".yaml", ".yml", ".xml",
    ".csv", ".sql", ".env.example",
}

DEFAULT_IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules",
    "dist", "build", "staticfiles", ".next", ".idea",
    ".vscode", "__pycache__", "migrations", "media",
}

DEFAULT_IGNORE_FILES = {
    "combined_output.md", ".env", "db.sqlite3",
}


def scan_project(
    input_dir: str,
    output_file: str = "combined_output.md",
    text_extensions: set | None = None,
    ignore_dirs: set | None = None,
    ignore_files: set | None = None,
) -> int:
    """Scan *input_dir*, collect all matching text files, and write them
    into *output_file* as a single markdown document.

    Returns the number of files processed.
    """
    text_extensions = text_extensions or DEFAULT_TEXT_EXTENSIONS
    ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS
    ignore_files = ignore_files or DEFAULT_IGNORE_FILES

    input_path = Path(input_dir)
    files_processed = 0

    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_path in sorted(input_path.rglob("*")):
            if not file_path.is_file():
                continue

            if any(part in ignore_dirs for part in file_path.parts):
                continue

            if file_path.name in ignore_files:
                continue

            if "management" in file_path.parts and "commands" in file_path.parts:
                continue

            if file_path.suffix.lower() not in text_extensions:
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                outfile.write("\n\n")
                outfile.write("=" * 100 + "\n")
                outfile.write(f"FILE: {file_path.relative_to(input_path)}\n")
                outfile.write("=" * 100 + "\n\n")
                outfile.write(content)
                outfile.write("\n")

                files_processed += 1
                print(f"Added: {file_path.relative_to(input_path)}")

            except Exception as e:
                print(f"Skipping {file_path}: {e}")

    print(f"\nProcessed {files_processed} files")
    print(f"Output saved to {output_file}")
    return files_processed

