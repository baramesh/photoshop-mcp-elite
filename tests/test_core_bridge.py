from unittest.mock import MagicMock, patch

import pytest

from core import jsx_templates
from core.bridge import JSON2_POLYFILL, PhotoshopBridge


def test_json2_polyfill_content():
    assert "stringify: function" in JSON2_POLYFILL
    assert "parse: function" in JSON2_POLYFILL


def test_jsx_templates_generation():
    doc_script = jsx_templates.GET_DOCUMENT_INFO
    assert "activeDocument" in doc_script
    assert "JSON.stringify" in doc_script

    select_rect_script = jsx_templates.select_rectangle_script(10, 20, 100, 200, 2.0)
    assert "doc.selection.select" in select_rect_script
    assert "10" in select_rect_script
    assert "200" in select_rect_script

    curves_script = jsx_templates.adjust_curves_auto_script()
    assert "autoCutout" not in curves_script
    assert "Curves" in curves_script or "Crvs" in curves_script


@patch("subprocess.run")
def test_bridge_execute_jsx_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout='{"ok": true, "layers": 3}', stderr="")
    b = PhotoshopBridge()
    res = b.execute_jsx("return JSON.stringify({ok: true, layers: 3});")

    assert res == {"ok": True, "layers": 3}
    assert mock_run.called


@patch("subprocess.run")
def test_bridge_execute_jsx_error(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Execution error -1708")
    b = PhotoshopBridge()
    with pytest.raises(RuntimeError) as exc_info:
        b.execute_jsx("invalid code;")
    assert "Photoshop execution failed" in str(exc_info.value)
