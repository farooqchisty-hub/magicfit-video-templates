import json,re
X=lambda u,i:f"https://x.com/{u}/status/{i}"
R=lambda s:f"https://www.reddit.com/r/{s}"
S=[]
def add(name,defn,sources,mentions,examples,numbers,fmt,signal,agn,agn_note,notes=""):
    S.append(dict(style=name,definition=defn,sources=sources,independent_mentions=mentions,
      notable_examples=examples,performance_numbers=numbers,format_type=fmt,performance_signal=signal,
      product_agnostic=agn,product_agnostic_note=agn_note,notes=notes))

add("Podcast-style clip ad (real or AI fake podcast)",
 "Two people at mics in a studio set; the product comes up mid-conversation so it reads as a clipped podcast moment, not an ad.",
 ["X","Reddit","LinkedIn","Web"],20,
 ["AG1 podcast UGC playbook (Influee swipe file)","Danger Coffee founder podcast ads (Dave Asprey)","grounding product podcast VSL (FedotOff90)","Veo 3 / Gemini Omni AI podcast ads (maxxmalist, NahFlo2n, Mho_23)"],
 [{"claim":"Influee saw 9x as many podcast UGC briefs since 2022","url":"https://www.linkedin.com/posts/sebastian-novin_ag1-scaled-from-160m-to-600m-in-3-years-activity-7509159961608704000"},
  {"claim":"Ranked S tier AI UGC format ('best format for anything that needs explaining')","url":X("CEO_Vlad","2096569603761827953")},
  {"claim":"Ranked A tier ecom format","url":X("ChelalaPierre1","2103088143138193657")},
  {"claim":"'podcast style VEO3 ads are crushing for us right now' (327 likes, 65k views)","url":X("maxxmalist","1970196560718794918")},
  {"claim":"One of 5 formats scaling clients past $300k/mo","url":X("lorenzo_pravata","1998842454238199877")},
  {"claim":"AI fake podcast $12 to 15 per 30s clip","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"}],
 "proven_performance","strong","partial","Best for products that need explaining (supplements, gadgets, wellness); weak for pure impulse or visual products.",
 "Backlash signal: Reddit threads complain about ads posing as fake podcast clips (r/AskMarketing) and full podcast episodes as YouTube ads (r/mildlyinfuriating, 452 upvotes).")

add("UGC testimonial / talking head (human creator)",
 "A real customer or creator speaks to camera about their result, shot on a phone in a natural setting.",
 ["X","Reddit","LinkedIn","Web"],12,
 ["Ryze Superfoods (24% of 5,324 active ads are UGC talking head)","Angry Orange ('This saved my marriage' review-led creative, $40M in 18 months)"],
 [{"claim":"#1 Instagram ad format 2026, avg CTR 2.5 to 4%","url":"https://www.balistro.com/instagram-ad-creative-ideas-convert-2026/"},
  {"claim":"Ryze format mix: UGC talking-head 24%","url":X("FedotOff90","2092303494250135860")},
  {"claim":"Roughly 1 in 10 to 12 creator pieces become winners","url":R("EntrepreneurRideAlong")+"/comments/1vr8fcy/"},
  {"claim":"Testimonials one of 5 ads used across $100M Meta spend","url":"https://www.linkedin.com/posts/curtishowland_ive-spent-100m-on-meta-ads-in-the-dtc-space-activity-7417573805969276928-75Mk"}],
 "proven_performance","strong","yes","Works for any physical product with a customer outcome to describe.")

add("AI UGC avatar ad (synthetic creator)",
 "An AI-generated person films a selfie-style testimonial, unboxing or demo with the real product composited or generated in.",
 ["X","Reddit","LinkedIn","Web"],18,
 ["Arcads gaming laptop and protein smoothie ads (SparkifyAI)","Higgsfield Marketing Studio UGC style","Kling 3.0 one-prompt UGC (mikefutia)"],
 [{"claim":"'huge Ecom brands spend upwards of 90% of their budgets on AI creatives' (practitioner claim)","url":R("AI_UGC_Marketing")+"/comments/1ud6rrl/"},
  {"claim":"Real customer video beat AI UGC 'by a landslide' on every PDP test (Videowise brands)","url":"https://www.linkedin.com/posts/claudiucioba_18-months-ago-i-thought-ai-generated-ugc-activity-7455901492676460545-GUUZ"},
  {"claim":"16B-impression study: AI ads match human CTR unless they look AI; perceived artificiality lowers CTR","url":"https://www.linkedin.com/posts/ericseufert_ai-generated-ads-perform-roughly-as-well-activity-7461053580997853184-s9Nk"},
  {"claim":"Ranked F tier ecom format","url":X("ChelalaPierre1","2103088143138193657")},
  {"claim":"Higgsfield Marketing Studio launch post 3.79M views","url":X("higgsfield","2043752265472004424")}],
 "proven_performance","contested","yes","Product-agnostic, but trust-heavy categories (skincare claims, health) carry FTC/EU AI Act exposure for synthetic testimonials.",
 "Proven format, contested AI execution: cost wins are clear, conversion wins are disputed.")

