# Golden Example 1: Master Travel & Architectural Photo Retouch

## Scenario
The user provides a travel photo (e.g. at a landmark or historic terrace) with unwanted tourists in the background and a flat, overcast sky, asking:
> *"ช่วยลบคนข้างหลังออกให้หมด แล้วเปลี่ยนท้องฟ้าให้ดูสดใส ปรับแสงให้สวยเป็นธรรมชาติ"*

---

## Retoucher's Mental Model (ลำดับการคิดเชิงศิลป์)
1. **Never use naive Content-Aware Fill on architecture**: People are standing against carved stone balustrades and perspective railings. Patch-match algorithms will blur straight lines and create obvious duplicate smudges. **Must use Adobe Firefly Generative AI (`photoshop_generative_fill_ai` or `photoshop_generative_remove_ai`)**.
2. **Surgical Selection**: Tightly bound the tourists (add only 5-10px padding) and feather by 2.0px. Do not select huge swathes of undamaged stone.
3. **Realistic Sky Dynamics**: Real bright skies possess **Atmospheric Horizon Haze** (low saturation, bright mist near terrain/rooftops) and **cast warm ambient light onto the foreground**. Putting a blue sky without relighting the subject looks instantly fake.
4. **Non-Destructive Final Grade**: Convert composite to Smart Object, apply Adobe Camera Raw filter for unified Dehaze, Clarity, and Vibrance.

---

## Tool Execution Sequence

### Step 1: Document Inspection
```json
// Tool: photoshop_get_document_info
{}
```
*Result: Confirm document dimensions, e.g. 4000x3000, RGB mode.*

### Step 2: Autonomous Distraction Removal via Firefly
```json
// Tool: photoshop_generative_remove_ai
{
  "regions": [
    [710, 1515, 1025, 2335],
    [2420, 1600, 2750, 2280]
  ],
  "feather_px": 2.5
}
```
*Effect: Generative Fill autonomously synthesizes continuous stone railings and textures with perfect perspective and shadow consistency.*

### Step 3: Sensei Sky Replacement with Horizon Haze & Ambient Relighting
```json
// Tool: photoshop_harmonize_sky
{
  "new_sky_path": "/Users/baramesh/Downloads/sample_sky.jpg",
  "sky_opacity": 85.0,
  "warm_foreground": true
}
```
*Effect: Sensei isolates the sky boundary. Embeds atmospheric haze gradient along the horizon and applies gentle warming Curves to the foreground subject.*

### Step 4: Pro Hollywood Camera Raw Finishing
```json
// 1. Convert to Smart Object
// Tool: photoshop_convert_to_smart_object
{}

// 2. Camera Raw Studio Grade
// Tool: photoshop_apply_camera_raw_filter
{
  "dehaze": 8,
  "clarity": 12,
  "vibrance": 10,
  "temperature": 3,
  "shadows": 5
}
```
*Effect: Pops midtone micro-textures on stone, removes ambient atmospheric cast, unifies color temperature across the whole frame.*

### Step 5: Visual Verification & Export
```json
// Tool: photoshop_export_as
{
  "file_path": "/path/to/final_master_retouched.jpg",
  "format_type": "jpeg",
  "quality": 92
}
```
