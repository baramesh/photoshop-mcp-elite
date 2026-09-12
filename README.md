# Photoshop MCP Elite (`photoshop-mcp-elite`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-2.0-orange.svg)](https://modelcontextprotocol.io/)

A high-performance, native Python **Model Context Protocol (MCP)** server for **Adobe Photoshop** on macOS.

Unlike legacy Node.js wrappers that rely on outdated 2010 PatchMatch algorithms and crash on ExtendScript ES3 syntax mismatches, `photoshop-mcp-elite` delivers:
* **True Adobe Firefly Generative AI Automation**: Autonomously triggers Generative Fill and AI object removal via macOS accessibility bridges.
* **Intelligent Photographic Workflows**: Includes automated Sky Replacement with atmospheric horizon haze and foreground relighting, precision distraction removal, and color harmony adjustments.
* **Bulletproof ES3 Engine**: Embedded JSON2 polyfill and isolated ActionManager execution that completely prevents `JSON is undefined` and quote-escaping errors.
* **Fast & Lightweight**: Built on the official Python MCP SDK with sub-second execution speeds (0.1–0.3s).

---

## 🌟 Key Features

| Category | Features |
| :--- | :--- |
| **Generative AI** | Autonomous Adobe Firefly Generative Fill (`photoshop_generative_fill_ai`, `photoshop_generative_remove_ai`) with zero human clicks required. |
| **Photographic Workflows** | `photoshop_harmonize_sky` (Sensei contour isolation + horizon haze + foreground warming), `photoshop_smart_remove_distractions`, `photoshop_match_lighting_and_tone`. |
| **Adobe Sensei AI** | One-shot AI `selectSky` and `selectSubject` (autoCutout). |
| **Full Layer Suite** | Non-destructive layer management, visibility, opacity, blend modes, duplication, merge, and flatten. |
| **Precision Selection** | Rectangular, elliptical, feathering, boundary expansion/contraction, inversion, and bounds inspection. |
| **Adjustments** | Curves (auto/points), Levels, Brightness/Contrast, Hue/Saturation, Desaturate, Invert, Gaussian Blur. |
| **Document Management** | Info query, document list, open image, save, and high-fidelity export as JPEG/PNG. |

---

## 🚀 Quickstart

