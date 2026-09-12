"""Image and color analysis engine using Pillow."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from PIL import Image, ImageStat


class VisionAnalyzer:
    @staticmethod
    def analyze_image(image_path: str) -> Dict[str, Any]:
        """Analyzes an image file for dimensions, tone, luminance, and dominant color temperature."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        with Image.open(image_path) as img:
            width, height = img.size
            mode = img.mode
            format_name = img.format

            # Convert to RGB for photometric analysis
            rgb_img = img.convert("RGB")
            stat = ImageStat.Stat(rgb_img)

            # Means per channel: [R, G, B]
            r_mean, g_mean, b_mean = stat.mean[:3]
            # Perceived luminance (ITU-R BT.709)
            luminance = 0.2126 * r_mean + 0.7152 * g_mean + 0.0722 * b_mean
            # Warmth ratio: (Red - Blue) / 255.0 (-1.0 to +1.0)
            warmth = (r_mean - b_mean) / 255.0

            # RMS contrast per channel
            r_rms, g_rms, b_rms = stat.rms[:3]

            mood = "neutral"
            if warmth > 0.1:
                mood = "warm"
            elif warmth < -0.1:
                mood = "cool"

            return {
                "path": image_path,
                "format": format_name,
                "mode": mode,
                "width": width,
                "height": height,
                "aspectRatio": round(width / height, 3),
                "luminance": round(luminance, 1),
                "warmthScore": round(warmth, 3),
                "mood": mood,
                "channelMeans": {
                    "red": round(r_mean, 1),
                    "green": round(g_mean, 1),
                    "blue": round(b_mean, 1)
                }
            }


analyzer = VisionAnalyzer()
