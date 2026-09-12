import pytest
from PIL import Image

from core.vision import analyzer


def test_analyze_image_not_found():
    with pytest.raises(FileNotFoundError):
        analyzer.analyze_image("/non/existent/path/image.jpg")


def test_analyze_image_warm_palette(tmp_path):
    # Create a warm image (high red, low blue)
    img_path = str(tmp_path / "warm_test.png")
    img = Image.new("RGB", (200, 100), color=(255, 100, 20))
    img.save(img_path, format="PNG")

    info = analyzer.analyze_image(img_path)
    assert info["path"] == img_path
    assert info["width"] == 200
    assert info["height"] == 100
    assert info["aspectRatio"] == 2.0
    assert info["format"] == "PNG"
    assert info["mood"] == "warm"
    assert info["warmthScore"] > 0.1
    assert info["channelMeans"]["red"] == 255.0
    assert info["channelMeans"]["blue"] == 20.0


def test_analyze_image_cool_palette(tmp_path):
    # Create a cool image (low red, high blue)
    img_path = str(tmp_path / "cool_test.png")
    img = Image.new("RGB", (100, 100), color=(20, 100, 255))
    img.save(img_path, format="PNG")

    info = analyzer.analyze_image(img_path)
    assert info["mood"] == "cool"
    assert info["warmthScore"] < -0.1
