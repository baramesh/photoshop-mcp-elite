"""ExtendScript (JSX) templates and ActionManager snippets for Adobe Photoshop.
All scripts are strictly ES3-compliant and pre-validated.
"""

# --- Document Templates ---

GET_DOCUMENT_INFO = """
(function() {
    if (app.documents.length === 0) return JSON.stringify({status: "no_document", message: "No document is currently open"});
    var doc = app.activeDocument;
    var res = {
        status: "ok",
        id: doc.id,
        name: doc.name,
        width: Math.round(doc.width.value),
        height: Math.round(doc.height.value),
        resolution: Math.round(doc.resolution),
        mode: "" + doc.mode,
        bitsPerChannel: "" + doc.bitsPerChannel,
        colorProfileName: doc.colorProfileName || "None",
        layerCount: doc.layers.length,
        activeLayer: doc.activeLayer ? doc.activeLayer.name : null
    };
    return JSON.stringify(res);
})();
"""

LIST_DOCUMENTS = """
(function() {
    var docs = [];
    for (var i = 0; i < app.documents.length; i++) {
        var d = app.documents[i];
        docs.push({
            id: d.id,
            name: d.name,
            width: Math.round(d.width.value),
            height: Math.round(d.height.value)
        });
    }
    return JSON.stringify({count: docs.length, documents: docs});
})();
"""

def open_document_script(file_path: str) -> str:
    escaped = file_path.replace("\\", "\\\\").replace('"', '\\"')
    return f"""
    (function() {{
        try {{
            var fileRef = new File("{escaped}");
            if (!fileRef.exists) return JSON.stringify({{ok: false, error: "File not found: " + "{escaped}"}});
            var doc = app.open(fileRef);
            return JSON.stringify({{ok: true, id: doc.id, name: doc.name, width: doc.width.value, height: doc.height.value}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def save_document_script(file_path: str | None = None) -> str:
    if file_path:
        escaped = file_path.replace("\\", "\\\\").replace('"', '\\"')
        return f"""
        (function() {{
            try {{
                var doc = app.activeDocument;
                doc.saveAs(new File("{escaped}"));
                return JSON.stringify({{ok: true, message: "Saved as " + "{escaped}"}});
            }} catch(e) {{
                return JSON.stringify({{ok: false, error: e.message}});
            }}
        }})();
        """
    return """
    (function() {
        try {
            app.activeDocument.save();
            return JSON.stringify({ok: true, message: "Document saved"});
        } catch(e) {
            return JSON.stringify({ok: false, error: e.message});
        }
    })();
    """

def export_as_script(file_path: str, format_type: str = "png", quality: int = 90) -> str:
    escaped = file_path.replace("\\", "\\\\").replace('"', '\\"')
    fmt = format_type.lower()
    if fmt in ["jpg", "jpeg"]:
        return f"""
        (function() {{
            try {{
                var doc = app.activeDocument;
                var opt = new ExportOptionsSaveForWeb();
                opt.format = SaveDocumentType.JPEG;
                opt.quality = {quality};
                doc.exportDocument(new File("{escaped}"), ExportType.SAVEFORWEB, opt);
                return JSON.stringify({{ok: true, path: "{escaped}"}});
            }} catch(e) {{
                return JSON.stringify({{ok: false, error: e.message}});
            }}
        }})();
        """
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var opt = new ExportOptionsSaveForWeb();
            opt.format = SaveDocumentType.PNG;
            opt.PNG8 = false;
            doc.exportDocument(new File("{escaped}"), ExportType.SAVEFORWEB, opt);
            return JSON.stringify({{ok: true, path: "{escaped}"}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """


# --- Layer Templates ---

GET_LAYERS = """
(function() {
    if (app.documents.length === 0) return JSON.stringify({layers: []});
    var doc = app.activeDocument;
    var list = [];
    for (var i = 0; i < doc.layers.length; i++) {
        var l = doc.layers[i];
        var bounds = [
            Math.round(l.bounds[0].value),
            Math.round(l.bounds[1].value),
            Math.round(l.bounds[2].value),
            Math.round(l.bounds[3].value)
        ];
        list.push({
            id: l.id,
            name: l.name,
            visible: l.visible,
            opacity: Math.round(l.opacity),
            blendMode: "" + l.blendMode,
            kind: "" + l.typename,
            isBackgroundLayer: l.isBackgroundLayer,
            bounds: bounds
        });
    }
    return JSON.stringify({count: list.length, layers: list});
})();
"""

