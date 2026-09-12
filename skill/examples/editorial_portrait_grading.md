# Golden Example 3: Studio & Editorial Portrait Color Grading

## Scenario
The user opens a RAW or high-res portrait and requests:
> *"ช่วยเกรดสีรูปพอร์ตเทรตนี้ให้ดูแพง สกินโทนเนียนเป็นธรรมชาติ ไม่หลอกตา"*

---

## Retoucher's Mental Model (ลำดับการคิดเชิงศิลป์)
1. **Never Over-Saturate Skin**: Never push global `saturation` on portraits; it introduces harsh orange/red patches and sunburn looks. Always use **`vibrance`** (+6 to +12) which protects skin tone luminance.
2. **Skin Texture Protection**: Avoid high `clarity` on faces (clarity accentuates pores and blemishes). Instead, use slight negative clarity (-5 to -10) on skin if needed, or rely on Camera Raw's gentle `shadows` lifting.
3. **Subject Isolation**: Use Adobe Sensei `photoshop_select_subject` to create a dedicated mask before lifting background exposure or changing background color.

---

## Tool Execution Sequence

### Step 1: Sensei Subject Detection
```json
// Tool: photoshop_select_subject
{}
```
*Effect: Adobe Sensei automatically isolates the person from the background with hair-level boundary precision.*

### Step 2: Non-Destructive Subject Relighting
```json
// Tool: photoshop_create_adjustment_layer
{
  "adj_type": "curves",
  "name": "Subject Radiance"
}
```

### Step 3: Studio Camera Raw Color Harmonization
```json
// 1. Convert background/composite to Smart Object
// Tool: photoshop_convert_to_smart_object
{}

// 2. Camera Raw Color Engine
// Tool: photoshop_apply_camera_raw_filter
{
  "exposure": 0.15,
  "shadows": 10,
  "highlights": -8,
  "clarity": -3,
  "vibrance": 8,
  "temperature": 2,
  "tint": 1
}
```
*Effect: Smooth natural skin tones, soft shadow transitions, highlights protected without blowout.*

### Step 4: Export Master Portrait
```json
// Tool: photoshop_export_as
{
  "file_path": "/path/to/portrait_editorial_master.jpg",
  "format_type": "jpeg",
  "quality": 95
}
```
