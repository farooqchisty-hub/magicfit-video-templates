# Template spec v1 (for turning an approved board into a sellable template)

A template is a FIXED concept (world, cast, story, beats, camera, sound, captions) that takes ANY physical product. The buyer's agent reads `template.json`, the style bible `style.json` and a product card built from a product URL, then fills every slot. Nothing about the example product may remain outside `example_fill`.

Reference implementation: `bundle/templates/cinematic-01-night-stint/template.json`. Validate with `python3 lib/lint_template.py <template dir>` (must print PASS).

## Files per template: bundle/templates/<id>/
- `template.json` (this spec)
- `style.json` (copied from styles/<key>/style.json)
- `assets/` cast cards, location plates, signature object sheets (copied, JPG 1536 px). These are part of the product: the buyer reuses them so faces and worlds stay identical. Reference them by relative path; `asset_urls` in template.json maps each to its public URL.

## Product card (what the runner builds from the URL; templates reference these fields)
`product.name`, `product.brand`, `product.phonetic` (how to say the brand), `product.short_name` (what a character calls it in speech, e.g. "the can", "these shoes", "my serum"), `product.visual` (one sentence describing its look, used in prompts), `product.archetype` (one of: ingested, applied, worn, handheld, carried, home, consumable), `product.scale` (hand, body, room), `product.benefits` (verbatim claims from the page only), `product.tagline` (only if the page has one, else empty), `product.use_moments`.

## template.json fields
- `id`, `style`, `title`, `version` "1.0", `runtime_s` 30, `aspect` "9:16", `logline` with `{{product.name}}`.
- `fit`: `archetypes` object with each of the 7 archetypes rated `great`, `good` or `stretch` plus a one-line reason; `avoid` (products this concept should refuse, e.g. "products for children", "large furniture" if it truly cannot work).
- `world_bible`: copied from the board, but product-adjacent items move to `product_adjacent` keyed by archetype (e.g. ingested: "a steel ice bucket of crushed ice"). No example-product words anywhere else.
- `cast`, `locations`, `signature_objects`: as in the board, each with `asset` (relative path) and the original prompt for regeneration.
- `beats`: as in the board, product mentions replaced by slots.
- `script`: each line has `id`, `t`, `speaker`, `on_camera`, `shot`, `delivery`, `line_intent` (product-agnostic, says exactly what the line must do), `max_words`, `rules` (e.g. "benefit must be one of product.benefits, reworded no further than tense and person"), and `fixed_line` ONLY if the line never changes with the product (no product words). Product lines never have fixed wording.
- `shots`: as in the board plus `product_role` (absent, reveal, hero, in_use, background). For every shot where the product appears or is used: `product_action` object with ALL 7 archetypes, each a concrete, physically plausible action or placement in THIS world at the right scale. `keyframe_prompt` uses `{{action}}` for that text and `{{product.visual}}` / `{{product.short_name}}` where the product is described. `refs` uses "product" for the product image.
- `units`: as in the board, with `prompt` rewritten as a template: `{{action.S05}}` for shot actions, `{{line.L4}}` for lines, `{{product.visual}}`. Exact-risk units stay short.
- `music`, `sfx`, `voices`, `captions` (from the style: font, colour, position, max words), `post_text` (templated: `{{product.name}}`, `{{product.tagline_or_line.L7}}`).
- `qa`: checks the runner must pass for THIS template (in addition to the global ones in AGENT.md).
- `example_fill`: the Red Bull Sugarfree version: product card, every line filled, every action chosen. This is the worked example the buyer's agent can study.

## Rules
1. No example-product words ("Red Bull", "Sugarfree", "can", "cans", "sip", "sugar", "drink", "fizz", "ice bucket" for the product) outside `example_fill` and `product_adjacent.ingested`. The lint enforces this.
2. Every `{{...}}` used must be a product card field, `action`, `action.<shot id>` of a shot that has `product_action`, or `line.<id>` of a script line.
3. Product actions must respect scale: a sofa is never held; a serum is never sat on. `home` products move the product beat to where such an object would live in this world.
4. Keep all house rules from BRIEF.md and DEPTH.md (no em or en dashes, fictional world, legible text in post, claims only from product.benefits).

## How to build one (for conversion agents)
1. `mkdir -p bundle/templates/<id>/assets`, copy styles/<key>/style.json in. The id is the board's id (e.g. ugc-01-finals-week).
2. Assets: for every cast id, location id and signature object id, convert styles/<key>/img/<id>.png to `assets/<id>.jpg` with `ffmpeg -y -loglevel error -i <png> -vf "scale='min(1536,iw)':-2" -q:v 3 <jpg>`.
3. Write template.json from styles/<key>/board.json following this spec and the reference template exactly (study how the reference turned the board's product shots, units, lines and world bible into slots, and how it wrote all 7 product_action entries per product shot). Human-readable fields (action, product_state, audio, beats) must also be product-agnostic.
4. `python3 lib/lint_template.py bundle/templates/<id>` until PASS.
5. Self-review: read every product_action for every archetype and ask "would this be physically plausible and good-looking in this world for a sofa, a serum, a hoodie, a phone case, a backpack, a snack bar?" Rewrite weak ones. Set honest fit ratings.
