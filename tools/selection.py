"""Selection and AI mask operations for Photoshop MCP."""

from __future__ import annotations

from typing import Any

from core.bridge import bridge
from core.jsx_templates import (
    CONTENT_AWARE_FILL,
    DESELECT,
    GET_SELECTION_BOUNDS,
    INVERT_SELECTION,
    SELECT_ALL,
    SELECT_SKY,
    contract_selection_script,
    expand_selection_script,
    feather_selection_script,
    select_ellipse_script,
    select_rectangle_script,
    select_subject_script,
)


def select_rectangle(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> dict[str, Any]:
    """Create a rectangular selection with optional feathering."""
    res = bridge.execute_jsx(select_rectangle_script(left, top, right, bottom, feather))
    if isinstance(res, dict):
        return res
    return {"ok": True, "bounds": [left, top, right, bottom]}


def select_ellipse(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> dict[str, Any]:
    """Create an elliptical selection with optional feathering."""
    res = bridge.execute_jsx(select_ellipse_script(left, top, right, bottom, feather))
    if isinstance(res, dict):
        return res
    return {"ok": True, "bounds": [left, top, right, bottom]}


def select_all() -> dict[str, Any]:
    """Select entire canvas."""
    bridge.execute_jsx(SELECT_ALL)
    return {"ok": True}


def deselect() -> dict[str, Any]:
    """Clear active selection."""
    bridge.execute_jsx(DESELECT)
    return {"ok": True}


def invert_selection() -> dict[str, Any]:
    """Invert active selection."""
    bridge.execute_jsx(INVERT_SELECTION)
    return {"ok": True}


def feather_selection(radius: float) -> dict[str, Any]:
    """Feather the boundary of active selection."""
    bridge.execute_jsx(feather_selection_script(radius))
    return {"ok": True, "radius": radius}


def expand_selection(pixels: int) -> dict[str, Any]:
    """Expand active selection by specified pixels."""
    bridge.execute_jsx(expand_selection_script(pixels))
    return {"ok": True, "pixels": pixels}


def contract_selection(pixels: int) -> dict[str, Any]:
    """Contract active selection by specified pixels."""
    bridge.execute_jsx(contract_selection_script(pixels))
    return {"ok": True, "pixels": pixels}


def get_selection_bounds() -> dict[str, Any]:
    """Get pixel bounds [left, top, right, bottom] of current selection."""
    res = bridge.execute_jsx(GET_SELECTION_BOUNDS)
    if isinstance(res, dict):
        return res
    return {"ok": True, "hasSelection": False, "bounds": None}


def select_subject(sample_all_layers: bool = True) -> dict[str, Any]:
    """Use Adobe Sensei AI to automatically select primary subject(s)."""
    res = bridge.execute_jsx(select_subject_script(sample_all_layers))
    if isinstance(res, dict):
        return res
    return {"ok": True, "message": "Sensei Select Subject executed"}


def select_sky() -> dict[str, Any]:
    """Use Adobe Sensei AI to automatically select the sky region."""
    res = bridge.execute_jsx(SELECT_SKY)
    if isinstance(res, dict):
        return res
    return {"ok": True, "message": "Sensei Select Sky executed"}


def content_aware_fill() -> dict[str, Any]:
    """Apply Content-Aware Fill to the currently selected area."""
    res = bridge.execute_jsx(CONTENT_AWARE_FILL)
    if isinstance(res, dict):
        return res
    return {"ok": True, "message": "Content-Aware Fill applied"}
