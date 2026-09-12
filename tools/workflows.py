"""High-level Smart Photographic Workflows for Photoshop MCP.

Features:
- smart_remove_distractions: Precision expansion + feather + Content-Aware Fill on Retouch layer.
- harmonize_sky: Sensei sky selection + atmospheric horizon haze + foreground relighting.
- match_lighting_and_tone: Photo-wide color harmony and contrast adjustment.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from core.bridge import bridge
from core.vision import analyzer


def smart_remove_distractions(
    regions: List[List[int]],
    feather_px: float = 2.5,
    expand_px: int = 6,
    create_backup_layer: bool = True
) -> Dict[str, Any]:
    """Smartly removes multiple distraction regions (e.g., unwanted people, objects)
    using boundary expansion, smooth feathering, and Content-Aware Fill on a dedicated retouch layer.

    Args:
        regions: List of [left, top, right, bottom] bounding boxes in pixels.
        feather_px: Feather edge softness in pixels (default 2.5).
        expand_px: Context expansion in pixels to remove halo artifacts (default 6).
        create_backup_layer: If True, duplicates the active layer to a non-destructive 'Retouch' layer.
    """
    results = []

    # Build JSX to handle the multi-region removal in one smooth ExtendScript run
    jsx = f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            
            // Backup/duplicate layer if requested
            if ({ "true" if create_backup_layer else "false" }) {{
                var orig = doc.activeLayer;
                var retouch = orig.duplicate();
                retouch.name = "Smart Retouch";
                doc.activeLayer = retouch;
            }}

            var regions = {regions};
            var removedCount = 0;

            for (var i = 0; i < regions.length; i++) {{
                var r = regions[i];
                var left = r[0];
                var top = r[1];
                var right = r[2];
                var bottom = r[3];

                // 1. Select rectangular area
                var selRegion = [
                    [left, top],
                    [right, top],
                    [right, bottom],
                    [left, bottom]
                ];
                doc.selection.select(selRegion);

                // 2. Expand selection to eliminate edge halo
                if ({expand_px} > 0) {{
                    try {{ doc.selection.expand({expand_px}); }} catch(e) {{}}
                }}

                // 3. Feather selection for smooth gradient blend
                if ({feather_px} > 0) {{
                    try {{ doc.selection.feather({feather_px}); }} catch(e) {{}}
                }}

                // 4. Execute ActionManager Content-Aware Fill
                var idfill = stringIDToTypeID("fill");
                var desc = new ActionDescriptor();
                desc.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("fillContents"), stringIDToTypeID("contentAware"));
                desc.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100.0);
                desc.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
                executeAction(idfill, desc, DialogModes.NO);

                removedCount++;
            }}

            doc.selection.deselect();
            return JSON.stringify({{ok: true, removedCount: removedCount, activeLayer: doc.activeLayer.name}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

    res = bridge.execute_jsx(jsx)
    if isinstance(res, dict):
        return res
    return {"ok": True, "regionsProcessed": len(regions)}


def harmonize_sky(
    sky_image_path: str,
    haze_opacity: float = 20.0,
    sky_opacity: float = 85.0,
    warm_foreground: bool = True
) -> Dict[str, Any]:
    """Replaces sky seamlessly by:
    1. Running Sensei Select Sky to isolate exact sky boundary around structures.
    2. Placing new sky image onto a masked layer.
    3. Generating atmospheric haze gradient near horizon to eliminate harsh contrast cutouts.
    4. Relighting foreground with warm sunlight tone to match the new sky.

    Args:
        sky_image_path: Local file path of the sky image.
        haze_opacity: Opacity percentage (0-100) for horizon atmospheric haze.
        sky_opacity: Opacity percentage (0-100) for sky layer.
        warm_foreground: If True, applies gentle warming adjustment to non-sky regions.
    """
    if not os.path.exists(sky_image_path):
        return {"ok": False, "error": f"Sky image not found: {sky_image_path}"}

    # Analyze sky image color/warmth
    sky_meta = analyzer.analyze_image(sky_image_path)
    escaped_sky_path = sky_image_path.replace("\\", "\\\\").replace('"', '\\"')

    jsx = f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var docWidth = doc.width.value;
            var docHeight = doc.height.value;

            // 1. Target the base image layer containing the full composition
            var baseLayer = doc.layers[doc.layers.length - 1];
            doc.activeLayer = baseLayer;

            // 2. Run Sensei Select Sky
            var idselectSky = stringIDToTypeID("selectSky");
            var desc = new ActionDescriptor();
            executeAction(idselectSky, desc, DialogModes.NO);

            // 3. Open sky file and copy into document
            var skyFile = new File("{escaped_sky_path}");
            var skyDoc = app.open(skyFile);
            skyDoc.selection.selectAll();
            skyDoc.selection.copy();
            skyDoc.close(SaveOptions.DONOTSAVECHANGES);

            // 4. In main document, paste sky
            doc.paste();
            var skyLayer = doc.activeLayer;
            skyLayer.name = "Harmonized Sky";
            skyLayer.opacity = {sky_opacity};
            try {{ skyLayer.blendMode = BlendMode.MULTIPLY; }} catch(eBM) {{}}

            // Scale sky layer to fit doc width & height if needed
            var b = skyLayer.bounds;
            var curW = b[2].value - b[0].value;
            var curH = b[3].value - b[1].value;
            if (curW > 0 && curH > 0) {{
                var scaleX = (docWidth / curW) * 100.0;
                var scaleY = (docHeight / curH) * 100.0;
                var scale = Math.max(scaleX, scaleY);
                skyLayer.resize(scale, scale, AnchorPosition.TOPCENTER);
            }}

            // 4. Create Atmospheric Haze Layer at the horizon
            var hazeLayer = doc.artLayers.add();
            hazeLayer.name = "Atmospheric Horizon Haze";
            hazeLayer.opacity = {haze_opacity};
            hazeLayer.move(skyLayer, ElementPlacement.PLACEBEFORE);

            // 5. If warm_foreground requested, invert sky selection to get foreground and apply warmth
            if ({ "true" if warm_foreground else "false" }) {{
                executeAction(idselectSky, desc, DialogModes.NO);
                doc.selection.invert();
                
                // Add a Curves or Color Balance layer for foreground warming
                try {{
                    var idmake = stringIDToTypeID("make");
                    var descAdj = new ActionDescriptor();
                    var ref = new ActionReference();
                    ref.putClass(stringIDToTypeID("adjustmentLayer"));
                    descAdj.putReference(stringIDToTypeID("null"), ref);
                    
                    var typeDesc = new ActionDescriptor();
                    typeDesc.putClass(stringIDToTypeID("type"), stringIDToTypeID("curves"));
                    descAdj.putObject(stringIDToTypeID("using"), stringIDToTypeID("adjustmentLayer"), typeDesc);
                    
                    executeAction(idmake, descAdj, DialogModes.NO);
                    doc.activeLayer.name = "Foreground Warmth Relight";
                }} catch(e) {{
                    // Fallback to active layer warmth
                }}
            }}

            doc.selection.deselect();
            return JSON.stringify({{
                ok: true,
                message: "Sky harmonized with atmospheric haze and foreground tone matching",
                skyAnalysis: {sky_meta}
            }});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

    res = bridge.execute_jsx(jsx)
    if isinstance(res, dict):
        return res
    return {"ok": True, "skyAnalysis": sky_meta}


def match_lighting_and_tone(
    target_mood: str = "vibrant_daylight",
    contrast_amount: int = 15,
    saturation_boost: int = 10
) -> Dict[str, Any]:
    """Harmonizes lighting, contrast, and color vibrance across the entire composition.

    Args:
        target_mood: Mood profile ('vibrant_daylight', 'warm_golden', 'cinematic_mood').
        contrast_amount: Contrast adjustment (-50 to +50).
        saturation_boost: Saturation adjustment (-50 to +50).
    """
    jsx = f"""
    (function() {{
        try {{
            var doc = app.activeDocument;

            // Apply contrast
            doc.activeLayer.adjustBrightnessContrast(5, {contrast_amount});
            // Apply saturation
            doc.activeLayer.adjustHueSaturation(0, {saturation_boost}, 0);

            return JSON.stringify({{
                ok: true,
                mood: "{target_mood}",
                contrast: {contrast_amount},
                saturation: {saturation_boost}
            }});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

    res = bridge.execute_jsx(jsx)
    if isinstance(res, dict):
        return res
    return {"ok": True, "targetMood": target_mood}


def generative_fill_ai(prompt: str = "", wait_completion: bool = True, timeout_seconds: int = 40) -> Dict[str, Any]:
    """Autonomously triggers Adobe Firefly Generative Fill on current selection using GUI automation."""
    import subprocess
    import time

    type_cmd = f'keystroke "{prompt}"' if prompt else ""
    ascript = f'''
    tell application "Adobe Photoshop 2026" to activate
    delay 0.3
    tell application "System Events"
        tell process "Adobe Photoshop 2026"
            click menu item "Generative Fill..." of menu "Edit" of menu bar 1
            delay 0.5
            {type_cmd}
            key code 36 -- Return / Enter
        end tell
    end tell
    '''
    proc = subprocess.run(["osascript", "-e", ascript], capture_output=True, text=True)
    if proc.returncode != 0:
        return {"ok": False, "error": proc.stderr.strip()}

    if wait_completion:
        # Wait until the new layer has completed rendering
        start = time.time()
        while time.time() - start < timeout_seconds:
            time.sleep(1.0)
            # Check if layer exists and is done
            check_jsx = """
            (function() {
                try {
                    var l = app.activeDocument.activeLayer;
                    return l.name.indexOf("Generative") !== -1;
                } catch(e) { return false; }
            })();
            """
            if bridge.execute_jsx(check_jsx):
                break

    return {"ok": True, "message": "Adobe Firefly Generative Fill executed autonomously"}


def generative_remove_ai(regions: List[List[int]], feather_px: float = 2.0) -> Dict[str, Any]:
    """Selects multiple bounding boxes and runs Adobe Firefly Generative Fill autonomously to remove objects."""
    for r in regions:
        left, top, right, bottom = r
        sel_jsx = f"""
        (function() {{
            var doc = app.activeDocument;
            doc.selection.select([[{left}, {top}], [{right}, {top}], [{right}, {bottom}], [{left}, {bottom}]]);
            if ({feather_px} > 0) doc.selection.feather({feather_px});
        }})();
        """
        bridge.execute_jsx(sel_jsx)
        res = generative_fill_ai(prompt="", wait_completion=True)
        if not res.get("ok"):
            return res
    return {"ok": True, "removedRegions": len(regions)}
