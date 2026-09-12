---
name: photoshop-mcp-elite
description: Control and automate Adobe Photoshop via the Photoshop MCP Elite server with professional photographic intelligence, realistic visual harmonization, autonomous Adobe Firefly Generative AI inpainting, Camera Raw grading, Smart Objects, typography design, and color theory. Use when the user asks to edit photos, retouch portraits, remove distractions, replace sky, match lighting, grade color, add text/posters, or composite elements.
---

# Photoshop MCP Elite & Photographic Intelligence Guide

Use the connected `photoshop` MCP server (`photoshop-mcp-elite`) to interact directly with Adobe Photoshop on macOS. Follow professional editorial, Hollywood compositing, and graphic design standards.

---

## 1. Core Visual Analysis (วิเคราะห์ก่อนลงมือ)

Before executing any edits (especially Sky Replacement, Color Grading, or Inpainting), analyze the source image:

1. **Light Quality & Direction**:
   - Is the source image taken in **Direct Sunlight** (sharp shadows, high contrast) or **Overcast / Diffuse Light** (soft shadows, muted highlights)?
   - If the original is diffuse/overcast, putting in a harsh, deeply saturated sunny sky will immediately look fake unless the foreground is relit.
2. **Color Temperature & Ambient Cast**:
   - Check the Kelvin/tint of the foreground subject and environment.
   - Any new background must match or be harmonized with this ambient temperature.
3. **Horizon & Atmospheric Depth**:
   - Real skies have **Atmospheric Haze** near the horizon (lower saturation, higher brightness/haze). Pure deep blue reaching all the way to the ground destroys depth perception.

---

## 2. Professional Color Grading & Camera Raw Rules (กฎการเกรดสีระดับสตูดิโอ)

Instead of flat, destructive Brightness/Contrast tweaks, use Adobe Camera Raw Filter and True Adjustment Layers:

1. **Convert to Smart Object First**:
   - Always call `photoshop_convert_to_smart_object()` before applying `photoshop_apply_camera_raw_filter()`.
   - This ensures the Camera Raw adjustments become a **Smart Filter**, allowing parameters to be re-adjusted without degrading pixels.
2. **Atmospheric Dehaze & Clarity**:
   - Use `dehaze` (+5 to +15) to cut through background mist or restore contrast in washed-out skies.
   - Use `clarity` (+10 to +25) to pop midtone textures on architectural stone, foliage, or clothing, but keep it low on portraits.
3. **Color Temperature Harmonization**:
   - Adjust `temperature` (+ warm / - cool) and `tint` (+ magenta / - green) to unify the mood.
   - Use `vibrance` instead of `saturation` to boost muted colors while protecting natural skin tones.

---

## 3. Realistic Sky Replacement Rules (กฎการเปลี่ยนท้องฟ้าให้สมจริง)

1. **Atmospheric Haze Calibration**:
   - Add a soft linear/radial gradient of atmospheric haze (light cyan/white with low opacity) near the horizon where the sky meets buildings or terrain.
2. **Foreground Relighting & Color Harmonization**:
   - When replacing an overcast sky with a vibrant or sunny sky, you **MUST** apply an adjustment layer (Curves or Photo Filter - Warming/Cooling) to the foreground/subject.
   - Warm up the highlights slightly if adding sunlight.
   - Adjust the contrast of the foreground to match the dynamic range of the new background.
3. **Light Wrap / Edge Bleeding**:
   - Bright sky naturally bleeds slightly over the edges of dark silhouettes (such as tree branches, roof edges, or architectural latticework).
   - Use soft mask feathering or a subtle inner glow / screen blend mode to allow the ambient sky light to wrap around edges.
4. **Global Unified Color Grade**:
   - Always place a subtle Curves or Levels adjustment layer on top of **ALL** layers to unify blacks, midtones, and highlights across the composite.

---

## 4. High-Quality Inpainting & Distraction Removal Rules (กฎการลบคนและสิ่งแปลกปลอม)

1. **Never Use Naive Content-Aware Fill on Complex Architecture**:
   - Standard Content-Aware Fill uses simple patch-match texture synthesis. It blurs straight perspective lines, distorts balustrades/ledges, and leaves obvious duplicate smudges.
2. **Prioritize Generative AI (Firefly Inpainting)**:
   - For people standing against complex backgrounds (stone walls, railings, streets, steps), use Autonomous Generative Fill (`photoshop_generative_fill_ai` or `photoshop_generative_remove_ai`) with a contextually accurate prompt (e.g., "empty stone terrace wall, straight clean balustrade").
   - Generative AI understands vanishing points, architectural symmetry, and lighting shadows.