add("Pixar-style 3D animated story",
 "Stylized 3D animated mini-story, often with the product or a body part as an expressive character; pain point, quick narrative, product as hero.",
 ["X","Reddit","LinkedIn","Web"],16,
 ["Ryze Superfoods (17% of active ads are AI-animated 3D/Pixar storytelling)","Jeep AI-generated anthropomorphic spot premiered at Cannes Lions 2026","'Pixar doctor' AI VSLs (Lachezar Voynov)","Flowmix (construction) Pixar-style ad"],
 [{"claim":"Client spent $80K on one Pixar-style AI ad, still profitable, outperforming UGC","url":"https://www.linkedin.com/posts/aazarshad_everyones-calling-ai-generated-content-activity-7439294828200411137-HHfH"},
  {"claim":"Client ad: 12% CTR, 5% CVR","url":R("AI_UGC_Marketing")+"/comments/1sy17ny/"},
  {"claim":"Commenter across 4 DTC clients: 3.8% hook rate vs 2.9% human UGC baseline","url":R("AI_UGC_Marketing")+"/comments/1sy17ny/"},
  {"claim":"'Winning on Meta ($45k)', $6 to 7 per video","url":R("FacebookAds")+"/comments/1ro2hyi/"},
  {"claim":"Ryze format mix: 17% AI-animated 3D/Pixar","url":X("FedotOff90","2092303494250135860")},
  {"claim":"'Pixar ads are crushing for my clients' (412 likes), good for boring products","url":"https://www.linkedin.com/posts/ferdinandterme_pixar-ads-are-crushing-for-my-clients-right-activity-7439660205677809664-_LRn"}],
 "novelty_scroll_stop_ai","strong","yes","Works for boring or invisible-benefit products (bandages, vacuums, supplements); the animation carries the story.",
 "Fatigue warning in r/FacebookAds comments: novelty dies once the feed saturates with the Pixar look.")

add("AI claymation / clay stop-motion",
 "Tactile clay characters and sets animated in stop-motion style, usually with an absurd premise and a clay villain/hero arc.",
 ["X","Reddit","LinkedIn","Web"],15,
 ["Bioma Health claymation ad (Shiv Sakhuja)","Vidrip app claymation spot (r/SideProject)","founder turned into claymation ad (kobyjconrad, 200+ creatives/month)"],
 [{"claim":"'2 to 3x the feed average CTR' (repeated by two creators)","url":X("spect3ral","2060415839422001561")},
  {"claim":"CTRs 2 to 3x feed average","url":"https://www.linkedin.com/posts/aashams1992_claymotion-ads-are-crushing-it-on-meta-right-activity-7448391881367142400-6n5d"},
  {"claim":"S tier: 'highest usable rate of any animation style'","url":X("CEO_Vlad","2096569603761827953")},
  {"claim":"Winning in multiple client accounts, made in 30 minutes","url":"https://www.linkedin.com/posts/fraser-cottrell_how-we-made-an-ai-claymation-ad-in-30-minutes-activity-7467541809678893057-T2Lr"},
  {"claim":"'These AI claymation ads are crushing it on Meta' 46k views, 408 bookmarks","url":X("mikefutia","2040101348621095173")},
  {"claim":"Caveat: absurdity pulls views not buyers; test as hook grafted onto a selling body","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"}],
 "novelty_scroll_stop_ai","moderate","yes","Any product; strongest for consumables and household goods; lean into absurd premise.",
 "Backlash in r/aislop and r/mildlyinfuriating ('disrespectful to animators').")

add("Street interview (real or AI)",
 "Interviewer stops passersby with a question; reactions and answers deliver social proof and the product reveal.",
 ["X","Reddit","LinkedIn","Web"],15,
 ["StreetTalk (Josh Suggs) for Ridge, Dr. Squatch, Magic Spoon and 100+ brands","NAKED perfume street interview (r/streetinterviewads)","Conzuri, IceMob, Cupid Fragrances (bradenbt)"],
 [{"claim":"StreetTalk: 8 figures ARR, over $100M attributable revenue","url":"https://www.linkedin.com/posts/josh-suggs-street-interview-ads-9912a3251_streettalk-has-reached-8-figures-in-a"},
  {"claim":"AI street interviews as paid ads: 4.5x ROAS","url":X("recap_david","2024150545884418432")},
  {"claim":"A tier: 'the question does the hooking, converts on social proof'","url":X("CEO_Vlad","2096569603761827953")},
  {"claim":"Contrarian: ranked F tier","url":X("ChelalaPierre1","2103088143138193657")},
  {"claim":"AI street interview cloned in 15 minutes (40 upvotes)","url":R("AI_UGC_Marketing")+"/comments/1tmb3ks/"}],
 "proven_performance","strong","yes","Any mass-market product with a relatable question hook.")

add("Founder story / founder-led ad",
 "The founder on camera explains why they built the product, from sit-down story to lo-fi phone rant to warehouse walk-and-talk.",
 ["X","Reddit","LinkedIn","Web"],12,
 ["Henson Shaving","BePresent","Danger Coffee (Dave Asprey)","Carpe warehouse challenge ad","Blume, HigherDose, Tushy (founder intro hooks)","Blogilates"],
 [{"claim":"Founder-story videos run 6 to 12 months, longest lifespan of formats","url":"https://adlibrary.com/posts/best-dtc-meta-ads-examples-2026"},
  {"claim":"'Problem-first founder video' single highest-converting content format for a DTC social agency","url":R("socialmedia")+"/comments/1sbyoqy/"},
  {"claim":"7 founder ad types with 100+ swipe file","url":"https://www.linkedin.com/posts/alexgoughcooper_founder-ads-you-need-to-run-activity-7462857254866870273-PrlE"},
  {"claim":"Ranked B tier","url":X("ChelalaPierre1","2103088143138193657")}],
 "proven_performance","strong","partial","Needs a real founder willing to be on camera; AI founder clones exist but invented founders are a trust risk.")

