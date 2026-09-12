# Golden Example 2: Social Media Marketing Banner & Poster Design

## Scenario
The user has a product or campaign hero shot and requests:
> *"ช่วยทำแบนเนอร์โปรโมชั่น Summer Sale ใส่ข้อความลดสูงสุด 50% ให้ดูพรีเมียมและอ่านง่าย"*

---

## Retoucher's Mental Model (ลำดับการคิดเชิงศิลป์)
1. **Visual Hierarchy**:
   - Primary Headline ("SUMMER SALE"): 64–72 pt, bold, high contrast.
   - Secondary Benefit ("UP TO 50% OFF"): 32–36 pt, colored accent.
   - Call-to-Action ("SHOP NOW"): 16–20 pt.
2. **Text Legibility Guarantee**: Never place raw colored text directly over photographic backgrounds without contrast protection. Always apply **Layer Styles (`photoshop_apply_layer_style`)** with a subtle Drop Shadow and/or Outset Stroke.
3. **Product Emphasis**: Use a non-destructive Adjustment Layer (`curves` or `levels`) under the text to slightly vignette or darken background distractions.

---

## Tool Execution Sequence

### Step 1: Background Contrast Calibration
```json
// Tool: photoshop_create_adjustment_layer
{
  "adj_type": "curves",
  "name": "Background Tone Control"
}
```

### Step 2: Create Hero Typography Layer
```json
// Tool: photoshop_add_text_layer
{
  "text": "SUMMER SALE 2026",
  "font_name": "Helvetica-Bold",
  "font_size_pt": 64.0,
  "color_hex": "FFFFFF",
  "x_px": 200.0,
  "y_px": 350.0,
  "justification": "left"
}
```

### Step 3: Apply Professional Layer FX (Drop Shadow & Stroke)
```json
// Tool: photoshop_apply_layer_style
{
  "drop_shadow": true,
  "shadow_opacity": 55.0,
  "shadow_distance": 8,
  "shadow_size": 16,
  "stroke": true,
  "stroke_size": 2,
  "stroke_color_hex": "1A1A1A"
}
```
*Effect: The typography pops off the image with cinematic depth and guaranteed readability across any backdrop.*

### Step 4: Subtitle Text Layer
```json
// Tool: photoshop_add_text_layer
{
  "text": "UP TO 50% OFF • LIMITED TIME ONLY",
  "font_name": "Helvetica",
  "font_size_pt": 28.0,
  "color_hex": "FFD700",
  "x_px": 200.0,
  "y_px": 440.0,
  "justification": "left"
}
```

### Step 5: Final Export
```json
// Tool: photoshop_export_as
{
  "file_path": "/path/to/summer_banner_ready.png",
  "format_type": "png"
}
```