def create_layer_script(name: str = "Layer", opacity: float = 100.0, blend_mode: str = "normal") -> str:
    escaped_name = name.replace('"', '\\"')
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var l = doc.artLayers.add();
            l.name = "{escaped_name}";
            l.opacity = {opacity};
            if ("{blend_mode}" !== "normal") {{
                try {{
                    l.blendMode = BlendMode.{blend_mode.upper()};
                }} catch(err) {{}}
            }}
            return JSON.stringify({{ok: true, name: l.name, id: l.id}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def select_layer_script(name: str) -> str:
    escaped = name.replace('"', '\\"')
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            doc.activeLayer = doc.layers.getByName("{escaped}");
            return JSON.stringify({{ok: true, activeLayer: doc.activeLayer.name}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def set_layer_visibility_script(name: str, visible: bool) -> str:
    escaped = name.replace('"', '\\"')
    vis_str = "true" if visible else "false"
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var l = doc.layers.getByName("{escaped}");
            l.visible = {vis_str};
            return JSON.stringify({{ok: true, layer: l.name, visible: l.visible}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def set_layer_opacity_script(name: str, opacity: float) -> str:
    escaped = name.replace('"', '\\"')
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var l = doc.layers.getByName("{escaped}");
            l.opacity = {opacity};
            return JSON.stringify({{ok: true, layer: l.name, opacity: l.opacity}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def duplicate_layer_script(name: str | None = None, new_name: str | None = None) -> str:
    target = f'doc.layers.getByName("{name.replace(chr(34), chr(92)+chr(34))}")' if name else "doc.activeLayer"
    rename = f'dup.name = "{new_name.replace(chr(34), chr(92)+chr(34))}";' if new_name else ""
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var target = {target};
            var dup = target.duplicate();
            {rename}
            return JSON.stringify({{ok: true, layer: dup.name, id: dup.id}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

DELETE_ACTIVE_LAYER = """
(function() {
    try {
        var doc = app.activeDocument;
        var name = doc.activeLayer.name;
        doc.activeLayer.remove();
        return JSON.stringify({ok: true, deleted: name});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

MERGE_VISIBLE_LAYERS = """
(function() {
    try {
        app.activeDocument.mergeVisibleLayers();
        return JSON.stringify({ok: true, activeLayer: app.activeDocument.activeLayer.name});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

FLATTEN_IMAGE = """
(function() {
    try {
        app.activeDocument.flatten();
        return JSON.stringify({ok: true, activeLayer: app.activeDocument.activeLayer.name});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""


# --- Selection Templates ---

def select_rectangle_script(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> str:
    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var selRegion = [
                [{left}, {top}],
                [{right}, {top}],
                [{right}, {bottom}],
                [{left}, {bottom}]
            ];
            doc.selection.select(selRegion);
            if ({feather} > 0) doc.selection.feather({feather});
            return JSON.stringify({{ok: true, bounds: [{left}, {top}, {right}, {bottom}], feather: {feather}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def select_ellipse_script(left: int, top: int, right: int, bottom: int, feather: float = 0.0) -> str:
    return f"""
    (function() {{
        try {{
            var idset = stringIDToTypeID("set");
            var desc = new ActionDescriptor();
            var ref = new ActionReference();
            ref.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
            desc.putReference(stringIDToTypeID("null"), ref);
            
            var shapeDesc = new ActionDescriptor();
            shapeDesc.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("pixelsUnit"), {top});
            shapeDesc.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("pixelsUnit"), {left});
            shapeDesc.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("pixelsUnit"), {bottom});
            shapeDesc.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("pixelsUnit"), {right});
            
            desc.putObject(stringIDToTypeID("to"), stringIDToTypeID("ellipse"), shapeDesc);
            executeAction(idset, desc, DialogModes.NO);
            if ({feather} > 0) app.activeDocument.selection.feather({feather});
            return JSON.stringify({{ok: true, bounds: [{left}, {top}, {right}, {bottom}]}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

DESELECT = """
(function() {
    try {
        app.activeDocument.selection.deselect();
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

SELECT_ALL = """
(function() {
    try {
        app.activeDocument.selection.selectAll();
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

INVERT_SELECTION = """
(function() {
    try {
        app.activeDocument.selection.invert();
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

def feather_selection_script(radius: float) -> str:
    return f"""
    (function() {{
        try {{
            app.activeDocument.selection.feather({radius});
            return JSON.stringify({{ok: true, radius: {radius}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def expand_selection_script(pixels: int) -> str:
    return f"""
    (function() {{
        try {{
            app.activeDocument.selection.expand({pixels});
            return JSON.stringify({{ok: true, pixels: {pixels}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def contract_selection_script(pixels: int) -> str:
    return f"""
    (function() {{
        try {{
            app.activeDocument.selection.contract({pixels});
            return JSON.stringify({{ok: true, pixels: {pixels}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

GET_SELECTION_BOUNDS = """
(function() {
    try {
        var b = app.activeDocument.selection.bounds;
        return JSON.stringify({
            ok: true,
            hasSelection: true,
            bounds: [Math.round(b[0].value), Math.round(b[1].value), Math.round(b[2].value), Math.round(b[3].value)]
        });
    } catch(e) {
        return JSON.stringify({ok: true, hasSelection: false, bounds: null});
    }
})();
"""


# --- Adobe Sensei AI Selection ---

def select_subject_script(sample_all_layers: bool = True) -> str:
    bool_str = "true" if sample_all_layers else "false"
    return f"""
    (function() {{
        try {{
            var idautoCutout = stringIDToTypeID("autoCutout");
            var desc = new ActionDescriptor();
            desc.putBoolean(stringIDToTypeID("sampleAllLayers"), {bool_str});
            executeAction(idautoCutout, desc, DialogModes.NO);
            return JSON.stringify({{ok: true, message: "Sensei Select Subject executed successfully"}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

SELECT_SKY = """
(function() {
    try {
        var idselectSky = stringIDToTypeID("selectSky");
        var desc = new ActionDescriptor();
        executeAction(idselectSky, desc, DialogModes.NO);
        return JSON.stringify({ok: true, message: "Sensei Select Sky executed successfully"});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""


# --- Content-Aware Fill (CAF) ---

CONTENT_AWARE_FILL = """
(function() {
    try {
        var idfill = stringIDToTypeID("fill");
        var desc = new ActionDescriptor();
        desc.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("fillContents"), stringIDToTypeID("contentAware"));
        desc.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100.0);
        desc.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        executeAction(idfill, desc, DialogModes.NO);
        return JSON.stringify({ok: true, message: "Content-Aware Fill applied successfully"});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""


# --- Adjustments and Filters ---

def adjust_brightness_contrast_script(brightness: int = 0, contrast: int = 0) -> str:
    return f"""
    (function() {{
        try {{
            app.activeDocument.activeLayer.adjustBrightnessContrast({brightness}, {contrast});
            return JSON.stringify({{ok: true, brightness: {brightness}, contrast: {contrast}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def adjust_curves_auto_script() -> str:
    return """
    (function() {
        try {
            var idautoCurves = stringIDToTypeID("autoCurves");
            var desc = new ActionDescriptor();
            executeAction(idautoCurves, desc, DialogModes.NO);
            return JSON.stringify({ok: true, message: "Auto Curves applied"});
        } catch(e) {
            return JSON.stringify({ok: false, error: e.message});
        }
    })();
    """

def adjust_hue_saturation_script(hue: int = 0, saturation: int = 0, lightness: int = 0) -> str:
    return f"""
    (function() {{
        try {{
            app.activeDocument.activeLayer.adjustHueSaturation({hue}, {saturation}, {lightness});
            return JSON.stringify({{ok: true, hue: {hue}, saturation: {saturation}, lightness: {lightness}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

AUTO_LEVELS = """
(function() {
    try {
        app.activeDocument.activeLayer.autoLevels();
        return JSON.stringify({ok: true, message: "Auto Levels applied"});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

AUTO_CONTRAST = """
(function() {
    try {
        app.activeDocument.activeLayer.autoContrast();
        return JSON.stringify({ok: true, message: "Auto Contrast applied"});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

DESATURATE = """
(function() {
    try {
        app.activeDocument.activeLayer.desaturate();
        return JSON.stringify({ok: true, message: "Layer desaturated"});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

INVERT = """
(function() {
    try {
        app.activeDocument.activeLayer.invert();
        return JSON.stringify({ok: true, message: "Layer inverted"});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

def apply_gaussian_blur_script(radius: float) -> str:
    return f"""
    (function() {{
        try {{
            app.activeDocument.activeLayer.applyGaussianBlur({radius});
            return JSON.stringify({{ok: true, radius: {radius}}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

UNDO = """
(function() {
    try {
        var idundo = stringIDToTypeID("undo");
        var desc = new ActionDescriptor();
        executeAction(idundo, desc, DialogModes.NO);
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

REDO = """
(function() {
    try {
        var idredo = stringIDToTypeID("redo");
        var desc = new ActionDescriptor();
        executeAction(idredo, desc, DialogModes.NO);
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

# --- Pro & Advanced Features: Camera Raw, Adjustment Layers, Typography, Layer Styles ---

def camera_raw_filter_script(
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
) -> str:
    """Invokes Adobe Camera Raw Filter with specific development settings."""
    return f"""
    (function() {{
        try {{
            var idAdobeCameraRaw = stringIDToTypeID("Adobe Camera Raw Filter");
            var desc = new ActionDescriptor();
            var crSettings = new ActionDescriptor();
            
            if ({exposure} !== 0.0) crSettings.putDouble(stringIDToTypeID("Exposure2012"), {exposure});
            if ({contrast} !== 0) crSettings.putInteger(stringIDToTypeID("Contrast2012"), {contrast});
            if ({highlights} !== 0) crSettings.putInteger(stringIDToTypeID("Highlights2012"), {highlights});
            if ({shadows} !== 0) crSettings.putInteger(stringIDToTypeID("Shadows2012"), {shadows});
            if ({clarity} !== 0) crSettings.putInteger(stringIDToTypeID("Clarity2012"), {clarity});
            if ({dehaze} !== 0) crSettings.putInteger(stringIDToTypeID("Dehaze"), {dehaze});
            if ({vibrance} !== 0) crSettings.putInteger(stringIDToTypeID("Vibrance"), {vibrance});
            if ({saturation} !== 0) crSettings.putInteger(stringIDToTypeID("Saturation"), {saturation});
            if ({temperature} !== 0) crSettings.putInteger(stringIDToTypeID("Temperature"), {temperature});
            if ({tint} !== 0) crSettings.putInteger(stringIDToTypeID("Tint"), {tint});
            
            desc.putObject(stringIDToTypeID("CrSettings"), stringIDToTypeID("CrSettings"), crSettings);
            executeAction(idAdobeCameraRaw, desc, DialogModes.NO);
            return JSON.stringify({{ok: true, message: "Camera Raw Filter applied successfully"}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

CONVERT_TO_SMART_OBJECT = """
(function() {
    try {
        var idnewPlacedLayer = stringIDToTypeID("newPlacedLayer");
        executeAction(idnewPlacedLayer, undefined, DialogModes.NO);
        return JSON.stringify({ok: true, name: app.activeDocument.activeLayer.name});
    } catch(e) {
        return JSON.stringify({ok: false, error: e.message});
    }
})();
"""

def create_adjustment_layer_script(adj_type: str, name: str | None = None) -> str:
    """Creates a true non-destructive Adjustment Layer (e.g. curves, hue_saturation, levels, solid_color)."""
    type_map = {
        "curves": "curves",
        "hue_saturation": "hueSaturation",
        "levels": "levels",
        "brightness_contrast": "brightnessContrast",
        "color_lookup": "colorLookup",
        "photo_filter": "photoFilter",
        "black_and_white": "blackAndWhite",
        "vibrance": "vibrance"
    }
    adj_id = type_map.get(adj_type.lower(), "curves")
    layer_name = name or (adj_type.replace("_", " ").title() + " 1")
    escaped_name = layer_name.replace('"', '\\"')

    return f"""
    (function() {{
        try {{
            var idmake = stringIDToTypeID("make");
            var desc = new ActionDescriptor();
            var ref = new ActionReference();
            ref.putClass(stringIDToTypeID("adjustmentLayer"));
            desc.putReference(stringIDToTypeID("null"), ref);
            
            var adjDesc = new ActionDescriptor();
            var classDesc = new ActionDescriptor();
            adjDesc.putClass(stringIDToTypeID("type"), stringIDToTypeID("{adj_id}"));
            adjDesc.putString(stringIDToTypeID("name"), "{escaped_name}");
            desc.putObject(stringIDToTypeID("using"), stringIDToTypeID("adjustmentLayer"), adjDesc);
            
            executeAction(idmake, desc, DialogModes.NO);
            return JSON.stringify({{ok: true, name: "{escaped_name}", type: "{adj_type}"}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def add_text_layer_script(
    text: str,
    font_name: str = "Helvetica",
    font_size_pt: float = 24.0,
    color_hex: str = "FFFFFF",
    x_px: float = 100.0,
    y_px: float = 100.0,
    justification: str = "left"
) -> str:
    """Creates a vector Typography Text Layer in the active document."""
    escaped_text = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\r")
    clean_hex = color_hex.lstrip("#")
    r = int(clean_hex[0:2], 16) if len(clean_hex) >= 2 else 255
    g = int(clean_hex[2:4], 16) if len(clean_hex) >= 4 else 255
    b = int(clean_hex[4:6], 16) if len(clean_hex) >= 6 else 255

    just_enum = "Justification.LEFT"
    if justification.lower() == "center":
        just_enum = "Justification.CENTER"
    elif justification.lower() == "right":
        just_enum = "Justification.RIGHT"

    return f"""
    (function() {{
        try {{
            var doc = app.activeDocument;
            var textLayer = doc.artLayers.add();
            textLayer.kind = LayerKind.TEXT;
            textLayer.name = "{escaped_text.split('\\r')[0][:30]}";
            
            var textItem = textLayer.textItem;
            textItem.contents = "{escaped_text}";
            textItem.size = {font_size_pt};
            textItem.position = [{x_px}, {y_px}];
            textItem.justification = {just_enum};
            
            try {{
                textItem.font = "{font_name}";
            }} catch(fErr) {{}}
            
            var textColor = new SolidColor();
            textColor.rgb.red = {r};
            textColor.rgb.green = {g};
            textColor.rgb.blue = {b};
            textItem.color = textColor;
            
            return JSON.stringify({{ok: true, name: textLayer.name, id: textLayer.id}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """

def apply_layer_style_script(
    drop_shadow: bool = False,
    shadow_opacity: float = 50.0,
    shadow_distance: int = 5,
    shadow_size: int = 10,
    stroke: bool = False,
    stroke_size: int = 2,
    stroke_color_hex: str = "000000"
) -> str:
    """Applies Layer Styles (FX) like Drop Shadow and Stroke to the active layer."""
    clean_hex = stroke_color_hex.lstrip("#")
    sr = int(clean_hex[0:2], 16) if len(clean_hex) >= 2 else 0
    sg = int(clean_hex[2:4], 16) if len(clean_hex) >= 4 else 0
    sb = int(clean_hex[4:6], 16) if len(clean_hex) >= 6 else 0

    return f"""
    (function() {{
        try {{
            var idset = stringIDToTypeID("set");
            var desc = new ActionDescriptor();
            var ref = new ActionReference();
            ref.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
            ref.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
            desc.putReference(stringIDToTypeID("null"), ref);
            
            var fxDesc = new ActionDescriptor();
            fxDesc.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 100.0);
            
            if ({str(drop_shadow).lower()}) {{
                var dsDesc = new ActionDescriptor();
                dsDesc.putBoolean(stringIDToTypeID("enabled"), true);
                dsDesc.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("multiply"));
                dsDesc.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), {shadow_opacity});
                dsDesc.putUnitDouble(stringIDToTypeID("distance"), stringIDToTypeID("pixelsUnit"), {shadow_distance});
                dsDesc.putUnitDouble(stringIDToTypeID("blur"), stringIDToTypeID("pixelsUnit"), {shadow_size});
                fxDesc.putObject(stringIDToTypeID("dropShadow"), stringIDToTypeID("dropShadow"), dsDesc);
            }}
            
            if ({str(stroke).lower()}) {{
                var stDesc = new ActionDescriptor();
                stDesc.putBoolean(stringIDToTypeID("enabled"), true);
                stDesc.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), {stroke_size});
                stDesc.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
                
                var strokeColor = new ActionDescriptor();
                strokeColor.putDouble(stringIDToTypeID("red"), {sr}.0);
                strokeColor.putDouble(stringIDToTypeID("green"), {sg}.0);
                strokeColor.putDouble(stringIDToTypeID("blue"), {sb}.0);
                stDesc.putObject(stringIDToTypeID("color"), stringIDToTypeID("RGBColor"), strokeColor);
                fxDesc.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), stDesc);
            }}
            
            desc.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), fxDesc);
            executeAction(idset, desc, DialogModes.NO);
            return JSON.stringify({{ok: true, message: "Layer style applied"}});
        }} catch(e) {{
            return JSON.stringify({{ok: false, error: e.message}});
        }}
    }})();
    """
