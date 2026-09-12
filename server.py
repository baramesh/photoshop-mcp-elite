#!/usr/bin/env python3
"""Custom Photoshop Python MCP Server.

Native AppleScript / ExtendScript Bridge with Photographic Workflows.
"""

from __future__ import annotations

from typing import Any

from mcp.server.mcpserver import MCPServer

from core.bridge import bridge
from tools import adjustment, document, layer, selection, workflows

app = MCPServer("photoshop")


# --- Document Tools ---

@app.tool()
def photoshop_get_document_info() -> dict[str, Any]:
    """Get metadata about the currently active Photoshop document (dimensions, color mode, layers count, active layer)."""
    return document.get_document_info()


@app.tool()
def photoshop_list_documents() -> dict[str, Any]:
    """List all open documents in Photoshop with their IDs and names."""
    return document.list_documents()


@app.tool()
def photoshop_open_image(file_path: str) -> dict[str, Any]:
    """Open an image file from the filesystem into Photoshop."""
    return document.open_image(file_path)


@app.tool()
def photoshop_save_document(file_path: str | None = None) -> dict[str, Any]:
    """Save the active document, optionally specifying a new path."""
    return document.save_document(file_path)


@app.tool()
def photoshop_export_as(file_path: str, format_type: str = "png", quality: int = 90) -> dict[str, Any]:
    """Export the active document as PNG or JPEG."""
    return document.export_as(file_path, format_type, quality)


@app.tool()
def photoshop_undo() -> dict[str, Any]:
    """Undo the last action in Photoshop."""
    return document.undo()


@app.tool()
def photoshop_redo() -> dict[str, Any]:
    """Redo the last undone action in Photoshop."""
    return document.redo()


# --- Layer Tools ---

@app.tool()
def photoshop_get_layers() -> dict[str, Any]:
    """Get list, visibility, opacity, blend modes, and pixel bounds of all layers in the active document."""
    return layer.get_layers()


@app.tool()
def photoshop_create_layer(name: str = "Layer", opacity: float = 100.0, blend_mode: str = "normal") -> dict[str, Any]:
    """Create a new art layer with specified name and opacity."""
    return layer.create_layer(name, opacity, blend_mode)


@app.tool()
def photoshop_select_layer_by_name(name: str) -> dict[str, Any]:
    """Select a layer by name to make it active."""
    return layer.select_layer(name)


@app.tool()
def photoshop_set_layer_visibility(name: str, visible: bool) -> dict[str, Any]:
    """Show or hide a layer by name."""
    return layer.set_layer_visibility(name, visible)


@app.tool()
def photoshop_set_layer_opacity(name: str, opacity: float) -> dict[str, Any]:
    """Set the opacity percentage (0-100) of a layer by name."""
    return layer.set_layer_opacity(name, opacity)


@app.tool()
def photoshop_duplicate_layer(name: str | None = None, new_name: str | None = None) -> dict[str, Any]:
    """Duplicate a layer (or active layer) with an optional new name."""
    return layer.duplicate_layer(name, new_name)


@app.tool()
def photoshop_delete_layer() -> dict[str, Any]:
    """Delete the currently active layer."""
    return layer.delete_active_layer()


@app.tool()
def photoshop_merge_visible_layers() -> dict[str, Any]:
    """Merge all visible layers into one composite layer."""
    return layer.merge_visible_layers()


@app.tool()
def photoshop_flatten_image() -> dict[str, Any]:
    """Flatten all layers into a single background layer."""
    return layer.flatten_image()


# --- Selection Tools ---

