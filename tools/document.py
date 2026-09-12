"""Document operations for Photoshop MCP."""

from __future__ import annotations

from typing import Any, Dict, Optional
from core.bridge import bridge
from core.jsx_templates import (
    GET_DOCUMENT_INFO,
    LIST_DOCUMENTS,
    open_document_script,
    save_document_script,
    export_as_script,
    UNDO,
    REDO
)


def get_document_info() -> Dict[str, Any]:
    """Get metadata about the currently active Photoshop document."""
    res = bridge.execute_jsx(GET_DOCUMENT_INFO)
    if isinstance(res, dict):
        return res
    return {"status": "ok", "raw": res}


def list_documents() -> Dict[str, Any]:
    """List all open documents in Photoshop."""
    res = bridge.execute_jsx(LIST_DOCUMENTS)
    if isinstance(res, dict):
        return res
    return {"count": 0, "documents": []}


def open_image(file_path: str) -> Dict[str, Any]:
    """Open an image file into Photoshop."""
    res = bridge.execute_jsx(open_document_script(file_path))
    if isinstance(res, dict):
        return res
    return {"ok": True, "result": res}


def save_document(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Save the active document, optionally specifying a new path."""
    res = bridge.execute_jsx(save_document_script(file_path))
    if isinstance(res, dict):
        return res
    return {"ok": True, "result": res}


def export_as(file_path: str, format_type: str = "png", quality: int = 90) -> Dict[str, Any]:
    """Export the active document as PNG or JPEG."""
    res = bridge.execute_jsx(export_as_script(file_path, format_type, quality))
    if isinstance(res, dict):
        return res
    return {"ok": True, "path": file_path}


def undo() -> Dict[str, Any]:
    """Undo the last action in Photoshop."""
    res = bridge.execute_jsx(UNDO)
    return {"ok": True, "action": "undo"}


def redo() -> Dict[str, Any]:
    """Redo the last undone action in Photoshop."""
    res = bridge.execute_jsx(REDO)
    return {"ok": True, "action": "redo"}
