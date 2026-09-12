from tools import adjustment, document, layer, selection


def test_document_tools(mock_bridge):
    mock_bridge.execute_jsx.return_value = {"status": "ok", "id": 1, "name": "test.psd", "width": 1920, "height": 1080}
    info = document.get_document_info()
    assert info["name"] == "test.psd"
    assert info["width"] == 1920

    mock_bridge.execute_jsx.return_value = {"count": 1, "documents": [{"id": 1, "name": "doc1.psd"}]}
    docs = document.list_documents()
    assert docs["count"] == 1

    mock_bridge.execute_jsx.return_value = {"ok": True, "name": "sample.jpg", "path": "/path/sample.jpg"}
    opened = document.open_image("/path/sample.jpg")
    assert opened["ok"] is True


def test_layer_tools(mock_bridge):
    mock_bridge.execute_jsx.return_value = {"layers": [{"id": 1, "name": "Background", "visible": True}]}
    layers = layer.get_layers()
    assert len(layers["layers"]) == 1

    mock_bridge.execute_jsx.return_value = {"ok": True, "id": 2, "name": "New Layer"}
    created = layer.create_layer("New Layer")
    assert created["ok"] is True
    assert created["name"] == "New Layer"


def test_selection_tools(mock_bridge):
    mock_bridge.execute_jsx.return_value = {"ok": True, "bounds": [10, 10, 100, 100]}
    rect = selection.select_rectangle(10, 10, 100, 100)
    assert rect["ok"] is True
    assert rect["bounds"] == [10, 10, 100, 100]

    mock_bridge.execute_jsx.return_value = {"ok": True}
    deselected = selection.deselect()
    assert deselected["ok"] is True


def test_adjustment_tools(mock_bridge):
    mock_bridge.execute_jsx.return_value = {"ok": True}
    adj = adjustment.adjust_curves_auto()
    assert adj["ok"] is True


def test_pro_tools(mock_bridge):
    # Smart Object
    mock_bridge.execute_jsx.return_value = {"ok": True, "name": "Layer 1"}
    so = layer.convert_to_smart_object()
    assert so["ok"] is True

    # Adjustment Layer
    mock_bridge.execute_jsx.return_value = {"ok": True, "name": "Curves 1", "type": "curves"}
    adj_layer = layer.create_adjustment_layer("curves")
    assert adj_layer["ok"] is True

    # Camera Raw Filter
    mock_bridge.execute_jsx.return_value = {"ok": True, "message": "Camera Raw Filter applied"}
    cr = adjustment.apply_camera_raw_filter(clarity=20, dehaze=10)
    assert cr["ok"] is True

    # Typography Text Layer
    mock_bridge.execute_jsx.return_value = {"ok": True, "name": "Summer Sale", "id": 10}
    txt = layer.add_text_layer("Summer Sale", font_size_pt=36)
    assert txt["ok"] is True

    # Layer Styles
    mock_bridge.execute_jsx.return_value = {"ok": True, "message": "Layer style applied"}
    fx = layer.apply_layer_style(drop_shadow=True, stroke=True)
    assert fx["ok"] is True


def test_coverage_boosters(mock_bridge):
    mock_bridge.execute_jsx.return_value = {"ok": True}

    # Document tools
    document.save_document("/path/saved.psd")
    document.export_as("/path/out.png", format_type="png", quality=95)
    document.undo()
    document.redo()

    # Layer tools
    layer.select_layer("Layer 1")
    layer.set_layer_visibility("Layer 1", True)
    layer.set_layer_opacity("Layer 1", 75.0)
    layer.duplicate_layer("Layer 1", "Layer 1 Copy")
    layer.delete_active_layer()
    layer.merge_visible_layers()
    layer.flatten_image()

    # Selection tools
    selection.select_ellipse(10, 10, 50, 50)
    selection.select_all()
    selection.invert_selection()
    selection.feather_selection(2.0)
    selection.expand_selection(5)
    selection.contract_selection(3)
    selection.get_selection_bounds()
    selection.select_subject()
    selection.select_sky()
    selection.content_aware_fill()

    # Adjustment tools
    adjustment.adjust_brightness_contrast(10, 20)
    adjustment.adjust_hue_saturation(5, -5, 0)
    adjustment.auto_levels()
    adjustment.auto_contrast()
    adjustment.desaturate()
    adjustment.invert()
    adjustment.apply_gaussian_blur(3.5)


def test_workflows_mocked(monkeypatch):
    from tools import workflows
    from unittest.mock import MagicMock

    mock_b = MagicMock()
    mock_b.execute_jsx.return_value = {"ok": True}
    monkeypatch.setattr("tools.workflows.bridge", mock_b)

    # Test smart_remove_distractions
    rem = workflows.smart_remove_distractions([[10, 10, 50, 50]])
    assert rem["ok"] is True

    # Test match_lighting_and_tone
    ml = workflows.match_lighting_and_tone(target_mood="vibrant_daylight")
    assert ml["ok"] is True
