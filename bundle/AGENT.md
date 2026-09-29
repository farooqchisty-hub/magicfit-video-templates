# MagicFit Video Templates: agent runner

You are turning ONE template plus ONE product URL into a finished 30 second, 9:16 video ad with captions. The template fixes the concept (world, cast, story, camera, sound). You adapt the product into it. Follow the stages in order. Do not skip the checks.

## What you need
- A video model that takes reference images (best: Seedance 2.x reference mode; also works: Veo 3.x, Kling 2.x with image references). 4 to 15 second clips.
- An image model that takes several reference images (best: Gemini 3 Pro Image / Nano Banana Pro; GPT Image works but check product text carefully, it rewrites labels).
- ffmpeg, Python 3 with Pillow (`pip install pillow`), and ideally a speech-to-text model (Whisper) for caption timing. No libass needed.
- Inputs from the user: a template folder (`templates/<id>/`) and a product URL. Optional: target market (default North America), a max budget.

## Files in a template folder
- `template.json`: the concept, cast, world bible, shots, script intents, generation units, sound and caption plan, fit ratings, and a fully worked `example_fill`.
- `style.json`: the style bible (look, camera, pacing, caption look, known failure modes, negatives, prompt prefix). Obey its `failure_modes` and `negatives`: they are lessons from real renders.
- `assets/`: cast cards, location plates and signature objects. Reuse them as references; never redraw the cast. `template.asset_urls` maps each asset id to a public URL for models that need URLs.
- `manifest.json` (bundle root): every template with its fit ratings, for suggesting alternatives.

## Stage 1: Product card
Fetch the product page. Shopify stores expose `https://<store>/products/<handle>.json`; otherwise read the page's JSON-LD `Product` block, then the visible text. Build:
```json
{"name":"", "brand":"", "phonetic":"how to say the brand, e.g. RED BULL SHUG-er-free",
 "short_name":"what a person calls it out loud: the can, my serum, these shoes",
 "visual":"one sentence describing its look (shape, colours, label, material) for image prompts",
 "archetype":"ingested | applied | worn | handheld | carried | home | consumable",
 "scale":"hand | body | room", "image":"public URL of the cleanest front product image",
 "benefits":["verbatim claims from the page, 1 to 5"], "tagline":"only if the page has one",
 "use_moments":["when people use it"], "forbidden":["claims or depictions to avoid"]}
```
Rules: benefits are copied from the page, never invented. No medical, weight, or numerical performance claims unless the page states them word for word. If the product is for children, alcohol, tobacco, weapons, or a regulated drug, stop and tell the user.

## Stage 2: Fit check
Read `template.fit.archetypes[product.archetype]` and `template.fit.avoid`. If the rating is `stretch` or the product matches an `avoid` entry, tell the user plainly, name 2 better templates from the bundle manifest if you can, and ask whether to continue.

## Stage 3: Fill the template
1. Actions: for every shot with `product_action`, take the entry for `product.archetype` and substitute `{{product.visual}}` and `{{product.short_name}}`. Read it back against the world: is it physically plausible at this scale? If not, rewrite it inside the same beat and world, keeping the camera and timing.
1b. Rival shots: if a shot has `"action_subject": "rival"`, its action describes the template's generic, unbranded rival (never a real brand). Generate the rival prop from the template's rival prompt for this archetype and use it as that shot's reference instead of the product image.
2. Lines: write each product line from its `line_intent`, `rules` and `max_words`. Keep every `fixed_line` exactly. Total spoken words must stay under about 70 (2.5 words per second). The brand goes in speech as written, and in video prompts with `product.phonetic` after it.
3. Product-adjacent props: use `world_bible.product_adjacent[archetype]` in the shots near the product.
3b. `{{product.tagline_or_line.<line id>}}` means: product.tagline if the page has one, otherwise the filled text of that line. `sub_fallback` on a post_text entry names the line to use when there is no tagline.
4. Fill every `{{...}}` in `shots[].keyframe_prompt`, `units[].prompt`, `shots[].caption` and `post_text`. No braces may remain.
5. Compare your fill with `example_fill`: same structure, same energy, different product.
Save as `run/fill.json`.

## Stage 4: Keyframes (the storyboard)
For each shot build the image prompt: `style.prompt_prefix` + filled `keyframe_prompt` + `Specific details in this shot: <dressing>` + one sentence per reference saying what it is ("Image 1 is the product: reproduce it exactly", "Image 2 is the character sheet for Jess") + `Avoid: <style.negatives>`. References: the product image, the cast cards and plates listed in `refs` (at most 3 references in any shot that shows a face). Generate at 9:16.
Check every keyframe before moving on: product identical to the product image (shape, colours, label text), faces match the cast cards, no readable text drawn by the model, no real brands, no extra limbs, no rotated frame, physics plausible. Re-roll a failed shot up to 3 times, fixing the prompt each time. Save `run/keyframes/Sxx.png` and a contact sheet `run/contact_sheet.png` (all frames in order with their captions). If the user asked to review the storyboard, stop here and show the contact sheet.