add("Cinematic AI product commercial (hyper motion / TV spot)",
 "Premium macro product film: splashes, levitation, ingredient bursts, drone dives, fast camera moves, generated end to end with Seedance/Veo/Kling.",
 ["X","Reddit","LinkedIn","Web"],18,
 ["Sapporo and Vitamin-C spec ads (D_studioproject, 147k and 322k views)","Therabody spec ad (Seedance 2.5)","Pepsi, Pringles, Cadbury prompt-share ads","Loop agency full-AI ATL ads on YouTube and Prime (r/VEO3)","Higgsfield 'Hyper Motion' and 'TV Spot' presets"],
 [{"claim":"Higgsfield URL-to-Ad with Hyper Motion / TV Spot styles, 150k views","url":X("higgsfield","2044163123268177929")},
  {"claim":"Counter: 'Cinematic ads, big-budget shoots, slow-mo product shots... performed the worst, every single time' across 25 Meta formats","url":"https://www.linkedin.com/posts/joe-hides_i-just-put-together-a-ranking-of-the-top-activity-7508123370182590464-BxCR"},
  {"claim":"Counter: cinematic skincare ad tanked while a grainy mirror review drove 4x CTR","url":"https://www.linkedin.com/posts/zahramaharana_digitalmarketing-marketingstrategy-consumerbehavior-activity-7501"},
  {"claim":"First full-AI ATL Veo 3 ad (536 upvotes)","url":R("VEO3")+"/comments/1o2gtdm/"}],
 "novelty_scroll_stop_ai","contested","yes","Any product with a hero shot; strongest for food, beverage, beauty, gadgets.",
 "Most-posted AI style on X (showcase content), weakest performance evidence for direct response.")

add("Singing / song ad (AI music)",
 "The whole script is a catchy AI-generated song (Suno/Udio), often over a cartoon or stylized character, sometimes a long drama-style musical VSL.",
 ["X","Reddit","LinkedIn","Web"],11,
 ["Ryze mushroom coffee singing ads","Resilia drama-style singing VSLs","LEGO/crochet/cartoon singing ads (Diego_exits, DevidKeule)"],
 [{"claim":"Resilia 'rakes in 14M annually running drama style VSL singing ads'","url":X("OriSilver","2103501563956269161")},
  {"claim":"8.2 ROAS with singing cartoon ads","url":X("Diego_exits","2088560005716836605")},
  {"claim":"9.2 ROAS with cartoon ads","url":X("DevidKeule","2089352262665552294")},
  {"claim":"First singing ad test: 19 cents spend for 2 sales","url":X("moderndayscaler","2103859077612782001")},
  {"claim":"Suno song per script doubles variants (15 to 30 ads)","url":X("alexgoughcooper","2046294017927704607")}],
 "novelty_scroll_stop_ai","moderate","yes","Any product; the song carries benefits and brand recall.",
 "Strong backlash: r/hatethissmug 'these horrible singing ai ads' (Ryze named), r/aislop 'singing AI slop ads' (121 upvotes).")

add("Unboxing",
 "Hands or a creator open the package and reveal the product with close-ups, often with crisp packaging sound.",
 ["X","Reddit","LinkedIn","Web"],10,
 ["Arcads gaming laptop unboxing ad","Flova Apple-style unboxing","AI agent sweater unboxing (r/AI_UGC_Marketing)"],
 [{"claim":"UGC unboxings among dominant TikTok ecommerce formats","url":"https://influee.co/blog/tiktok-ad-formats"},
  {"claim":"AI unboxing $1.40 to 3 per 10 seconds","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"},
  {"claim":"Listed in 11 AI video formats crushing across 200+ winning DTC ads","url":"https://www.linkedin.com/posts/yousifa_ive-tore-apart-200-winning-dtc-ads-these-activity-7510039496156020736-fzqr"}],
 "proven_performance","moderate","yes","Any boxed physical product; best with premium packaging.")

add("ASMR / satisfying product",
 "Close-mic tactile sound and oddly satisfying visuals (pours, crunches, cleaning, cutting, clicks), little or no talking.",
 ["X","Reddit","LinkedIn","Web"],9,
 ["ASMR plus ridiculous foley ad (HireFireTeam)","'Silent review' ASMR format (The Social Savannah)","AI mukbang ASMR ramen ad","Toyota satisfying ad (r/Satisfyingasfuck, 2,252 upvotes)"],
 [{"claim":"ASMR + foley ad took over account with 43% hold rate","url":X("HireFireTeam","1807762698664337743")},
  {"claim":"Motion trends: escapism/satisfying content, soap-crushing account 42M likes","url":"https://motionapp.com/creative-trends"},
  {"claim":"ASMR listed among 37 favourite formats from 50,000+ DTC video ads","url":"https://www.linkedin.com/posts/abramsjake_favorite-creative-formats-activity-7465744981731942401-fxtA"}],
 "proven_performance","moderate","partial","Best for tactile, food, beauty, cleaning products; weaker for products with no sensory moment.")

