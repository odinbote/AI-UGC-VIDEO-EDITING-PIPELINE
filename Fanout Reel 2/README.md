# Fanout Reel 2 — "Structured paths" (built from the AI UGC 1 system)

Open `Fanout Reel 2.prproj` in Premiere Pro 26.5. All media is inside `Media/` (self-contained, 1080x1920, 24 fps, 9.3 s).

## What's on the timeline

| Time (frames) | Section | Layers |
|---|---|---|
| 0–38 | Layout: curriculum list scroll | White matte, `fanout_system_curriculum_list.png` scale 165 scrolling y 0.95→0.40 (50 f linear), cutout rotated −11° at x 0.61 |
| 38–67 | Layout: lesson push-in | `fanout_lesson_sql_kv.png` scale 56→74 over 24 f (eased), cutout centred |
| 67 | Jump cut | 0.458 s of pause removed from the A-roll (src 2.79→3.25 s), click SFX 3 f before |
| 67–128 | Full-screen A-roll + title | Scale 140, y 0.57. "Instead of" (f67) / "memorizing" (f76) / "random concepts" (f88), all end on f114; captions "you'll" / "understand" after |
| 128–173 | B-roll + cutout + titles | Silicon Valley (f128), Social Network cut in on "the way" (f157). "Why" / "Systems" / "are designed" → "the way" / "they are?" |
| 173–223 | Outro | White matte + fanout loader (scale 48) |

Captions (green pill, Instrument Serif Italic): "with structured", "learning", "paths", "and", "interactive", "animations.", "you'll", "understand".
SFX: Mechanical click before each layout cut, UI clicks on the b-roll cuts and the outro cut. Music: Electronica the Witch from 14.875 s.
Grade: adjustment layer (Faded Film 28 + Noise 5 %) over the dialogue, not the outro.

## Things to check in Premiere

1. **Cutout (V7 "Aroll Cutout")** uses `veo31_take3_cutout_alpha.mov`, an AI-generated alpha matte (isnet). If you prefer Premiere's Object Mask like the original, replace those three clips with the raw A-roll and apply Object Mask → track. Clip in/out points are already correct for a 1:1 swap.
2. **Media re-scan**: `veo31_1080p_take3.mp4` and the two PNGs replace the old A-roll / screenshot entries, so Premiere may show "media pending" for a second while it re-indexes them.
3. **Titles** are the exact graphics from AI UGC 1 (same fonts, sizes, box colours, Text Animator in: Ease Out 80 / Fade 75 / push-up / motion blur). In-transition lengths are 18 f on the long titles and 4–10 f on short ones, like the original.
4. The raw clip starts mid-sentence ("with structured…"), so the reel has no hook section; everything else follows the system.

Preview render (approximate, PIL compositor, no grade): `Fanout_Reel_2_preview.mp4` next to this file.

## Regenerate

```bash
python3 "../tools/build_prproj.py" "../Fanout Reel 2 plan.json"
PREVIEW_REUSE= python3 "../tools/render_preview.py" "../Fanout Reel 2 plan.json" "Fanout_Reel_2_preview.mp4"
```
