"""Send filtered file data to a hosted backend."""

import re
from pathlib import Path

import requests


def send_to_backend(
    input_md: str = "filtered_files.md",
    api_url: str = "https://docshokage-web.vercel.app",
    api_key: str = "",
    project_id: str = "",
    title: str = "Untitled Documentation",
) -> dict:
    """Parse *input_md* into structured file entries and POST them to
    the hosted backend at *api_url* using the ``/api/docs/with-key`` endpoint.

    Returns the JSON response from the server.
    """
    with open(input_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse file blocks
    pattern = r"=+\nFILE:\s+(.*?)\n=+\n\n"
    matches = list(re.finditer(pattern, content))

    files = []
    for i, match in enumerate(matches):
        file_path = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        file_content = content[start:end].strip()

        parts = Path(file_path).parts
        app_name = parts[0] if len(parts) > 1 else "root"

        files.append({
            "app": app_name,
            "path": file_path,
            "content": file_content,
        })

    payload = {
        "api_key": api_key,
        "project_id": project_id,
        "title": title,
        "content": {"files": files},
    }

    url = f"{api_url.rstrip('/')}/api/docs/with-key"
    print(f"Sending {len(files)} files to {url} ...")

    resp = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=60,
    )
    resp.raise_for_status()

    result = resp.json()
    print(f"Backend responded: {result}")
    return result
