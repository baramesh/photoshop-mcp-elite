from unittest.mock import MagicMock

import pytest

from core.bridge import PhotoshopBridge


@pytest.fixture
def mock_bridge(monkeypatch):
    """Fixture to mock PhotoshopBridge execution without needing live Photoshop."""
    mock = MagicMock(spec=PhotoshopBridge)
    monkeypatch.setattr("tools.document.bridge", mock)
    monkeypatch.setattr("tools.layer.bridge", mock)
    monkeypatch.setattr("tools.selection.bridge", mock)
    monkeypatch.setattr("tools.adjustment.bridge", mock)
    monkeypatch.setattr("tools.workflows.bridge", mock)
    return mock