add("Micro movie / short drama ad",
 "A 30 to 60 second film built on story architecture (character, conflict, payoff) instead of hook-benefit-CTA; includes AI short-drama ads.",
 ["X","Reddit","LinkedIn","Web"],9,
 ["Toyota truck cliff spot (Kyra Richards breakdown)","Marc Jacobs microdrama for the Scene bag","Sparko 'The Empire' germ-board-meeting AI film","Seedance 2.5 multi-cut drama ads"],
 [{"claim":"'2027 will be the year of Micro movie ads' post, 11,671 likes","url":"https://www.linkedin.com/posts/kyraserio_2027-will-be-the-year-of-micro-movie-ads-activity-7505962524463382528-JxSx"},
  {"claim":"Motion masterclass: FB video ads turning into micro movies in 2026 (Sarah Levinger)","url":"https://www.linkedin.com/posts/motion1_how-you-can-make-micro-movies-save-this-activity-7412496767960862720-BO"},
  {"claim":"'Entertainment ads': song ads, drama ads, educational animation dominate top brands","url":X("pounddz","2103086813598408802")},
  {"claim":"Ipsos/Syracuse: AI ads underperform partly because AI attempts storytelling less often","url":"https://www.linkedin.com/posts/lisa-zielinski-570a3a6_in-our-recent-study-with-syracuse-university-activity-74"}],
 "proven_performance","moderate","yes","Any product that can be the payoff of a story.")

add("Skit / comedic scenario",
 "Short scripted or staged comedic scene (often relatable conflict) that introduces the product as the punchline or fix.",
 ["X","Reddit","LinkedIn","Web"],8,
 ["Harmon Brothers-style scripted spots (Squatty Potty, Purple, Poo-Pourri)","Liquid Death 'Deadliest Thing on Earth' ($1,500, 3M views)"],
 [{"claim":"25% of ads spending $1M+ use humor vs 14% of social ads","url":"https://motionapp.com/creative-trends"},
  {"claim":"Skits 'blowing up right now for cold top of the funnel' (1,200+ ads analyzed)","url":R("UGCcreators")+"/comments/1s5tmkf/"},
  {"claim":"Skits listed in $100M-spend winning formats cheat sheet","url":"https://www.linkedin.com/posts/lachezarvoynov_winning-meta-ad-creative-formats-cheat-sheet-activity-7479904514553151488-68VR"}],
 "proven_performance","moderate","yes","Any product with a relatable problem.")

add("Us vs Them / David and Goliath comparison",
 "Split-screen or alternating head-to-head of the product against the category default or big incumbent.",
 ["X","Reddit","LinkedIn","Web"],8,
 ["HiSmile, Ancestral Cosmetics, Tallow Truth (Ours vs Theirs)","'We're Not Cheap' videos (Dara Denney)"],
 [{"claim":"#1 of 5 formats always used across $100M DTC Meta spend","url":"https://www.linkedin.com/posts/curtishowland_ive-spent-100m-on-meta-ads-in-the-dtc-space-activity-7417573805969276928-75Mk"},
  {"claim":"'David & Goliath' videos top performing format across 20,000 ads","url":"https://www.linkedin.com/posts/daradenney_ive-created-20000-ads-heres-whats-converting-activity-7453082218517917696-MNVD"},
  {"claim":"Ours vs Theirs among 8 formats in 1,200+ winning ads","url":R("FacebookAds")+"/comments/1s9hlea/"}],
 "proven_performance","strong","yes","Any product with a clear differentiator vs the old way.")

add("Ugly ad / lo-fi native",
 "Deliberately rough phone footage or low-effort text so it reads as organic content, not an ad.",
 ["X","Reddit","LinkedIn","Web"],8,
 ["Shroom IQ, Norse Organics, 40 Plus & Fabulous (ugly ads)","Blogilates ugly founder videos"],
 [{"claim":"42% of top-spending ads are lo-fi; 53% of advertisers plan more lo-fi","url":"https://motionapp.com/creative-trends"},
  {"claim":"'The less an ad feels like an ad, the better it performs' (25-format ranking)","url":"https://www.linkedin.com/posts/joe-hides_i-just-put-together-a-ranking-of-the-top-activity-7508123370182590464-BxCR"}],
 "proven_performance","strong","yes","Any product.")

add("Zach D Films style 3D explainer",
 "Fast, clay-like 3D animation in second person ('you') that escalates a what-if or shows anatomy/mechanism, then cuts to the product.",
 ["X","Reddit","LinkedIn","Web"],8,
 ["Ridge suitcases sponsored Zack D Films short","Prime Hydration Zack D Films ad (r/ksi, 897 upvotes)"],
 [{"claim":"A tier: 'second person escalation, best for problems that compound'","url":X("CEO_Vlad","2096569603761827953")},
  {"claim":"Channel has 28.6M subscribers; Upwork/Fiverr jobs for ZDF-style ads","url":"https://www.upwork.com/freelance-jobs/apply/Animator-Video-Editor-for-Zack-Films-Style-Ads_~022034006309696494168/"},
  {"claim":"'Anatomical product animations' in 11 AI formats crushing","url":"https://www.linkedin.com/posts/yousifa_ive-tore-apart-200-winning-dtc-ads-these-activity-7510039496156020736-fzqr"}],
 "novelty_scroll_stop_ai","moderate","partial","Best when there is a hidden mechanism (body, sleep, digestion, materials); weaker for pure aesthetic products.")

