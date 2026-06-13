"""CLI entry point for docshokage."""

import argparse
import json
import sys
from pathlib import Path

from .scanner import scan_project
from .filter import filter_files
from .sender import send_to_backend

CONFIG_DIR = Path.home() / ".docshokage"
CONFIG_FILE = CONFIG_DIR / "config.json"


# ── Config helpers ──────────────────────────────────────────────

def _load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}


def _save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


def _get_api_key() -> str | None:
    return _load_config().get("api_key")


def _set_api_key(key: str) -> None:
    cfg = _load_config()
    cfg["api_key"] = key
    _save_config(cfg)
    print(f"✅ API key saved to {CONFIG_FILE}")


def _get_project_id() -> str | None:
    return _load_config().get("project_id")


def _set_project_id(pid: str) -> None:
    cfg = _load_config()
    cfg["project_id"] = pid
    _save_config(cfg)
    print(f"✅ Project ID saved to {CONFIG_FILE}")


# ── Commands ────────────────────────────────────────────────────

def cmd_set_key(api_key: str) -> None:
    _set_api_key(api_key)


def cmd_arise(args: argparse.Namespace) -> None:
    api_key = _get_api_key()
    if not api_key:
        print(
            "❌ No API key configured.\n"
            "   Run:  docshokage --kagi <your-api-key>\n"
            "   to set your API key first."
        )
        sys.exit(1)

    project_id = args.project_id or _get_project_id()
    if not project_id:
        print(
            "❌ No project ID configured.\n"
            "   Run:  docshokage --set-project-id <your-project-id>\n"
            "   or pass:  docshokage arise --project-id <your-project-id>"
        )
        sys.exit(1)

    print("=" * 50)
    print("  📄 docshokage arise")
    print("=" * 50)

    # Step 1 – Scan
    scan_project(input_dir=args.input_dir)

    # Step 2 – Filter
    filter_files()

    # Step 3 – Send
    send_to_backend(
        api_url=args.api_url,
        api_key=api_key,
        project_id=project_id,
    )

    print("\n✅ Done — arise sent to backend!\n")


# ── Main ────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="docshokage",
        description="Scan a project, extract relevant files, and send them to a hosted backend.",
    )

    parser.add_argument(
        "--kagi",
        metavar="API_KEY",
        help="Save your API key so it can be used later.",
    )
    parser.add_argument(
        "--set-project-id",
        metavar="PROJECT_ID",
        help="Save your project ID so it can be used later.",
    )

    subparsers = parser.add_subparsers(dest="command")

    arise_parser = subparsers.add_parser("arise", help="Run the full extraction pipeline.")
    arise_parser.add_argument(
        "--input-dir",
        default=".",
        help="Project directory to scan (default: current directory).",
    )
    arise_parser.add_argument(
        "--api-url",
        default="https://docshokage-web.vercel.app",
        help="Backend URL to send data to.",
    )
    arise_parser.add_argument(
        "--project-id",
        help="Project ID to associate the documentation with (overrides saved value).",
    )

    args = parser.parse_args()

    # --kagi flag always takes precedence
    if args.kagi:
        cmd_set_key(args.kagi)
        return

    if args.set_project_id:
        _set_project_id(args.set_project_id)
        return

    if args.command == "arise":
        cmd_arise(args)
    else:
        parser.print_help()