3. **Targeted Surgical Selections**:
   - Select tightly around the distraction (5-10px padding). Do not select large rectangular swathes that swallow existing clean structures.
   - Always apply feathering (`2.0` to `3.0` px) to blend the generative boundary seamlessly.

---

## 5. Typography, Posters & Layout Design Rules (กฎการออกแบบตัวอักษรและแบนเนอร์)

When asked to create marketing graphics, posters, thumbnails, or banners:

1. **Hierarchy & Font Sizing**:
   - Main Heading / Hook: 48–72 pt bold.
   - Subtitle / Supporting text: 24–36 pt regular.
   - Call-to-Action / Details: 14–18 pt medium.
2. **Readability with Layer Styles (FX)**:
   - Never place raw text directly over busy photos without contrast separation.
   - Apply `photoshop_apply_layer_style()`:
     - **Drop Shadow**: Opacity 40–60%, Distance 4–8px, Size 8–16px (blends text against bright/uneven backgrounds).
     - **Stroke**: 2–4px solid contrasting color (e.g. black stroke on white text).
3. **Positioning & Alignment**:
   - Use `justification` ("center", "left", "right") consistently.
   - Maintain safe margins (at least 50px away from canvas edges).

---

## 6. Complete Tool Mapping & Recipe Catalog (47 Tools)

### Autonomous Multi-Step Workflows
* `photoshop_harmonize_sky`: Sensei sky selection + replacement + horizon atmospheric haze + foreground ambient light warming.
* `photoshop_generative_fill_ai`: Autonomously trigger Adobe Firefly on the current selection with an optional prompt (macOS Accessibility automation).
* `photoshop_generative_remove_ai`: Autonomously remove multiple bounding-box regions using Firefly AI.
* `photoshop_smart_remove_distractions`: Multi-region precision removal with expansion + feathering on a non-destructive Retouch layer.
* `photoshop_match_lighting_and_tone`: Photo-wide color balance and dynamic range adjustment.

### Pro Studio & Non-Destructive Tools
* `photoshop_apply_camera_raw_filter`: Studio RAW controls (exposure, contrast, highlights, shadows, clarity, dehaze, vibrance, saturation, temperature, tint).
* `photoshop_convert_to_smart_object`: Wraps active or selected layers into a Smart Object.
* `photoshop_create_adjustment_layer`: Creates true non-destructive Adjustment Layers (`curves`, `hue_saturation`, `levels`, `brightness_contrast`, `vibrance`, `black_and_white`).
* `photoshop_add_text_layer`: Creates vector Typography text layers with custom font, size, hex color, coordinates, and alignment.
* `photoshop_apply_layer_style`: Applies layer effects (FX) including Drop Shadow and Stroke.

### Adobe Sensei AI & Selection Suite
* `photoshop_select_sky`: Adobe Sensei AI sky contour isolation.
* `photoshop_select_subject`: Adobe Sensei AI subject auto-cutout.
* `photoshop_select_rectangle`, `photoshop_select_ellipse`, `photoshop_select_all`, `photoshop_deselect`, `photoshop_invert_selection`.
* `photoshop_feather_selection`, `photoshop_expand_selection`, `photoshop_contract_selection`.
* `photoshop_get_selection_bounds`.

### Document & Layer Management
* `photoshop_get_document_info`, `photoshop_list_documents`, `photoshop_open_image`, `photoshop_save_document`, `photoshop_export_as`.
* `photoshop_get_layers`, `photoshop_create_layer`, `photoshop_select_layer_by_name`, `photoshop_duplicate_layer`, `photoshop_delete_layer`.
* `photoshop_set_layer_visibility`, `photoshop_set_layer_opacity`, `photoshop_merge_visible_layers`, `photoshop_flatten_image`.

### Adjustments & Filters
* `photoshop_adjust_brightness_contrast`, `photoshop_adjust_curves_auto`, `photoshop_adjust_hue_saturation`.
* `photoshop_auto_levels`, `photoshop_auto_contrast`, `photoshop_desaturate`, `photoshop_invert`, `photoshop_apply_gaussian_blur`.

### Custom ExtendScript
* `photoshop_execute_custom_jsx`: Direct raw ES3 ExtendScript execution with built-in JSON serialization.

---

## 7. Non-Destructive Workflow Gate (กฎเหล็กส่งงาน)

1. **Preserve Master Pixels**: Never overwrite or delete the original `Background` layer.
2. **Dedicated Labeled Layers**: Retouching, sky replacement, text, and grading must reside on explicitly named layers (`Smart Retouch`, `Sky Composite`, `Camera Raw Grade`, `Hero Typography`).
3. **Visual Verification**: Before finishing, always export a preview using `photoshop_export_as(file_path, "jpg", 90)` to verify overall visual harmony and composition.