add("Craft and toy material animation (felt, crochet, LEGO, plush, paper craft, doll)",
 "The same animated story rendered in a tactile material world: felt stop-motion, crochet, brick toys, plush, paper cutout, plastic doll, diorama.",
 ["X","Reddit","LinkedIn","Web"],8,
 ["feltmation and crochet prompt docs (adswithcami)","LEGO/crochet singing ads (Diego_exits)"],
 [{"claim":"Style list: Pixar, cartoon, flat 2D, claymation, plush/toy, felt stop motion, paper craft, plastic doll, Lego, diorama (452 likes)","url":"https://www.linkedin.com/posts/alexgoughcooper_ai-animation-ad-styles-activity-7457783748747624448-oHv9"},
  {"claim":"3 angles x 5 styles = 15 ads; cartoon styles keep the 'AI slop detector quiet'","url":"https://www.linkedin.com/posts/yousifa_these-cartoon-style-ads-are-making-literal-activity-7509677157552398336-n-wl"}],
 "novelty_scroll_stop_ai","anecdotal","yes","Any product; mainly a variety lever on a winning animated script.")

add("Absurdist / brainrot / high-dopamine AI hook",
 "Rapid-fire impossible or unhinged scenes (floating in eggs, alien chugging beer, hybrid creatures) that grab attention before the product lands.",
 ["X","Reddit","LinkedIn","Web"],9,
 ["Kalshi NBA Finals spot by PJ Accetturo (Veo 3, under $2,000)","Italian brainrot brand content (Ryanair; KFC backlash)","stretch-jeans backflip Sora ad (Alex Cooper)"],
 [{"claim":"Kalshi ad: about 18M impressions in 48 hours, 20M+ total, under $2,000","url":"https://www.npr.org/2025/06/23/nx-s1-5432712/ai-video-ad-kalshi-advertising-nba-finals"},
  {"claim":"Kalshi launch post 1.14M views","url":X("PJaccetturo","1932893260399456513")},
  {"claim":"Caveat: pulls views not necessarily buyers; use as a 3s hook","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"},
  {"claim":"Motion trend: absurdity/brain rot lowers cognitive load","url":"https://motionapp.com/creative-trends"}],
 "novelty_scroll_stop_ai","moderate","yes","Any product as a hook; the body still has to sell.")

add("Talking objects / anthropomorphic everyday items",
 "Everyday objects or foods become talking characters (a fryer complaining, a banana explaining digestion) placed in real-looking scenes.",
 ["X","Reddit","LinkedIn"],7,
 ["fryer, grape, banana, sun, lightbulb health-hack characters (AlessandroLavis, davidfigeira)"],
 [{"claim":"'$150k+/month content systems' built on object characters","url":X("AlessandroLavis","2022264096318525834")},
  {"claim":"'$80k+/month ad accounts are quietly testing animated object formats'","url":X("davidfigeira","2031338896605286598")},
  {"claim":"Backlash: 'I hate AI animated objects in ads... these ads are EVERYWHERE'","url":R("hatethissmug")+"/comments/1vxdyj6/"}],
 "novelty_scroll_stop_ai","anecdotal","yes","Any product; the product or the problem itself can talk.")

add("Native text formats in video (iMessage, Notes app, Reddit post, tweet, sticky note)",
 "The ad is a screen of a text thread, notes list, forum post or sticky note, animated or filmed, so it reads as a recommendation between friends.",
 ["X","Reddit","LinkedIn","Web"],7,
 ["Spacegoods, Eleat, Life Cykel text-message ads","sticky-note UGC cloned with Nano Banana + Seedance"],
 [{"claim":"Text-message format 'consistently outperforms polished creatives by 2 to 3x on CTR' (commenter, supplement brands)","url":R("FacebookAds")+"/comments/1s9hlea/"},
  {"claim":"Text overlays + iMessage convos in list of formats top brands run","url":X("FynCas","1949502399451689237")}],
 "proven_performance","moderate","yes","Any product.")

add("Before / after transformation",
 "Two matched scenes (same framing and light) showing the problem state and the result state.",
 ["X","Reddit","LinkedIn","Web"],7,["Transformation ads ('what happens to X if you take Y for N days')"],
 [{"claim":"A tier (statics)","url":X("ChelalaPierre1","2103088143138193657")},
  {"claim":"Transformation UGC converts best for brands selling outcomes","url":"https://adlibrary.com/posts/best-dtc-meta-ads-examples-2026"}],
 "proven_performance","strong","partial","Needs a visible change (skin, cleaning, fitness, home); policy risk in skincare and weight loss.")

add("Product demo (show it working)",
 "20 to 40 seconds of the product in action, often no voiceover, sometimes POV hands only.",
 ["X","LinkedIn","Web"],7,["multi-scene demo (CEO_Vlad A tier)"],
 [{"claim":"One of 5 formats always used across $100M spend","url":"https://www.linkedin.com/posts/curtishowland_ive-spent-100m-on-meta-ads-in-the-dtc-space-activity-7417573805969276928-75Mk"},
  {"claim":"POV hands demo is the 'AI-friendliest format', $5 to 15 per demo","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"}],
 "proven_performance","strong","yes","Any product with a visible function.")

