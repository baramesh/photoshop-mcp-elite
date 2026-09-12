"""Adjustments, color, and filters for Photoshop MCP."""

from __future__ import annotations

from typing import Any, Dict
from core.bridge import bridge
from core.jsx_templates import (
    adjust_brightness_contrast_script,
    adjust_curves_auto_script,
    adjust_hue_saturation_script,
    AUTO_LEVELS,
    AUTO_CONTRAST,
    DESATURATE,
    INVERT,
    apply_gaussian_blur_script
)


def adjust_brightness_contrast(brightness: int = 0, contrast: int = 0) -> Dict[str, Any]:
    """Adjust brightness and contrast of the active layer (-100 to 100)."""
    res = bridge.execute_jsx(adjust_brightness_contrast_script(brightness, contrast))
    if isinstance(res, dict):
        return res
    return {"ok": True, "brightness": brightness, "contrast": contrast}


def adjust_curves_auto() -> Dict[str, Any]:
    """Apply auto Curves algorithm to active layer."""
    res = bridge.execute_jsx(adjust_curves_auto_script())
    if isinstance(res, dict):
        return res
    return {"ok": True}


def adjust_hue_saturation(hue: int = 0, saturation: int = 0, lightness: int = 0) -> Dict[str, Any]:
    """Adjust Hue (-180..180), Saturation (-100..100), and Lightness (-100..100)."""
    res = bridge.execute_jsx(adjust_hue_saturation_script(hue, saturation, lightness))
    if isinstance(res, dict):
        return res
    return {"ok": True, "hue": hue, "saturation": saturation, "lightness": lightness}


def auto_levels() -> Dict[str, Any]:
    """Apply Auto Levels to active layer."""
    res = bridge.execute_jsx(AUTO_LEVELS)
    return {"ok": True}


def auto_contrast() -> Dict[str, Any]:
    """Apply Auto Contrast to active layer."""
    res = bridge.execute_jsx(AUTO_CONTRAST)
    return {"ok": True}


def desaturate() -> Dict[str, Any]:
    """Desaturate the active layer to grayscale."""
    res = bridge.execute_jsx(DESATURATE)
    return {"ok": True}


def invert() -> Dict[str, Any]:
    """Invert colors of the active layer."""
    res = bridge.execute_jsx(INVERT)
    return {"ok": True}


def apply_gaussian_blur(radius: float) -> Dict[str, Any]:
    """Apply Gaussian Blur to active layer with given pixel radius."""
    res = bridge.execute_jsx(apply_gaussian_blur_script(radius))
    if isinstance(res, dict):
        return res
    return {"ok": True, "radius": radius}