## Stage 5: Video units
For each entry in `units`: send the filled `prompt` with its references (the unit's first keyframe as the first frame or reference, the product image, cast cards). Keep native sound on. Most units say "No music": respect it, the score is added in Stage 6. Units flagged `exact_risk` hold the brand and CTA lines: check them first and re-roll cheaply if the brand is misspoken or the product morphs.
Check every clip: transcript against the filled lines (the brand pronounced correctly), faces consistent, the product unchanged, no morphing hands, no physics errors, no dark or flash frames. Save `run/units/Ux.mp4`.

## Stage 6: Assemble
1. Plan the edit: each unit trimmed to its planned duration, in order, 30 fps throughout.
2. Music: one continuous score across all units, built from `template.music` sections (generate each section with a text-to-music model and cross-fade at the section boundaries). Duck it under dialogue. It must not restart at a cut and must carry into the end.
3. Added sounds: only those in `template.sfx`.
4. Captions (mandatory wherever there is speech) and post text: transcribe the joined vocal track for word timings (or use the planned line timings if no transcriber). Write `run/timing.json` as `{"words":[{"word","start","end"}...]}` or `{"lines":[{"text","start","end"}...]}`, plus `"post"` from `template.post_text` (filled product name and tagline, rendered in code, never by a model) and `"duration"`. Run `python3 tools/captions.py run/timing.json templates/<id>/template.json run/captions`. It renders the style's caption look (font, colour, position, max words on screen, active word highlight) and writes `run/captions/captions.srt`. Put `"captions_concat":"run/captions/captions.ffconcat"` in `run/edit.json`.
5. Run `python3 tools/assemble.py run/edit.json` (see the docstring for the edit.json shape: clips with in and out points, music sections, sfx, captions).
6. assemble.py normalises loudness to -14 LUFS and exports `run/final.mp4` (1080x1920, H.264, AAC). Copy `run/captions/captions.srt` to `run/final.srt`.

## Stage 7: Final check and delivery
Watch the final at full length. Report to the user: what was made, the product card used, every line as spoken, what you checked and what you could not check, and the cost. List any compromises honestly.

## Model notes (from real runs)
- Seedance on Replicate (2.5 and 2.0) rejects photoreal human faces in reference images and first frames (error E005). Stylized characters (3D, anime, clay, comic) pass. For photoreal templates either use a Seedance provider that accepts face references, or generate the whole ad as ONE native 30 second take (Seedance 2.5 supports it) with only the product and people-free references, describing the cast in text so the same people stay on screen.
- Reference syntax differs by provider: Replicate Seedance uses [Image1], [Image2]; convert the template's @Image tokens. Replicate cannot combine a first-frame image with reference images, so pass the storyboard keyframe as an extra reference ("[Image3] is the storyboard frame: match its composition").
- Uncommon brand words are often mispronounced in long takes. Always transcribe the brand line with two transcribers. If it is wrong and the line cannot be re-rolled cheaply, clone the speaker's voice from their own clean lines in the same take (e.g. Chatterbox with an audio prompt), generate only the brand words, splice them over the wrong words with a rain or room-tone bed, and re-check. Say the brand in the prompt plainly ("ember, like a glowing coal, then mug, like a coffee mug"); a parenthetical spelling can be read aloud.
- Video models improvise extra lines. Say "Only the scripted lines are spoken; no extra dialogue." Mute unscripted off-camera lines in the edit.
- A shot marked product-absent can still need the product: once a worn product is put on, it stays on the character in every later shot. Add it to those keyframes and units.
- Phrases like "one hand touching it" make image models put a second product in the hand. Describe empty hands instead.
- Resolve every either/or phrase in a product_action ("laces, strap, zip or fastening") to the one that fits, and fix grammar for pairs and plurals ("a pair of ... sneakers").
- Describe the product in full on its first mention in a prompt, then call it "the product".
- Always pass the cast card for every shot where the character appears. If a character drifts, add an explicit identity lock sentence (colours, glasses, scarf, no fingers on wings) and keep face shots to 3 references.

## Global rules
- Fictional world: invent any other brand; every other sign is blank or uses the template's fictional brands.
- Never show a real competitor. Never show children using adult products.
- Casting follows the template's cast cards. Do not replace the cast.
- No em dashes or en dashes in any on-screen text or caption.
- Never send, publish or post anything. Deliver files to the user.
