# Learnings from the first 3 real videos (30 Sep 2026)

| # | Finding | Where it now lives | Still to do |
|---|---|---|---|
| 1 | Replicate Seedance blocks photoreal faces (E005); stylized passes | AGENT.md model notes | Decide provider for photoreal templates (treg seedance-2.5-face accepts faces) |
| 2 | asset_urls were stamped with expiring hosts and path keys, so the runner silently got no cast card | publish_bundle.py + lint check | none |
| 3 | Location plates still contain example-product props (cinematic garage ice bucket of cans) | noted | Re-render product-free plates for all 22 templates, add a vision QA check |
| 4 | Worn products must persist on the character after they are put on | AGENT.md | Mark later shots in worn-rated templates with product_persists |
| 5 | "one hand touching it" makes the model add a second product | AGENT.md | Sweep all templates for hand-contact phrasing |
| 6 | Either/or options and plurals leak into prompts | AGENT.md | Lint for "or" lists inside product_action |
| 7 | Brand words mispronounced in long takes; voice-clone splice fixes it | AGENT.md + Chatterbox recipe | Add a splice tool to bundle/tools |
| 8 | Models improvise extra lines | AGENT.md | none |
| 9 | Product-free keyframes can ship with the template (cheaper, consistent) | noted | Ship keyframes/ for product-absent shots |
| 10 | captions.py needed outline parsing, title wrap, anime name cards, SFX lettering | bundle/tools/captions.py | Caption position per shot (pack shots) |