add("VSL / advertorial story video",
 "60 seconds to several minutes of education-through-story (history, mechanism, villain) with the product revealed late.",
 ["X","LinkedIn","Web"],7,
 ["The Black Stuff soap advertorial (2,000 years of leatherworking story)","Harmon Brothers (Squatty Potty, Purple, Poo-Pourri)","grounding product podcast VSL"],
 [{"claim":"5+ minute VSLs and 2 to 4 minute Pixar doctor AI VSLs in $100M-spend cheat sheet","url":"https://www.linkedin.com/posts/lachezarvoynov_winning-meta-ad-creative-formats-cheat-sheet-activity-7479904514553151488-68VR"},
  {"claim":"Advertorial-style video 'one of the better formats we're seeing right now'","url":X("sourfraser","2102401597879816679")},
  {"claim":"Long-form educational (40 to 50s+) gaining spend","url":"https://motionapp.com/creative-trends"}],
 "proven_performance","moderate","partial","Best for considered or 'weird' products that need belief building.")

add("CGI product hero / FOOH (fake out of home)",
 "Hyper-real CGI puts a giant or impossible version of the product into a real city (buses getting mascara, bags driving through Paris).",
 ["LinkedIn","Web","X","Reddit"],7,
 ["Maybelline mascara bus/tube","Jacquemus Le Bambino bags on cars","Nykaa sneakers portal at Gateway of India","Apple Vertex CGI NYC weather"],
 [{"claim":"Maybelline: 12M views in hours, 76M total","url":"https://www.marketingbrew.com/stories/2023/10/26/why-some-brands-are-embracing-fake-out-of-home"},
  {"claim":"Critic: fake OOH CGI ads 2 years on, 'probably costing £15k upwards for minimal impact'","url":"https://www.linkedin.com/posts/rich-johnson-84a0b51a_somewhere-in-an-alternate-universe-a-marketing-activity-7"},
  {"claim":"Academic study on engagement in TikTok #FOOH content accepted for 2027","url":"https://www.linkedin.com/posts/delchiappa_fooh-fooh-activity-7480512192635789312-rRel"}],
 "novelty_scroll_stop_ai","moderate","yes","Any product with an iconic shape or packaging.",
 "Brand-awareness format; almost no direct-response evidence.")

add("Anime / manga style",
 "Japanese-animation look: cel shading, speed lines, dramatic framing, sometimes manga panels animated.",
 ["X","Reddit","LinkedIn","Web"],8,
 ["World Cup anime fan video, 4M+ views (Deykhan Ten)","Seedance 2.0 manga-panel to anime (Varun Mayya)","Mochi.tv AI anime shorts (YC)"],
 [{"claim":"Anime listed among AI animation ad styles in multiple workflow posts (Mho_23, mikefutia, spwfeijen)","url":X("Mho_23","2071293386724982947")},
  {"claim":"AI anime ad generators marketed to brands","url":"https://www.pippit.ai/blog/ai-anime/what-is-ai-anime-ad-generator"}],
 "novelty_scroll_stop_ai","anecdotal","partial","Works for youth, gaming, streetwear, snacks, gadgets; brand-fit risk for premium or older audiences.",
 "No DTC performance numbers found; Reddit mentions are mostly complaints about AI anime app ads.")

add("Yapper ad (unscripted creator rant)",
 "A charismatic creator talks loosely and fast about a problem or product with minimal editing.",
 ["X","LinkedIn"],4,[],
 [{"claim":"Yapper ads top format in multiple accounts","url":"https://www.linkedin.com/posts/alexgoughcooper_yappers-are-the-top-ad-format-in-multiple-activity-7434968393566445569-tR9N"},
  {"claim":"'one of the last islands' AI cannot fake (575 likes)","url":"https://www.linkedin.com/posts/daradenney_the-latest-trend-in-creator-content-for-activity-7460297912896458753"},
  {"claim":"S tier ecom format","url":X("ChelalaPierre1","2103088143138193657")}],
 "proven_performance","strong","yes","Any product; depends on creator casting.")

add("Green screen reaction / reply-to-comment",
 "Creator appears over a screenshot, article, comment or a proven winning ad and reacts or answers the objection.",
 ["X","Reddit","LinkedIn","Web"],6,[],
 [{"claim":"A tier: green screen reactions over a proven winner","url":X("ChelalaPierre1","2103088143138193657")},
  {"claim":"Reply-to-comment ad $2 to 11 per video","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"},
  {"claim":"Green screen meme format automatable 'for pennies'","url":X("_mattwelter","1878104250560946482")}],
 "proven_performance","moderate","yes","Any product.")

add("Listicle video ('3 reasons why')",
 "Numbered reasons or signs, each segment its own mini hook, voiceover or creator delivered.",
 ["X","LinkedIn","Web"],5,[],
 [{"claim":"Listicle videos among top formats across 20,000 ads","url":"https://www.linkedin.com/posts/daradenney_ive-created-20000-ads-heres-whats-converting-activity-7453082218517917696-MNVD"},
  {"claim":"'Reasons why' one of 5 ads across $100M spend","url":"https://www.linkedin.com/posts/curtishowland_ive-spent-100m-on-meta-ads-in-the-dtc-space-activity-7417573805969276928-75Mk"}],
 "proven_performance","strong","yes","Any product.")

