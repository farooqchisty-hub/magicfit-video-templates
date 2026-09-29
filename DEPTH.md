# World depth pass (read fully, then also re-read BRIEF.md for the house rules)

Farooq approved the storyboards but wants far more world depth: specific props, objects, elements and detailing. Reference implementation: the "world_bible" block and the per-shot "dressing" lists in styles/cinematic/board.json and styles/claymation/board.json. Before/after proof: docs/sheets/depth/index.html. Match that structure and bar.

## What to add to each board.json (beats, cast, screenplay and units stay as they are)
1. `world_bible`:
   - `lore`: 4 or 5 concrete facts (who, where, when, history, what is at stake) that make the world feel real. Names, numbers, small histories.
   - `materials_rule` (stylized styles only, e.g. anime, comic, pixar3d, miniature, talking_objects, how_its_made, retro_infomercial): what every object is made of / how it is drawn or built in this style.
   - `locations`: for EVERY location id in the board, `foreground`, `midground`, `background` lists, 12 to 20 items in total. Each item is specific: material, age, wear, owner or story ("a dented sky-blue roll-cab tool chest with coloured tape strips on the drawers", not "a tool chest").
   - `personal_props`: 3 to 5 per cast member, each with a story or wear detail.
   - `signature_objects`: 2 to 4 designed objects unique to this world, each with `id`, `name`, `prop_prompt` (a prop reference sheet on plain mid-grey background, style-appropriate, no letters). These render as prop sheets and become references.
   - `brand_system`: each fictional brand with `name`, `mark` (a simple shape or symbol), `colors`, `appears_on`, `text_in_post`.
   - `wear_and_time`: time of day, weather, what has been used, what is out of place.
   - `sound_world`: 5 to 8 specific sounds from those objects.
2. For every shot: `dressing` = 3 to 6 specific items from the world bible (spread across depth layers), and add signature object ids to `refs` where the object is visible.

## Rules learned in the pilot (mandatory)
- Specificity comes from marks, shapes, wear and objects, NOT letters: chalk tally marks, drawn stars, coloured tape, stickers as drawings. Any readable text still goes in post.
- Never write words in capitals in prompts (ANALOG, START): the model prints them onto objects. Describe the look.
- Face shots: at most 3 references (cast card, product, one location). Describe props in text instead of adding prop references, or faces drift.
- The location plate carries most of the depth; everything inherits from it. Keep the hero subject and the can clearly readable at phone size: detail should frame the subject, not bury it. Density high in the background and mid, cleaner around the subject.
- Product-adjacent props stay generic enough to swap per product (note them in the adaptation block if relevant).
- No em or en dashes anywhere.

## Render and QA
- Re-render locations, signature objects and ALL keyframes (not cast cards): `python3 lib/render.py <key> --only <loc ids>,<object ids> --force`, then `python3 lib/render.py <key> --only S01,...,S10 --force`. If ERR, re-run the ids that failed.
- Montage and LOOK at every frame (use your own scratch subfolder `scratchpad/<your key names>/`, other agents share the scratchpad). Previous frames are in styles/<key>/v1/img for comparison. Check: depth visibly higher than v1, subject and can still clear, face consistency against the cast card, can fidelity, no garbled or readable model text, no real brands, no weapons, no rotated frames, physics. Re-roll with `--only SXX --force` (max 3 rounds per shot), add lessons to failure_modes.
- `python3 lib/page.py <key>`. Do not git commit or push.
Budget about $1 per style.

## Report back (short)
Per style: 2 or 3 of the best new specific details, re-rolls and why, anything unresolved.
