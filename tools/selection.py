"""Selection and AI mask operations for Photoshop MCP."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from core.bridge import bridge
from core.jsx_templates import (
    select_rectangle_script,
    select_ellipse_script,
    SELECT_ALL,
    DESELECT,
    INVERT_SELECTION,
    feather_selection_script,
    expand_selection_script,
    contract_selection_script,
    GET_SELECTION_BOUNDS,
    select_subject_script,
    SELECT_SKY,
    CONTENT_AWARE_FILL
)


def select_rectangle(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> Dict[str, Any]:
    """Create a rectangular selection with optional feathering."""
    res = bridge.execute_jsx(select_rectangle_script(left, top, right, bottom, feather))
    if isinstance(res, dict):
        return res
    return {"ok": True, "bounds": [left, top, right, bottom]}


def select_ellipse(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> Dict[str, Any]:
    """Create an elliptical selection with optional feathering."""
    res = bridge.execute_jsx(select_ellipse_script(left, top, right, bottom, feather))
    if isinstance(res, dict):
        return res
    return {"ok": True, "bounds": [left, top, right, bottom]}


def select_all() -> Dict[str, Any]:
    """Select entire canvas."""
    res = bridge.execute_jsx(SELECT_ALL)
    return {"ok": True}


def deselect() -> Dict[str, Any]:
    """Clear active selection."""
    res = bridge.execute_jsx(DESELECT)
    return {"ok": True}


def invert_selection() -> Dict[str, Any]:
    """Invert active selection."""
    res = bridge.execute_jsx(INVERT_SELECTION)
    return {"ok": True}


def feather_selection(radius: float) -> Dict[str, Any]:
    """Feather the boundary of active selection."""
    res = bridge.execute_jsx(feather_selection_script(radius))
    return {"ok": True, "radius": radius}


def expand_selection(pixels: int) -> Dict[str, Any]:
    """Expand active selection by specified pixels."""
    res = bridge.execute_jsx(expand_selection_script(pixels))
    return {"ok": True, "pixels": pixels}


def contract_selection(pixels: int) -> Dict[str, Any]:
    """Contract active selection by specified pixels."""
    res = bridge.execute_jsx(contract_selection_script(pixels))
    return {"ok": True, "pixels": pixels}


def get_selection_bounds() -> Dict[str, Any]:
    """Get pixel bounds [left, top, right, bottom] of current selection."""
    res = bridge.execute_jsx(GET_SELECTION_BOUNDS)
    if isinstance(res, dict):
        return res
    return {"ok": True, "hasSelection": False, "bounds": None}


def select_subject(sample_all_layers: bool = True) -> Dict[str, Any]:
    """Use Adobe Sensei AI to automatically select primary subject(s)."""
    res = bridge.execute_jsx(select_subject_script(sample_all_layers))
    if isinstance(res, dict):
        return res
    return {"ok": True, "message": "Sensei Select Subject executed"}


def select_sky() -> Dict[str, Any]:
    """Use Adobe Sensei AI to automatically select the sky region."""
    res = bridge.execute_jsx(SELECT_SKY)
    if isinstance(res, dict):
        return res
    return {"ok": True, "message": "Sensei Select Sky executed"}


def content_aware_fill() -> Dict[str, Any]:
    """Apply Content-Aware Fill to the currently selected area."""
    res = bridge.execute_jsx(CONTENT_AWARE_FILL)
    if isinstance(res, dict):
        return res
    return {"ok": True, "message": "Content-Aware Fill applied"}
