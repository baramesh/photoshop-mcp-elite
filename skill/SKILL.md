---
name: photoshop-mcp-elite
description: Control and automate Adobe Photoshop via the Photoshop MCP Elite server with professional photographic intelligence, realistic visual harmonization, autonomous Adobe Firefly Generative AI inpainting, and color theory. Use when the user asks to edit photos, retouch portraits, remove distractions, replace sky, match lighting, or composite elements.
---

# Photoshop MCP Elite & Photographic Intelligence Guide

Use the connected `photoshop` MCP server (`photoshop-mcp-elite`) to interact directly with Adobe Photoshop. Follow professional digital compositing and retouching standards.

---

## 1. Core Visual Analysis (วิเคราะห์ก่อนลงมือ)

Before executing any edits (especially Sky Replacement or Inpainting), analyze the source image:

1. **Light Quality & Direction**:
   - Is the source image taken in **Direct Sunlight** (sharp shadows, high contrast) or **Overcast / Diffuse Light** (soft shadows, muted highlights)?
   - If the original is diffuse/overcast, putting in a harsh, deeply saturated sunny sky will immediately look fake unless the foreground is relit.
2. **Color Temperature & Ambient Cast**:
   - Check the Kelvin/tint of the foreground subject and environment.
   - Any new background must match or be harmonized with this ambient temperature.
3. **Horizon & Atmospheric Depth**:
   - Real skies have **Atmospheric Haze** near the horizon (lower saturation, higher brightness/haze). Pure deep blue reaching all the way to the ground destroys depth perception.

---

## 2. Realistic Sky Replacement Rules (กฎการเปลี่ยนท้องฟ้าให้สมจริง)

1. **Atmospheric Haze Calibration**:
   - Add a soft linear/radial gradient of atmospheric haze (light cyan/white with low opacity) near the horizon where the sky meets buildings or terrain.
2. **Foreground Relighting & Color Harmonization**:
   - When replacing an overcast sky with a vibrant or sunny sky, you **MUST** apply an adjustment layer (Curves or Photo Filter - Warming/Cooling) to the foreground/subject.
   - Warm up the highlights slightly if adding sunlight.
   - Adjust the contrast of the foreground to match the dynamic range of the new background.
3. **Light Wrap / Edge Bleeding**:
   - Bright sky naturally bleeds slightly over the edges of dark silhouettes (such as tree branches, roof edges, or the iron latticework of buildings).
   - Use soft mask feathering or a subtle inner glow / screen blend mode to allow the ambient sky light to wrap around edges.
4. **Global Unified Color Grade**:
   - Always place a subtle Curves or Levels adjustment on top of **ALL** layers to unify blacks, midtones, and highlights across the composite.

---

## 3. High-Quality Inpainting & Distraction Removal Rules (กฎการลบคนและสิ่งแปลกปลอม)

1. **Never Use Naive Content-Aware Fill on Complex Architecture**:
   - Standard Content-Aware Fill uses simple patch-match texture synthesis. It blurs straight perspective lines, distorts balustrades/ledges, and leaves obvious duplicate smudges.
2. **Prioritize Generative AI (Firefly Inpainting)**:
   - For people standing against complex backgrounds (stone walls, railings, streets, steps), use Autonomous Generative Fill (`photoshop_generative_fill_ai` or `photoshop_generative_remove_ai`) with a contextually accurate prompt (e.g., "empty stone terrace wall, straight clean balustrade").
   - Generative AI understands vanishing points, architectural symmetry, and lighting shadows.
3. **Targeted Surgical Selections**:
   - Select tightly around the distraction (5-10px padding). Do not select large rectangular swathes that swallow existing clean structures.
   - Always apply feathering (`2.0` to `3.0` px) to blend the generative boundary seamlessly.

---

## 4. Operating Reference & Tool Mapping

### Autonomous Workflows
- **Sky Harmonization**: `photoshop_harmonize_sky` (Sensei contour isolation + horizon haze + foreground ambient light warming).
- **Autonomous Firefly Inpainting**: `photoshop_generative_fill_ai` (GUI-automated Generative Fill), `photoshop_generative_remove_ai` (multi-bounding-box removal).
- **Distraction Removal**: `photoshop_smart_remove_distractions` (multi-region precision removal on a non-destructive Retouch layer).
- **Lighting & Tone Match**: `photoshop_match_lighting_and_tone` (photo-wide color balance and dynamic range adjustment).

### AI Selections
- **Sky Mask**: `photoshop_select_sky`
- **Subject Cutout**: `photoshop_select_subject`

### Pro & Non-Destructive Tools
- **Camera Raw Grading**: `photoshop_apply_camera_raw_filter` (Pro exposure, clarity, dehaze, temperature, vibrance).
- **True Adjustment Layers**: `photoshop_create_adjustment_layer` (curves, hue_saturation, levels, brightness_contrast, vibrance).
- **Smart Objects**: `photoshop_convert_to_smart_object`.
- **Typography & Vector Text**: `photoshop_add_text_layer`.
- **Layer Styles (FX)**: `photoshop_apply_layer_style` (drop_shadow, stroke).

### Adjustments & Filters
- `photoshop_adjust_brightness_contrast`, `photoshop_adjust_curves_auto`, `photoshop_adjust_hue_saturation`, `photoshop_apply_gaussian_blur`, `photoshop_auto_levels`, `photoshop_auto_contrast`.

### Non-Destructive Workflow Gate
- Maintain the original `Background` intact.
- Keep sky replacements and inpaintings on dedicated, labeled layers (`Sky Composite`, `Retouched Wall`, `Global Harmonization`).
- Always inspect output with `photoshop_export_as` before confirming completion.