### Prerequisites
* macOS with Adobe Photoshop (Photoshop 2024, 2025, or 2026 recommended)
* [uv](https://docs.astral.sh/uv/) (recommended) or Python 3.12+

### 1. Clone the Repository
```bash
git clone https://github.com/baramesh/photoshop-mcp-elite.git
cd photoshop-mcp-elite
```

### 2. Install Dependencies
Using `uv`:
```bash
uv sync
```

### 3. Grant Accessibility Permissions (For Autonomous Generative AI)
To allow the server to autonomously trigger Adobe Firefly without requiring manual clicks on the Contextual Task Bar:
1. Open **System Settings** on macOS.
2. Navigate to **Privacy & Security** > **Accessibility**.
3. Toggle **ON** for your terminal or MCP host app (e.g., Terminal, iTerm2, Claude Desktop, Cursor, or Antigravity).

---

## 🧠 AI Agent Skill (`SKILL.md`)

This repository includes a ready-to-use Agent Skill in `skill/SKILL.md` for AI coding assistants and autonomous agents (e.g., Antigravity, Claude Code, Cursor):

* **Photographic Intelligence**: Guides agents on how to assess lighting direction, color temperature, and atmospheric horizon haze before editing.
* **Firefly & Inpainting Rules**: Instructs agents when to avoid naive Content-Aware Fill and how to use autonomous Generative Fill with surgical selections.
* **Non-Destructive Standard**: Enforces layer labeling and non-destructive retouching practices.

To install the skill in your local Antigravity / Agent configuration:
```bash
mkdir -p ~/.gemini/config/skills/photoshop-mcp-elite
cp skill/SKILL.md ~/.gemini/config/skills/photoshop-mcp-elite/
```

---

## ⚙️ MCP Configuration

Add `photoshop` to your client configuration:

### Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "photoshop": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/path/to/photoshop-mcp-elite",
        "python",
        "server.py"
      ]
    }
  }
}
```

### Cursor / Windsurf / Antigravity (`mcp_config.json`)
```json
{
  "mcpServers": {
    "photoshop": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/path/to/photoshop-mcp-elite",
        "python",
        "server.py"
      ]
    }
  }
}
```

---

## 🛠️ Tool Catalog (47 Tools)

### Generative AI & Smart Workflows
* `photoshop_generative_fill_ai`: Autonomously trigger Adobe Firefly on the current selection with an optional prompt.
* `photoshop_generative_remove_ai`: Autonomously remove multiple bounding-box regions using Firefly AI.
* `photoshop_harmonize_sky`: Sensei sky selection + replacement + horizon atmospheric haze + foreground ambient light matching.
* `photoshop_smart_remove_distractions`: Multi-region precision removal with expansion + feathering on a non-destructive Retouch layer.
* `photoshop_match_lighting_and_tone`: Photo-wide color harmony and contrast adjustment.

### Pro Hollywood & Design Capabilities (New 🚀)
* `photoshop_apply_camera_raw_filter`: Direct Adobe Camera Raw engine controls (Exposure, Contrast, Highlights, Shadows, Clarity, Dehaze, Vibrance, Saturation, Temperature, Tint).
* `photoshop_create_adjustment_layer`: Creates true non-destructive Adjustment Layers (`curves`, `hue_saturation`, `levels`, `brightness_contrast`, `vibrance`, `black_and_white`).
* `photoshop_convert_to_smart_object`: Wraps active or selected layers into a Smart Object for non-destructive filter stacks.
* `photoshop_add_text_layer`: Creates vector Typography text layers with custom fonts, point size, hex colors, and alignment.
* `photoshop_apply_layer_style`: Applies layer effects (FX) including Drop Shadow (opacity, distance, blur) and Stroke (color, size).

### Sensei AI & Selections
* `photoshop_select_sky`: Adobe Sensei AI sky contour isolation.
* `photoshop_select_subject`: Adobe Sensei AI subject auto-cutout.
* `photoshop_select_rectangle`, `photoshop_select_ellipse`, `photoshop_select_all`, `photoshop_deselect`, `photoshop_invert_selection`.
* `photoshop_feather_selection`, `photoshop_expand_selection`, `photoshop_contract_selection`.
* `photoshop_get_selection_bounds`.

### Document & Layers
* `photoshop_get_document_info`, `photoshop_list_documents`, `photoshop_open_image`, `photoshop_save_document`, `photoshop_export_as`.
* `photoshop_get_layers`, `photoshop_create_layer`, `photoshop_select_layer_by_name`, `photoshop_duplicate_layer`, `photoshop_delete_layer`.
* `photoshop_set_layer_visibility`, `photoshop_set_layer_opacity`, `photoshop_merge_visible_layers`, `photoshop_flatten_image`.

### Adjustments & Filters
* `photoshop_adjust_brightness_contrast`, `photoshop_adjust_curves_auto`, `photoshop_adjust_hue_saturation`.
* `photoshop_auto_levels`, `photoshop_auto_contrast`, `photoshop_desaturate`, `photoshop_invert`, `photoshop_apply_gaussian_blur`.

### Custom ExtendScript
* `photoshop_execute_custom_jsx`: Direct raw ES3 ExtendScript execution with built-in JSON serialization.

---

## 🏛️ Architecture

```
AI Client (Claude / Cursor / Antigravity)
               │ (MCP JSON-RPC over stdio)
               ▼
   photoshop-mcp-elite (Python 3.12 / FastMCP)
        ├── core/bridge.py        (AppleScript / JSX Execution Engine)
        ├── core/vision.py        (Pillow / Luminance & Warmth Analyzer)
        ├── tools/workflows.py    (Autonomous Firefly & Sky Harmonization)
        └── tools/*.py            (Document, Layer, Selection, Adjustment)
               │
               ▼ AppleScript (osascript) & System Events
      Adobe Photoshop 2026 Core Engine
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
