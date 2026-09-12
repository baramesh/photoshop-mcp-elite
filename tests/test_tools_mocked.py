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
