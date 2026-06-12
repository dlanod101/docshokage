"""Filter a combined markdown file to keep only relevant file sections."""

import re
from pathlib import Path

DEFAULT_TARGET_PATTERNS = {"view", "model", "serializer", "url"}


def filter_files(
    input_md: str = "combined_output.md",
    output_md: str = "filtered_files.md",
    target_patterns: set | None = None,
) -> list[str]:
    """Read *input_md*, keep sections whose filename matches any of the
    *target_patterns*, and write them into *output_md*.

    Returns the list of selected section strings.
    """
    target_patterns = target_patterns or DEFAULT_TARGET_PATTERNS

    with open(input_md, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(={10,}\nFILE:\s+(.*?)\n={10,}\n\n)"
    matches = list(re.finditer(pattern, content, re.DOTALL))

    selected_sections = []

    for i, match in enumerate(matches):
        file_path = match.group(2).strip()
        filename = Path(file_path).name

        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

        section = content[start:end]

        if any(p in filename.lower() for p in target_patterns):
            selected_sections.append(section)

    with open(output_md, "w", encoding="utf-8") as f:
        f.write("\n\n".join(selected_sections))

    print(f"Extracted {len(selected_sections)} files to {output_md}")
    return selected_sections


if __name__ == "__main__":
    filter_files()
