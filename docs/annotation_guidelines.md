# Annotation Guidelines - A reference for the manual annotation

This document captures the methodological record of the annotation process: every refinement and choice made while annotating the gold-standard corpus.



## 1. The five entity categories

| Category | Definition | Typical words |
|---|---|---|
| **FLORA** | Individual plants, trees, flowers, or vegetation | tree, oak, flower, moss, grove, foliage |
| **FAUNA** | Animals, birds, insects — literal, non-human creatures | albatross, bird, snake |
| **WEATHER** | Weather, atmospherical and celestial phenomena | wind, storm, rain, cloud, ice, sun, moon, stars, sky |
| **LANDSCAPE** | Topographic / geological features, including named places | river, mountain, glacier, lake, rock, Mont Blanc, the Jungfrau |
| **NATURE** | Personified nature-as-a-unified-force - abstract address, a named spirit-character, *or* an animating force described without either the word "Nature" or a character-name | "Nature, thou great and unconquerable force..."; "the Witch of the Alps" |

Four concrete categories plus NATURE for personification, since agency
is the project's central question.



## 2. What counts as a mention (span rules)

- **Tag the head noun.** For "the frozen lake," tag only `lake`, not the full noun phrase — this keeps spans consistent for a machine learning model to learn from.
- **Proper/compound names stay together.** "Mont Blanc", "Lake Leman", "the West Wind" are tagged as one span, since they function as a single named entity.
- **One tag per mention**, even if a pronoun refers back to it later in the sentence ("the river... it glideth" → tag "river" only; don't tag "it"). **But a fresh full noun-phrase in a new clause gets its own tag**, even referring to the same underlying entity as an earlier mention — the rule only exempts bare pronouns (it/he/she/thou), not repeated naming.
- **Generic vs. specific mentions are not distinguished.** "the trees" and "an oak" are both tagged FLORA — no special sub-marking needed.
- **Only tag nouns, never verbs** — even when clearly derived from nature vocabulary. "Melancholy **clouded** every thought" → no tag.
- **"X of Y" — composition vs. one combined span.** Test: does X remain
  independently, specifically meaningful *without* Y?
  - **Yes → tag both** (composition): "caves **of** ice," "icy wall **of** the glacier," "summits **of** the mountains" — X already names something real and specific on its own.
  - **No → tag as ONE span**: "**skeletons of** leaves," "**sea of** ice" (proper name for the Mer de Glace), "**dome of** air" — X is an empty shape that only becomes a concrete image once combined with Y.
- **Possessive compounds ("[entity]'s [word]") — one combined span vs. excluded attribute vs. split composition:**
  - **One combined span** when the possessed word is conventionalized locative/anatomical vocabulary functioning as real location-naming, or a substantive component actively doing work: "**mountain's head**" (= summit), "**torrent's brink**", "**Sun's rim**".
  - **Excluded entirely** when the possessed word is purely decorative personification with no substantive content: wilderness's "**tongue**", the Cloud's "**wings**", "**Sun's throne**" -> Tag only the possessor.
  - **Split as composition** when both halves are already independently, robustly real entities elsewhere in the corpus: "summit**s of** the mountains," "torrent's **stream**" (contrast: excluded when brief/decorative — "the tempest's stream" — but tagged when substantive and structural to a whole passage — "on whose **stream**, mid the steep sky's commotion" opens an entire stanza).
  - **Intensity/manner descriptors stay excluded**, regardless of grammar: "**roar** of torrents," "**thunder** sound of the avalanche," "pouring in **torrents**" (idiom for "heavily") — these describe volume/intensity, not a second entity.
- **Reduplicative idioms are one mention.** "From **peak** to peak," "from **steep** to steep" → tag once (one adverbial unit meaning "extensively"), not twice.
- **"[Being] of [domain1] AND [domain2]" = one epithet.** "Daughter of Earth and Water" → one NATURE span. **"[Being1] OR [Being2]" = two separate tags**, since "or" presents alternative possible identities, not one composite being: "Teach us, Sprite **or** Bird" → `Sprite` (NATURE) + `Bird` (FAUNA), each its own row.
- **Real anatomy of an already-tagged FLORA/FAUNA entity is tagged normally**, distinct from borrowed/decorative personification: a pine's "trunk" (real, composition, like "caves of ice"), an eagle's own "wings" (its real anatomy) — vs. wilderness's borrowed "tongue" (excluded).



## 3. Boundary rules — the hard cases

These are the calls that will actually vary between annotators. To keep data consistent, use this table as a source of truth during the pilot.

| Case | Decision | Example |
|---|---|---|
| **Named landscape features** | LANDSCAPE, even proper nouns WordNet won't recognize | "Mont Blanc", "Arveiron", "Jura" |
| **Sun/moon/stars** | Tag as WEATHER (not a separate CELESTIAL category) | "the horned Moon", "the Sun came up" |
| **Direct address to a *concrete* entity** | Tag by its own concrete category — **not** NATURE, even in a poem that also personifies an abstract Power nearby | "thou fresh breaking Day" → WEATHER |
| **Personification that explicitly names its plain referent** | Stays in its concrete category — the naming bridges the personification back to a literal thing | *"that orbed maiden... **whom mortals call the Moon**"* → WEATHER, not NATURE |
| **Personification that never names a plain referent** | Functions as an independent character → NATURE | "**mother**'s breast... **she** dances about the sun" (never says "Earth") → NATURE |
| **Personified spirit-characters, generally** | Tag as NATURE whenever named/clearly the subject — confirmed across multiple texts independently | "the Spirits whose presence I command", "the everlasting **universe of things** flows through the mind" |
| **Same abstract force elaborated cumulatively across many appositive restatements** | Tag once at first naming — UNLESS a later restatement independently clears the domain-test on its own separate merits, in which case tag it too | "a presence... a sense sublime... a motion and a **spirit**, that impels" → `presence` + `spirit`, both tagged, since "spirit" independently qualifies |
| **A soul/mind/light word used purely psychologically (human interiority), even with spatial/dwelling vocabulary** | Do NOT tag | "thy memory be as a **dwelling-place** for all sweet sounds" (metaphor for memory, not a real place) — contrast "**fountain-dwellings**" (a real historical place, the springs at Gadara) → tagged |
| **"Spirit(s)" — domain test** | Tag NATURE only if (a) a concrete natural domain is identifiable, or (b) it functions as an abstract address to Nature itself. Generic religious/moral "spirit" satisfies neither | "blithe Spirit" → NATURE (path b); "spirit, good or evil" → not tagged |
| **"[Being] of [domain]" epithets** | Tag the whole epithet as one NATURE span | "Daughter of Air!" → `Daughter of Air`, not "Air" alone |
| **"Nature" — sense test, not agency test** | Tag whenever it refers to the natural world as a domain, regardless of capitalization or grammatical role — including passive uses. Do NOT tag when used in an unrelated sense (human nature, "by nature" = inherently) | "with nature reconciled" → tag, NATURE (passive role, but still refers to the natural world); "it is in his nature to lie" → don't tag (unrelated sense) |
| **"Mother Earth" / "Earth" as addressee** | LANDSCAPE if it clearly means the ground; NATURE if functioning as an abstract force | "My mother Earth!" → borderline, default LANDSCAPE; contrast "this **green earth**, on which I gaze" (Mont Blanc) — unambiguous LANDSCAPE, since it's literally the observed ground beneath him, not addressed or invoked as a force |
| **"Mother Earth" / "Earth" as addressee** | LANDSCAPE — direct address to a concrete entity stays in its own category; NATURE only if genuinely described with pantheistic agentive verbs (contrast the "presence"/"the god" rule) | "My mother Earth! And thou fresh breaking Day, and you, ye Mountains" → all three stay in their concrete categories; contrast "this **green earth**, on which I gaze" (Mont Blanc), also unambiguous LANDSCAPE |
| **Abstract personified quality/process (Death, Decay, Destruction) with no natural domain** | Do NOT tag, even capitalized and agentive | "Destruction's splinters" → `splinters` tagged LANDSCAPE, "Destruction" itself excluded |
| **Wood/stone as material, not entity** | Do NOT tag | "a wooden door" |
| **"X is a Y" declarative equation between two different concrete things** | Judgment call — tag both if each contributes distinct information | "the **mountain** is a bare perpendicular **rock**" |
| **"Fire" — elemental vs. literal** | Tag when functioning as one of the classical four elements, paired with or implying earth/air/water. Ordinary combustion fire (mood-metaphor, a hearth, a burning building) stays excluded | "with hurricane, fire, and snow" (*The Cloud*, paired with weather-elements) → tag; "The one was fire and fickleness" (*Manfred*, mood metaphor, no elemental framework) → don't tag |

**General rule when still unsure:** tag it and leave a note in the `notes` column, rather than silently skipping it.



## 4. The figurative flag

Every tagged span gets `is_figurative`:
- **FALSE** — the entity is literally present/referenced in the scene ("the albatross followed the ship")
- **TRUE** — the entity is invoked only as a comparison, not literally present ("he wandered like a wolf")

The hard cases:

| Case | Decision | Example |
|---|---|---|
| **Similes/metaphors (explicit "like/as")** | Tag, `TRUE` | "he wandered like a wolf" |
| **Real nature-word as metaphor vehicle, no explicit "like/as" needed** | Still `TRUE`, if reinforced by supporting vocabulary keeping the literal sense active | "a spring of love **gushed**" |
| **Entity literally present but described unusually / perceived strangely** | Still `FALSE` — personification or distorted perception isn't substitution | "the mountains whirl spinning around me" |
| **Entity appears inside a dream** | Still `FALSE` — not the same axis as figurative | "I dreamt... filled with dew" |
| **Negated existence** | Still tag, still `FALSE` | "nor shapes of men nor beasts we ken" |
| **Negated identity-claim** | Also tag, `FALSE` | "Bird thou never wert" |



## 5. Abstract and idiomatic uses - "don't tag" principles

**Test: is something actually present and being described, or is the word doing idiomatic, classificatory or relational work with no scene pictured?**

- **Idioms for death/burial**: "the **grave** closed between us", "a fitting **tomb**".
- **Mood-words sharing vocabulary with weather, but not invoking it**: "dark **gloom**".
- **Purely optical/relational/perceptual concepts**: horizon, shadow, depth (abstract).
- **Territorial/administrative references**: land, climes, regions, latitude.
- **Color/texture-comparators using mineral/gem names, where nothing is depicted**: "as green as **emerald**", "yellow as **gold**". (Contrast "ribbed **sea-sand**" — tagged, since shore/beach are legitimate LANDSCAPE members.)
- **"Creature" and man/mankind/world/human/person/people** — almost always a human being, never FAUNA.
- **Attributive/classifying place-names or trade-names**: "a **Greenland** whaler", "the **whale**-fishing".
- **Aspiration/state-of-mind words borrowing spatial vocabulary**: "a **paradise** of my own creation."
- **Conventionalized dead metaphors with no reinforcing physical imagery**: "the **channel** of their earlier bent" (contrast "live" metaphors like spring, which keep the literal sense active via a supporting verb).
- **Lowercase, generic abstract nouns unrelated to the literal sense**: "the **power** of elevating his soul".
- **Purely human/philosophical vocabulary sharing a root with a nature word**: "all the **sages** can".



## 6. Known automatic-detection gaps

The `annotation.ipynb` notebook pre-selects sentences using a WordNet-based candidate lexicon, plus a keyword boost for capitalised "Nature." Both are heuristics, not ground truth:

**Wrong-sense matches** — check context: **sound** (strait, not noise), **head** (a head of cattle), **side** (a slope), **breath** (a slight wind, not respiration), **sweat** (condensation, not perspiration), **halo** (an atmospheric ring, not religious iconography), **recess** (an inlet, not an abstract retreat), **draught** (a current of air, not a drink), **fly** (insect noun vs. verb).

**Poetic/inverted syntax can fool the POS tagger**: a list-like line such as "Rocks, caves, lakes, fens..." may score artificially low because spaCy mis-tags some of those nouns as verbs. This is due to the fact that poetic syntax often tricks the automated tagger. Periodically check band_0 sentences in nature-heavy poems to ensure valid entities weren't missed.

**A fixed bug worth knowing about**: excluding human-referring words (to stop "man" from matching FAUNA) accidentally also excluded "star" via an unrelated "actor" sense. Fixed in the pipeline.



## 7. How to fill out the annotation CSV

- **Never annotate directly in `annotation_pool.csv`.** Work in a separate copy (e.g. `manual_annotation.csv`) — the pooling notebook refuses to overwrite `annotation_pool.csv` if it exists, but that only protects a file you aren't actively editing.
- **Don't edit `band`, `n_candidates`, or `candidate_words`** — provenance record of the automated pre-filter, useful for quantifying its accuracy later.
- **Duplicate the whole row**: one must create one row per entity mention, not per sentence, copying `sentence_id`/`sentence_text` exactly, for multi-entity sentences.

Fill out the blank target columns as follows:
- `target_span`: The exact text of the mention (e.g., "Albatross"), it must match the source text exactly (case-sensitive).
- `start_char` and `end_char`: They will be generated automatically once annotation is complete.
- `entity_type`: The category label (FLORA, FAUNA, WEATHER, LANDSCAPE, or NATURE).
- `is_figurative`: TRUE if it is a simile/metaphor, FALSE if literal.
- `lemma`: The root form of the target span.
- `notes`: Optional but useful for clarifying the reasons behind a tag.



## 8. Examples from the corpus

> *"The Ice was here, the Ice was there... It crack'd and growl'd"* → `Ice` × WEATHER/FALSE, each mention separate

> *"Clear, placid Leman! thy contrasted lake"* → `Leman` × LANDSCAPE only (apposition)

> *"The sea, or rather the vast river of ice"* → `sea` × LANDSCAPE + `river of ice` × LANDSCAPE, both tagged (self-correction, two distinct images)

> *"I have wandered here many days; the caves of ice"* → `caves` × LANDSCAPE, `ice` × WEATHER (composition)

> *"Skeletons of leaves that lag my forest-brook along"* → `skeletons of leaves` × FLORA, one span (X empty without Y)

> *"The sun above the mountain's head"* → `sun` × WEATHER, `mountain's head` × LANDSCAPE, one span (conventionalized locative)

> *"A presence that disturbs me... a motion and a spirit, that impels"* → `presence` × NATURE + `spirit` × NATURE, both tagged

> *"Daughter of Air!"* / *"Teach us, Sprite or Bird"* → `Daughter of Air` one NATURE span (and); `Sprite`/`Bird` two separate tags (or)

> *"The mountains whirl spinning around me"* → `mountains` × LANDSCAPE/FALSE (real entity, distorted perception)

> *"An age of years all winters"* → `winters` × WEATHER/TRUE

> *"Nor shapes of men nor beasts we ken"* → `beasts` × FAUNA/FALSE (negation still counts)

> *"With hurricane, fire, and snow"* vs. *"the one was fire and fickleness"* → `fire` tagged in the first (elemental), excluded in the second (mood metaphor)