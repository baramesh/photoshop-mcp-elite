"""Layer operations for Photoshop MCP."""

from __future__ import annotations

from typing import Any

from core.bridge import bridge
from core.jsx_templates import (
    DELETE_ACTIVE_LAYER,
    FLATTEN_IMAGE,
    GET_LAYERS,
    MERGE_VISIBLE_LAYERS,
    create_layer_script,
    duplicate_layer_script,
    select_layer_script,
    set_layer_opacity_script,
    set_layer_visibility_script,
)


def get_layers() -> dict[str, Any]:
    """Get list and attributes of all layers in the active document."""
    res = bridge.execute_jsx(GET_LAYERS)
    if isinstance(res, dict):
        return res
    return {"layers": []}


def create_layer(name: str = "Layer", opacity: float = 100.0, blend_mode: str = "normal") -> dict[str, Any]:
    """Create a new art layer in the active document."""
    res = bridge.execute_jsx(create_layer_script(name, opacity, blend_mode))
    if isinstance(res, dict):
        return res
    return {"ok": True, "name": name}


def select_layer(name: str) -> dict[str, Any]:
    """Select a layer by name to make it active."""
    res = bridge.execute_jsx(select_layer_script(name))
    if isinstance(res, dict):
        return res
    return {"ok": True, "activeLayer": name}


def set_layer_visibility(name: str, visible: bool) -> dict[str, Any]:
    """Show or hide a layer by name."""
    res = bridge.execute_jsx(set_layer_visibility_script(name, visible))
    if isinstance(res, dict):
        return res
    return {"ok": True, "layer": name, "visible": visible}


def set_layer_opacity(name: str, opacity: float) -> dict[str, Any]:
    """Set the opacity percentage (0-100) of a layer by name."""
    res = bridge.execute_jsx(set_layer_opacity_script(name, opacity))
    if isinstance(res, dict):
        return res
    return {"ok": True, "layer": name, "opacity": opacity}


def duplicate_layer(name: str | None = None, new_name: str | None = None) -> dict[str, Any]:
    """Duplicate a layer (or active layer) with an optional new name."""
    res = bridge.execute_jsx(duplicate_layer_script(name, new_name))
    if isinstance(res, dict):
        return res
    return {"ok": True, "duplicated": name or "activeLayer"}


def delete_active_layer() -> dict[str, Any]:
    """Delete the currently active layer."""
    res = bridge.execute_jsx(DELETE_ACTIVE_LAYER)
    if isinstance(res, dict):
        return res
    return {"ok": True}


def merge_visible_layers() -> dict[str, Any]:
    """Merge all visible layers into one."""
    res = bridge.execute_jsx(MERGE_VISIBLE_LAYERS)
    if isinstance(res, dict):
        return res
    return {"ok": True}


def flatten_image() -> dict[str, Any]:
    """Flatten all layers into a single background layer."""
    res = bridge.execute_jsx(FLATTEN_IMAGE)
    if isinstance(res, dict):
        return res
    return {"ok": True}