add("Problem / solution (problem agitation)",
 "Open on a specific pain, agitate for a couple of seconds, flip to the product as the fix; under 30 seconds.",
 ["X","Reddit","LinkedIn","Web"],6,[],
 [{"claim":"'highest-performing cold-traffic format for DTC brands in most verticals'","url":"https://adlibrary.com/posts/best-dtc-meta-ads-examples-2026"},
  {"claim":"One of 5 formats across $100M spend","url":"https://www.linkedin.com/posts/curtishowland_ive-spent-100m-on-meta-ads-in-the-dtc-space-activity-7417573805969276928-75Mk"}],
 "proven_performance","strong","yes","Any problem-solving product.")

add("POV / first-person",
 "Camera is the viewer's eyes ('POV: you finally...'), hands and point of view, no face.",
 ["X","LinkedIn","Web"],5,["pastel earbuds Japanese cut-scene POV ad (ShamiWeb3)"],
 [{"claim":"First-person/POV content named a Motion creative trend","url":"https://motionapp.com/creative-trends"},
  {"claim":"Warning: 12 audited brands ran the same 'POV: you just found out about [product]' opening 47 times","url":"https://www.linkedin.com/posts/nishant-parmar-92b528305_dtc-ecommerce-creativestrategy-activity-75056772691773"}],
 "proven_performance","moderate","yes","Any product.")

add("Day in the life / GRWM / routine vlog",
 "The product woven into a morning routine, get-ready-with-me or vlog-style day, often a recurring persona.",
 ["X","LinkedIn","Web"],6,["'GRWM in Tokyo, Harajuku vibes' AI earbuds ad went viral (ShamiWeb3)","AI persona day-in-the-life account earning $11k/mo (framexin)"],
 [{"claim":"Car POVs + GRWM and day-in-the-life hooks in list of formats top brands run","url":X("FynCas","1949502399451689237")},
  {"claim":"Vlog and native lifestyle in 37-format master list","url":"https://www.linkedin.com/posts/abramsjake_favorite-creative-formats-activity-7465744981731942401-fxtA"}],
 "proven_performance","moderate","partial","Best for daily-use products (beauty, wearables, food, wellness).")

add("Tutorial / hack",
 "The product is the payoff of a useful trick or how-to ('hack I wish I knew sooner').",
 ["X","LinkedIn","Web"],4,[],
 [{"claim":"Tutorial & hack: low sales pressure, excellent on cold audiences","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"},
  {"claim":"Higgsfield 'Tutorial' preset among 9 ad styles","url":X("higgsfield","2044163123268177929")}],
 "proven_performance","moderate","partial","Needs a use case that can be taught.")

add("Fake news report / breaking news",
 "Anchor, lower-thirds and breaking-news UI present the product as a news story or 'as featured on' moment.",
 ["X","Reddit","Web"],4,[],
 [{"claim":"Fake news-style ads in list of formats top brands run","url":X("FynCas","1949502399451689237")},
  {"claim":"'Brand just got featured on' authority hook (1,200+ ads analyzed)","url":R("UGCcreators")+"/comments/1s5tmkf/"},
  {"claim":"Fake news anchor $11 to 15 per video; must stay obvious parody","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"}],
 "proven_performance","anecdotal","yes","Any product; keep it parody to avoid deception.")

add("Meme ad",
 "A known meme template repurposed around the product or the problem.",
 ["X","Reddit","LinkedIn","Web"],6,["Olipop, Spot and Tango, EveryPlate"],
 [{"claim":"Meme ads among 8 formats in 1,200+ winning ads","url":R("FacebookAds")+"/comments/1s9hlea/"},
  {"claim":"Ranked C tier","url":X("ChelalaPierre1","2103088143138193657")}],
 "proven_performance","moderate","yes","Any product; short shelf life.")

add("Miniature / diorama / tilt-shift world",
 "Toy-sized sets and tilt-shift blur make the product world look like a miniature model.",
 ["X","LinkedIn","Web"],5,["Airbnb stylized miniature diorama spots into 2026"],
 [{"claim":"Airbnb diorama spots polished enough that viewers debated if they were AI","url":"https://shhots.ai/blog/best-ai-commercials/"},
  {"claim":"Miniature tilt-shift AI video 'one of the fastest-growing formats on Instagram and YouTube'","url":"https://www.lvprompts.com/2026/07/diorama-free-ai-prompt-generator-for.html"}],
 "novelty_scroll_stop_ai","anecdotal","yes","Any product as a hero in a tiny world.")

add("Wes Anderson symmetric pastel",
 "Centered symmetric frames, pastel palette, deadpan narration and chapter cards.",
 ["X","Web"],6,["Prada Wes Anderson short (fan anticipation)","Ava Williams train TikTok, 13M views, 180k videos on the audio"],
 [{"claim":"Wes Anderson miniature listed in one-workflow AI animation ad styles","url":X("mikefutia","2040101348621095173")},
  {"claim":"Trend origin 13M views","url":"https://www.creativebloq.com/news/wes-anderson-tiktok"}],
 "novelty_scroll_stop_ai","anecdotal","yes","Any product; brand-aesthetic play.")