@app.tool()
def photoshop_select_rectangle(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> dict[str, Any]:
    """Create a rectangular pixel selection [left, top, right, bottom] with optional feathering."""
    return selection.select_rectangle(left, top, right, bottom, feather)


@app.tool()
def photoshop_select_ellipse(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> dict[str, Any]:
    """Create an elliptical selection with optional feathering."""
    return selection.select_ellipse(left, top, right, bottom, feather)


@app.tool()
def photoshop_select_all() -> dict[str, Any]:
    """Select entire canvas area."""
    return selection.select_all()


@app.tool()
def photoshop_deselect() -> dict[str, Any]:
    """Deselect active selection."""
    return selection.deselect()


@app.tool()
def photoshop_invert_selection() -> dict[str, Any]:
    """Invert the active selection."""
    return selection.invert_selection()


@app.tool()
def photoshop_feather_selection(radius: float) -> dict[str, Any]:
    """Feather the edge of the active selection by radius pixels."""
    return selection.feather_selection(radius)


@app.tool()
def photoshop_expand_selection(pixels: int) -> dict[str, Any]:
    """Expand the active selection outwards by specified pixels."""
    return selection.expand_selection(pixels)


@app.tool()
def photoshop_contract_selection(pixels: int) -> dict[str, Any]:
    """Contract the active selection inwards by specified pixels."""
    return selection.contract_selection(pixels)


@app.tool()
def photoshop_get_selection_bounds() -> dict[str, Any]:
    """Get pixel bounds [left, top, right, bottom] of the current selection."""
    return selection.get_selection_bounds()


@app.tool()
def photoshop_select_subject(sample_all_layers: bool = True) -> dict[str, Any]:
    """Use Adobe Sensei AI to automatically detect and select the primary subject(s)."""
    return selection.select_subject(sample_all_layers)


@app.tool()
def photoshop_select_sky() -> dict[str, Any]:
    """Use Adobe Sensei AI to automatically detect and select the sky region."""
    return selection.select_sky()


@app.tool()
def photoshop_content_aware_fill() -> dict[str, Any]:
    """Fill the active selection using Content-Aware Fill."""
    return selection.content_aware_fill()


# --- Adjustment Tools ---

@app.tool()
def photoshop_adjust_brightness_contrast(brightness: int = 0, contrast: int = 0) -> dict[str, Any]:
    """Adjust brightness and contrast of the active layer (-100 to 100)."""
    return adjustment.adjust_brightness_contrast(brightness, contrast)


@app.tool()
def photoshop_adjust_curves_auto() -> dict[str, Any]:
    """Apply Auto Curves to the active layer."""
    return adjustment.adjust_curves_auto()


@app.tool()
def photoshop_adjust_hue_saturation(hue: int = 0, saturation: int = 0, lightness: int = 0) -> dict[str, Any]:
    """Adjust Hue, Saturation, and Lightness of the active layer."""
    return adjustment.adjust_hue_saturation(hue, saturation, lightness)


@app.tool()
def photoshop_auto_levels() -> dict[str, Any]:
    """Apply Auto Levels to the active layer."""
    return adjustment.auto_levels()


@app.tool()
def photoshop_auto_contrast() -> dict[str, Any]:
    """Apply Auto Contrast to the active layer."""
    return adjustment.auto_contrast()


@app.tool()
def photoshop_desaturate() -> dict[str, Any]:
    """Desaturate active layer to black and white."""
    return adjustment.desaturate()


@app.tool()
def photoshop_invert() -> dict[str, Any]:
    """Invert colors of the active layer."""
    return adjustment.invert()


@app.tool()
def photoshop_apply_gaussian_blur(radius: float) -> dict[str, Any]:
    """Apply Gaussian Blur filter to the active layer."""
    return adjustment.apply_gaussian_blur(radius)


# --- Smart Composite Workflows ---

@app.tool()
def photoshop_smart_remove_distractions(
    regions: list[list[int]],
    feather_px: float = 2.5,
    expand_px: int = 6,
    create_backup_layer: bool = True
) -> dict[str, Any]:
    """Smartly removes unwanted people or background distractions.
    Combines context expansion + edge feathering + Content-Aware Fill on a non-destructive Retouch layer.

    Args:
        regions: List of [left, top, right, bottom] bounding boxes in pixels.
        feather_px: Feather edge softness in pixels (default 2.5).
        expand_px: Context expansion in pixels to eliminate halo artifacts (default 6).
        create_backup_layer: If True, preserves the original layer and performs retouching on a duplicated layer.
    """
    return workflows.smart_remove_distractions(regions, feather_px, expand_px, create_backup_layer)


@app.tool()
def photoshop_harmonize_sky(
    sky_image_path: str,
    haze_opacity: float = 20.0,
    sky_opacity: float = 85.0,
    warm_foreground: bool = True
) -> dict[str, Any]:
    """Seamlessly replaces and harmonizes sky:
    1. Uses Sensei AI Select Sky for precise architectural contour isolation.
    2. Places and scales replacement sky image.
    3. Adds atmospheric horizon haze gradient layer to blend background naturally.
    4. Automatically relights foreground subjects with warm ambient light to match the sky.

    Args:
        sky_image_path: Local path to sky replacement image.
        haze_opacity: Opacity percentage (0-100) for horizon atmospheric haze.
        sky_opacity: Opacity percentage (0-100) for sky layer.
        warm_foreground: If True, warms non-sky foreground subjects with light tone curve matching.
    """
    return workflows.harmonize_sky(sky_image_path, haze_opacity, sky_opacity, warm_foreground)


@app.tool()
def photoshop_match_lighting_and_tone(
    target_mood: str = "vibrant_daylight",
    contrast_amount: int = 15,
    saturation_boost: int = 10
) -> dict[str, Any]:
    """Harmonizes lighting, contrast, and color vibrance across the entire composite."""
    return workflows.match_lighting_and_tone(target_mood, contrast_amount, saturation_boost)


@app.tool()
def photoshop_generative_fill_ai(prompt: str = "", wait_completion: bool = True) -> dict[str, Any]:
    """Autonomously triggers Adobe Firefly Generative Fill on the active selection."""
    return workflows.generative_fill_ai(prompt, wait_completion)


@app.tool()
def photoshop_generative_remove_ai(regions: list[list[int]], feather_px: float = 2.0) -> dict[str, Any]:
    """Autonomously removes regions using Adobe Firefly Generative Fill."""
    return workflows.generative_remove_ai(regions, feather_px)


@app.tool()
def photoshop_convert_to_smart_object() -> dict[str, Any]:
    """Convert the active layer or selected layers into a Smart Object."""
    return layer.convert_to_smart_object()


@app.tool()
def photoshop_create_adjustment_layer(adj_type: str = "curves", name: str | None = None) -> dict[str, Any]:
    """Create a non-destructive Adjustment Layer (curves, hue_saturation, levels, brightness_contrast, vibrance)."""
    return layer.create_adjustment_layer(adj_type, name)


@app.tool()
def photoshop_apply_camera_raw_filter(
    exposure: float = 0.0,
    contrast: int = 0,
    highlights: int = 0,
    shadows: int = 0,
    clarity: int = 0,
    dehaze: int = 0,
    vibrance: int = 0,
    saturation: int = 0,
    temperature: int = 0,
    tint: int = 0
) -> dict[str, Any]:
    """Apply professional Adobe Camera Raw Filter with exposure, clarity, dehaze, temperature, and vibrance controls."""
    return adjustment.apply_camera_raw_filter(
        exposure=exposure,
        contrast=contrast,
        highlights=highlights,
        shadows=shadows,
        clarity=clarity,
        dehaze=dehaze,
        vibrance=vibrance,
        saturation=saturation,
        temperature=temperature,
        tint=tint
    )


@app.tool()
def photoshop_add_text_layer(
    text: str,
    font_name: str = "Helvetica",
    font_size_pt: float = 24.0,
    color_hex: str = "FFFFFF",
    x_px: float = 100.0,
    y_px: float = 100.0,
    justification: str = "left"
) -> dict[str, Any]:
    """Create a vector typography Text Layer in the active document."""
    return layer.add_text_layer(text, font_name, font_size_pt, color_hex, x_px, y_px, justification)


@app.tool()
def photoshop_apply_layer_style(
    drop_shadow: bool = False,
    shadow_opacity: float = 50.0,
    shadow_distance: int = 5,
    shadow_size: int = 10,
    stroke: bool = False,
    stroke_size: int = 2,
    stroke_color_hex: str = "000000"
) -> dict[str, Any]:
    """Apply Layer Styles (FX) like Drop Shadow and Stroke to the active layer."""
    return layer.apply_layer_style(
        drop_shadow=drop_shadow,
        shadow_opacity=shadow_opacity,
        shadow_distance=shadow_distance,
        shadow_size=shadow_size,
        stroke=stroke,
        stroke_size=stroke_size,
        stroke_color_hex=stroke_color_hex
    )


@app.tool()
def photoshop_execute_custom_jsx(script: str) -> dict[str, Any]:
    """Execute raw ES3 ExtendScript code directly inside Photoshop with full JSON serialization."""
    res = bridge.execute_jsx(script)
    return {"ok": True, "result": res}



def main():
    """Run the Photoshop MCP server over stdio."""
    app.run(transport="stdio")


if __name__ == "__main__":
    main()

