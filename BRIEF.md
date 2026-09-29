# Storyboard brief for style agents (read fully before starting)

Project: 200+ product-agnostic 30 s video ad templates across 22 styles. This round: ONE flagship storyboard per style for the example product Red Bull Sugarfree, 9:16, 30 s. Farooq reviews all 22 contact sheets at Checkpoint 1.

## Files
- Product card: product/red-bull-sugarfree.json (facts, allowed_claims, forbidden, look, image URL). Product reference sheet: product/pack/can_sheet.png.
- Reference implementation (schema AND quality bar): styles/cinematic/style.json and styles/cinematic/board.json. Match every field. Do NOT reuse its creative choices (no racing, no rain garage, no Jess/Ray).
- Tools: `python3 lib/render.py <key>` renders cast cards, location plates, then keyframes (skips ones already rendered). `python3 lib/render.py <key> --only S03,S07 --force` re-rolls. `python3 lib/page.py <key>` builds docs/sheets/<key>/index.html. Images land in styles/<key>/img/. If a render prints ERR (treg timeout), just re-run it.

## For each of your styles, write styles/<key>/style.json then styles/<key>/board.json
style.json: key, name, definition, why_it_sells, visual_grammar, camera, light, texture, palette_rule, pacing, sound, caption_look (object: font, size, color, active_word, shadow or box, position, max_words_on_screen, and anything style-specific), model_vocab, failure_modes, negatives, prompt_prefix. These are the rules that make the style recognisable and that the video model needs. Make them specific and genuinely expert, not generic.

board.json fields exactly as the cinematic board: id (<key>-01-<slug>), style, title, logline (with {product}), runtime_s 30, aspect "9:16", product_ref, world (setting, palette, fictional_brands, rules), cast (id, name, role, look, voice, card_prompt), locations (id, name, plate_prompt), adaptation (all 7 types: ingested, applied, worn, handheld, carried, home, consumable, each {moment, scale}), beats, script (id, t, speaker, on_camera, line_intent, line, delivery, shot, optional phonetic and claim), shots (8 to 12; id, t0, t1, beat, framing, camera, action, product_state, audio, caption, refs, keyframe_prompt), units (2 to 4 generation units, each 4 to 15 s, totalling 30 to 33 s; exact_risk true for units holding the brand name or CTA; full video-model prompt using @Image1/@Image2 references, native sound, "No music" when spliced), music (sections), sfx (only sounds the viewer must register), voices, post_text, claims_used, cost_estimate (seconds x $0.27/s).

## Hard rules
1. The concept is FIXED and product-agnostic; only wording and product moments adapt. Every line has a line_intent that would work for any product, plus the Red Bull wording.
2. Claims: only allowed_claims from the product card (alertness/concentration, less tiredness, same benefits without sugar, the tagline "Wiiings without sugar"). Never calories, health, weight loss, or medical claims. No children drinking it. No more than one can per person per scene.
3. At most about 70 spoken words in 30 s (about 2.5 words per second). Wherever there is voiceover or dialogue there are captions (caption field per shot).
4. Fictional world: made-up brands only, every other sign blank. The only real brand is the product. Never name a real competitor (rivals are generic).
5. Casting for North America; vary gender, age and ethnicity across your styles; no Indian-coded characters. Speakers appear on camera on their first line unless the style is voiceover-led.
6. Brand name: "Red Bull Sugarfree" said as "RED BULL SHUG-er-free", in a short exact-risk unit.
7. Physics and continuity: one physical state per object per shot; the can keeps its exact shape and label.
8. Anything that must be legible (UI text, comic lettering, news tickers, infomercial price cards, text messages) is RENDERED IN CODE IN POST, never by the image or video model. Keyframe prompts should ask for clean areas or unreadable placeholder shapes there, and post_text describes what gets added.
9. NO em dashes or en dashes anywhere, in any file. Use commas, colons or parentheses. Ranges as "4 to 8".
10. Keyframe prompts are self-contained and say which reference is what ("the woman from the character sheet", "the exact can from the product reference"). Include the product in refs whenever the can is visible. Wide scenes: say "upright vertical composition, level horizon" (side-on vehicles and wide scenes sometimes come back rotated 90 degrees).
11. Each style must feel unmistakably like that style at a glance, and be a genuinely good ad: hook in the first 2 seconds, a clear product moment held at least 1.5 s, a payoff and an in-world CTA.

## QA loop (mandatory)
After rendering, build a montage of all keyframes (ffmpeg hstack/vstack, e.g. two rows of 5 at 300 px wide, `scale=300:534:force_original_aspect_ratio=decrease,pad=300:534:(ow-iw)/2:0`) into your scratch dir and LOOK at it with the Read tool, plus the cast cards. Check: can fidelity (sky-blue and silver diagonal split, red Red Bull wordmark, two red bulls, gold sun, SUGARFREE), same faces across shots, no garbled or readable model-generated text, no real brands, no rotated frames, no physics errors, style unmistakable. Fix the prompt, add the lesson to the style's failure_modes, re-roll with --only X --force. Up to 3 rounds per shot; record anything still imperfect.
Then run `python3 lib/page.py <key>`. Do NOT git commit or push.

Budget: about 14 images per style at $0.03 each plus re-rolls; stay under $2 per style.

## Report back (short)
Per style: key, title, one-line logline, spoken word count, number of re-rolls and why, anything unresolved.
