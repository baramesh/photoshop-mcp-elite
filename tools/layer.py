"""Layer operations for Photoshop MCP."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from core.bridge import bridge
from core.jsx_templates import (
    GET_LAYERS,
    create_layer_script,
    select_layer_script,
    set_layer_visibility_script,
    set_layer_opacity_script,
    duplicate_layer_script,
    DELETE_ACTIVE_LAYER,
    MERGE_VISIBLE_LAYERS,
    FLATTEN_IMAGE
)


def get_layers() -> Dict[str, Any]:
    """Get list and attributes of all layers in the active document."""
    res = bridge.execute_jsx(GET_LAYERS)
    if isinstance(res, dict):
        return res
    return {"layers": []}


def create_layer(name: str = "Layer", opacity: float = 100.0, blend_mode: str = "normal") -> Dict[str, Any]:
    """Create a new art layer in the active document."""
    res = bridge.execute_jsx(create_layer_script(name, opacity, blend_mode))
    if isinstance(res, dict):
        return res
    return {"ok": True, "name": name}


def select_layer(name: str) -> Dict[str, Any]:
    """Select a layer by name to make it active."""
    res = bridge.execute_jsx(select_layer_script(name))
    if isinstance(res, dict):
        return res
    return {"ok": True, "activeLayer": name}


def set_layer_visibility(name: str, visible: bool) -> Dict[str, Any]:
    """Show or hide a layer by name."""
    res = bridge.execute_jsx(set_layer_visibility_script(name, visible))
    if isinstance(res, dict):
        return res
    return {"ok": True, "layer": name, "visible": visible}


def set_layer_opacity(name: str, opacity: float) -> Dict[str, Any]:
    """Set the opacity percentage (0-100) of a layer by name."""
    res = bridge.execute_jsx(set_layer_opacity_script(name, opacity))
    if isinstance(res, dict):
        return res
    return {"ok": True, "layer": name, "opacity": opacity}


def duplicate_layer(name: Optional[str] = None, new_name: Optional[str] = None) -> Dict[str, Any]:
    """Duplicate a layer (or active layer) with an optional new name."""
    res = bridge.execute_jsx(duplicate_layer_script(name, new_name))
    if isinstance(res, dict):
        return res
    return {"ok": True, "duplicated": name or "activeLayer"}


def delete_active_layer() -> Dict[str, Any]:
    """Delete the currently active layer."""
    res = bridge.execute_jsx(DELETE_ACTIVE_LAYER)
    if isinstance(res, dict):
        return res
    return {"ok": True}


def merge_visible_layers() -> Dict[str, Any]:
    """Merge all visible layers into one."""
    res = bridge.execute_jsx(MERGE_VISIBLE_LAYERS)
    if isinstance(res, dict):
        return res
    return {"ok": True}


def flatten_image() -> Dict[str, Any]:
    """Flatten all layers into a single background layer."""
    res = bridge.execute_jsx(FLATTEN_IMAGE)
    if isinstance(res, dict):
        return res
    return {"ok": True}
