"""docshokage — scan, filter, and send project files to a hosted backend."""

from .scanner import scan_project
from .filter import filter_files
from .sender import send_to_backend

__all__ = ["scan_project", "filter_files", "send_to_backend"]