add("Retro VHS / 90s infomercial / nostalgia",
 "Degraded VHS look, 90s infomercial or 'As Seen On TV' parody, or Y2K nostalgia styling.",
 ["X","Reddit","Web"],5,["Poppi Y2K Super Bowl ad","90s POV-ray infomercial parody (re_skob, 113k views)"],
 [{"claim":"Poppi nostalgia campaign: 100x search, 10x Amazon sales, 250% IG engagement","url":"https://motionapp.com/creative-trends"},
  {"claim":"Retro cartoon and synthwave in AI animation ad style lists","url":X("mikefutia","2040101348621095173")}],
 "novelty_scroll_stop_ai","anecdotal","yes","Any product; parody tone suits gadgets and household goods.")

add("GTA / video game parody",
 "The ad is styled as open-world game footage or game UI, with missions and HUD.",
 ["X","Reddit"],4,["Kalshi 'GTA-style madness' NBA Finals spot","Whop GTA style ad (beechinour)"],
 [{"claim":"GTA-style ad for Whop 'generated millions of views'","url":X("beechinour","1988701882446176505")}],
 "novelty_scroll_stop_ai","anecdotal","partial","Best for youth, gaming-adjacent and male audiences.")

add("Pain point visualization ('make the invisible visible')",
 "Visceral AI visuals of the problem (shin splints cracking, bloated gut inflating) before the product fix.",
 ["LinkedIn","X"],3,["stretch jeans, running shoes, bloat relief concepts (Alex Cooper)"],
 [{"claim":"Best Sora outputs were unrealistic pain-point visuals","url":"https://www.linkedin.com/posts/alexgoughcooper_ive-spent-20-hours-making-ads-with-sora-activity-7391123251642482688-2m74"}],
 "novelty_scroll_stop_ai","anecdotal","partial","Best for problem-solving products (health, comfort, cleaning).")

add("Virtual try-on",
 "The product worn or used by many generated body types and settings without a shoot.",
 ["X","LinkedIn","Web"],4,["Higgsfield 'Virtual Try On' preset"],
 [{"claim":"Try-on videos without a model in 11 AI formats crushing","url":"https://www.linkedin.com/posts/yousifa_ive-tore-apart-200-winning-dtc-ads-these-activity-7510039496156020736-fzqr"}],
 "proven_performance","moderate","no","Only wearables (fashion, jewelry, eyewear, accessories).")

add("Expert explainer",
 "A doctor, specialist or credentialed person explains the mechanism; also AI 'doctor' characters.",
 ["Reddit","LinkedIn","Web"],4,["MUD\\WTR, Fulton Insoles, Jolie expert hooks"],
 [{"claim":"Expert angle one of 19 hooks in 10,000+ top video ads","url":R("FacebookAds")+"/comments/1rw5ufs/"},
  {"claim":"Oren John: 'the new mid funnel is expert storytelling'","url":"https://www.linkedin.com/posts/motion1_oren-john-value-content-is-commodified-activity-7436754533252263936-tGXH"}],
 "proven_performance","moderate","partial","Needs a mechanism an expert can credibly explain.")

add("In-car talking head",
 "Creator talks from the driver's seat, reads as private and unscripted.",
 ["X"],2,[],
 [{"claim":"S tier: 'reads as private and unscripted and is the CHEAPEST to render well'","url":X("CEO_Vlad","2096569603761827953")}],
 "proven_performance","anecdotal","yes","Any product.")

add("Hidden camera / doorbell cam hook",
 "Opens as security, doorbell or hidden-camera footage for voyeuristic realism.",
 ["LinkedIn","X"],2,[],
 [{"claim":"Hidden camera and doorcam hooks seen on the Sora feed, being tested","url":"https://www.linkedin.com/posts/alexgoughcooper_ive-spent-20-hours-making-ads-with-sora-activity-7391123251642482688-2m74"}],
 "novelty_scroll_stop_ai","anecdotal","partial","Works as a hook for home, pet, security, delivery-moment products.")

add("Mashup (AI plus real)",
 "Fast edit chaining UGC clips, AI shots and b-roll into re-hooking sequences with no linear narrative.",
 ["LinkedIn","Web"],3,[],
 [{"claim":"'AI + Real Mashup' in 37-format list","url":"https://www.linkedin.com/posts/abramsjake_favorite-creative-formats-activity-7465744981731942401-fxtA"},
  {"claim":"Mashup $3 to 10 generation cost","url":"https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/"}],
 "proven_performance","anecdotal","yes","Any product.")

# score
w={"strong":6,"moderate":3,"contested":2,"anecdotal":0}
for s in S:
    s["evidence_score"]=s["independent_mentions"]+3*len(s["sources"])+w[s["performance_signal"]]
S.sort(key=lambda s:-s["evidence_score"])
for i,s in enumerate(S,1): s["rank"]=i
txt=json.dumps(S,indent=1,ensure_ascii=False)
assert not re.search("[–—]",txt), "dash found"
open("/Users/farooq.chisty/claude fc/magicfit-video-templates/research/social_web_styles.json","w").write(txt)
for s in S[:25]: print(s["rank"],s["evidence_score"],s["independent_mentions"],"/".join(s["sources"]),s["format_type"],s["performance_signal"],"|",s["style"])
print(len(S))
