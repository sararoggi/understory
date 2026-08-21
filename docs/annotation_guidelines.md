# Annotation Guidelines - A reference for the manual annotation


## 1. The five entity categories

| Category | Definition | Typical words |
|---|---|---|
| **FLORA** | Individual plants, trees, flowers, or vegetation as a mass (woods, foliage) | tree, oak, flower, moss, grove, foliage |
| **FAUNA** | Animals, birds, insects — literal, non-human creatures | albatross, bird, snake |
| **WEATHER** | Weather, atmospherical and celestial phenomena | wind, storm, rain, cloud, ice, sun, moon, stars, sky |
| **LANDSCAPE** | Topographic / geological features, including named places | river, mountain, glacier, lake, rock, Mont Blanc, the Jungfrau |
| **NATURE** | Personified nature-as-a-unified-force. Covers both abstract address ("Nature, thou...") **and** nature manifested as a character (e.g. the Witch of the Alps in Manfred) — same underlying phenomenon, two literary devices. Not limited to the literal word "Nature": "Mother Earth," "the great Power," or a pronoun clearly referring to personified nature all qualify | "Nature, thou great and unconquerable force..."; "the Witch of the Alps" |

Four concrete categories plus NATURE for the abstract personification, since that's central to the agency question this project is actually asking.



## 2. What counts as a mention (span rules)

- **Tag the head noun.** For "the frozen lake," tag only `lake`, not the full noun phrase — this keeps spans consistent for a machine learning model to learn from.
- **Exception — proper/compound names stay together.** "Mont Blanc", "Lake Leman", "the West Wind" are tagged as one span, since they function as a single named entity.
- **One tag per mention**, even if a pronoun refers back to it later in the sentence ("the river... it glideth" → tag "river" only; don't tag "it").
- **Generic vs. specific mentions are not distinguished.** "the trees" and "an oak" are both tagged FLORA — no special sub-marking needed.
- **Only tag nouns, never verbs** — even when clearly derived from nature vocabulary. "Melancholy **clouded** every thought" → no tag.
- **Compound nouns joined by "of" — composition vs. apposition:**
  - **Composition** (two genuinely different physical things, one made of/covered in the other) → tag **both**. "caves **of ice**" → `caves` (LANDSCAPE) + `ice` (WEATHER).
  - **Apposition** (a second phrase renaming the same single referent) → tag **once**. "Clear, placid **Leman**! thy contrasted **lake**" → tag only `Leman`.
  - Test: does removing one noun change what's depicted, or just remove a second label for the same thing?
- **Reduplicative idioms are one mention, not several.** "From **peak** to peak," "from **steep** to steep" → tag once (one adverbial unit meaning "extensively"), not twice.
- **Body-part / attribute words used to personify an already-tagged entity are not separately tagged.** Wilderness's "mysterious **tongue**," the Cloud's "**wings**," "**nest**," Nature's "unseen **feet**" → don't tag; they're descriptive apparatus of a personification already captured by tagging the entity itself.



## 3. Boundary rules — the hard cases

These are the calls that will actually vary between annotators. To keep data consistent, use this table as a source of truth during the pilot.

| Case | Decision | Example |
|---|---|---|
| **Named landscape features** | Tag as LANDSCAPE, even though they're proper nouns | "Mont Blanc," "Arveiron," "Rhine" |
| **Sun/moon/stars** | Tag as WEATHER (not a separate CELESTIAL category) | "the horned Moon," "the Sun came up" |
| **Direct address to a *concrete* entity** | Tag by its own concrete category — **not** NATURE, even in a poem that also personifies an abstract Power nearby | "thou fresh breaking Day" → WEATHER; "great Mountain" (addressed directly) → LANDSCAPE |
| **Personification that explicitly names its plain referent** | Stays in its concrete category — the naming "bridges" the personification back to a literal thing | *"that orbed maiden... **whom mortals call the Moon**"* → WEATHER, not NATURE |
| **Personification that never names a plain referent** | Functions as an independent character → NATURE | "**mother**'s breast... **she** dances about the sun" (never says "Earth") → NATURE |
| **Personified spirit-characters, generally** | Tag as NATURE whenever named/clearly the subject — confirmed across multiple texts independently | "the Spirits whose presence I command" |
| **"Spirit(s)" — domain test** | Tag NATURE only if (a) a concrete natural domain is identifiable, or (b) it functions as an abstract address to Nature itself. Generic religious/moral "spirit" satisfies neither | "blithe Spirit" → NATURE (path b); "spirit, good or evil" → not tagged |
| **"[Being] of [domain]" epithets** | Tag the whole epithet as one NATURE span | "Daughter of Air!" → `Daughter of Air`, not "Air" alone |
| **"Nature" — sense test, not agency test** | Tag whenever it refers to the natural world as a domain, regardless of capitalization or grammatical role — including passive/objectified uses. Do NOT tag when used in an unrelated sense (human nature, "by nature" = inherently, "the nature of X" = essential character) | "with nature reconciled" → tag, NATURE (passive role, but still refers to the natural world); "it is in his nature to lie" → don't tag (unrelated sense) |
| **"Mother Earth" / "Earth" as addressee** | LANDSCAPE if it clearly means the ground; NATURE if functioning as an abstract force | "My mother Earth!" → borderline, default LANDSCAPE |
| **Similes/metaphors (explicit "like/as")** | Tag, `is_figurative=TRUE` | "he wandered like a wolf" |
| **A real nature-word as metaphor vehicle, no explicit "like/as" needed** | Still `TRUE` | "an age of years all **winters**"; "a strange cold **thaw**" |
| **Entity literally present but described unusually / perceived strangely** | Still `FALSE` | "the **mountains** whirl spinning around me" |
| **Entity appears inside a dream** | Still `FALSE` | "I dreamt that they were filled with **dew**" |
| **Negated existence** | Still tag, still `FALSE` | "nor shapes of men nor **beasts** we ken" |
| **Negated identity-claim** | Also tag, `FALSE` | "**Bird** thou never wert" |
| **Wood/stone as material, not entity** | Do NOT tag | "a wooden door" |
| **"X is a Y" descriptive equation** | Judgment call — tag both if each contributes distinct information | "the **mountain** is a bare perpendicular **rock**" |
| **"Fire" — elemental vs. literal** | Tag when functioning as one of the classical four elements, paired with or implying earth/air/water. Ordinary combustion fire (mood-metaphor, a hearth, a burning building) stays excluded | "with hurricane, fire, and snow" (*The Cloud*, paired with weather-elements) → tag; "The one was fire and fickleness" (*Manfred*, mood metaphor, no elemental framework) → don't tag |

**General rule when still unsure:** tag it and leave a note in the `notes` column, rather than silently skipping it.


## 4. The figurative flag

Every tagged span gets `is_figurative`:
- **FALSE** — the entity is literally present/referenced in the scene ("the albatross followed the ship")
- **TRUE** — the entity is invoked only as a comparison, not literally present ("he wandered like a wolf")



## 5. Abstract and idiomatic uses - "don't tag" principles

**Test: is something actually present and being described, or is the word doing idiomatic, classificatory, or relational work with no scene pictured?**

- **Idioms for death/burial**: "the **grave** closed between us," "a fitting **tomb**."
- **Mood-words sharing vocabulary with weather, but not invoking it**: "dark **gloom**."
- **Purely optical/relational/perceptual concepts**: **horizon, shadow, depth, sheen, echo**.
- **Territorial/administrative references**: **land, climes, regions, latitude**.
- **Color/texture-comparators using mineral/gem names, where nothing is depicted**: "as green as **emerald**," "yellow as **gold**." (Contrast "ribbed **sea-sand**" — tagged, since shore/beach are legitimate LANDSCAPE members.)
- **"Creature" and man/mankind/world/human/person/people** — almost always a human being, never FAUNA.
- **Attributive/classifying place-names or trade-names**: "a **Greenland** whaler," "the **whale**-fishing."
- **Aspiration/state-of-mind words borrowing spatial vocabulary**: "a **paradise** of my own creation."
- **Conventionalized dead metaphors with no reinforcing physical imagery**: "the **channel** of their earlier bent" (contrast "live" metaphors like spring/thaw, which keep the literal sense active via a supporting verb).
- **Lowercase, generic abstract nouns unrelated to the literal sense**: "the **power** of elevating his soul."
- **Purely human/philosophical vocabulary sharing a root with a nature word**: "all the **sages** can."



## 6. Known automatic-detection gaps (read before annotating)

The `annotation.ipynb` notebook pre-selects sentences using a WordNet-based candidate lexicon, plus a keyword boost for capitalised "Nature." Both are heuristics, not ground truth:

**Wrong-sense matches** — check context: **sound** (strait, not noise), **head** (a head of cattle), **side** (a slope), **breath** (a slight wind, not respiration), **sweat** (condensation, not perspiration), **halo** (an atmospheric ring, not religious iconography), **recess** (an inlet, not an abstract retreat), **draught** (a current of air, not a drink), **fly** (insect noun vs. verb).

**Words WordNet doesn't classify under any root, but should be tagged manually**: rock, drift, tide, wilderness, clifts (archaic spelling), ascent, whirl/whirlpool (a type of "current," not geological_formation), margin/bank, ripple, cold/night/summer/season-words (tag when describing actual current conditions, not when merely classifying something else), moonlight, steep (noun sense), herd, thaw, fountain (shares its sense with spring), earthquake (a dynamic event, not a static landform, but tag it anyway).

**Poetic/inverted syntax can fool the POS tagger**: a list-like line such as "Rocks, caves, lakes, fens..." may score artificially low because spaCy mis-tags some of those nouns as verbs. This is due to the fact that poetic syntax often tricks the automated tagger. Periodically check band_0 sentences in nature-heavy poems to ensure valid entities weren't missed.

**A fixed bug worth knowing about**: excluding human-referring words (to stop "man" from matching FAUNA) accidentally also excluded "star" via an unrelated "actor" sense. Fixed in the pipeline.



## 7. How to fill out the annotation CSV

**Important**: One must create one row per entity mention, not per sentence. If a sentence has three mentions, duplicate the row so there are three identical `sentence_id` rows, and fill out a distinct entity for each.

Fill out the blank target columns as follows:
- `target_span`: The exact text of the mention (e.g., "Albatross"), it must match the source text exactly (case-sensitive).
- `start_char` and `end_char`: They will be generated automatically once annotation is complete.
- `entity_type`: The category label (FLORA, FAUNA, WEATHER, LANDSCAPE, or NATURE).
- `is_figurative`: TRUE if it is a simile/metaphor, FALSE if literal.
- `lemma`: The root form of the target span.
- `notes`: Optional but useful for clarifying the reasons behind a tag.



## 8. Examples from the corpus

> *"The Ice was here, the Ice was there, / The Ice was all around: / It crack'd and growl'd, and roar'd and howl'd"* (Ancient Mariner)
→ `Ice` × WEATHER, `is_figurative=FALSE` (three separate mentions, same span text, each tagged individually since they're distinct clauses)

> *"At length did cross an Albatross"* (Ancient Mariner)
→ `Albatross` × FAUNA, `is_figurative=FALSE`

> *"O wild West Wind, thou breath of Autumn's being"* (Ode to the West Wind)
→ `West Wind` × WEATHER, `is_figurative=FALSE` (compound name, tagged as one span)

> *"My mother Earth! And thou fresh breaking Day, and you, ye Mountains"* (Manfred)
→ `Earth` × LANDSCAPE (borderline call per §3), `Day` × WEATHER,
`Mountains` × LANDSCAPE — three separate mentions in one line

> *"I stood beside the sources of the Arveiron, which take their rise in a glacier"* (Frankenstein, Ch. 10)
→ `Arveiron` × LANDSCAPE, `glacier` × LANDSCAPE

> *"Clear, placid Leman! thy contrasted lake"* (Childe Harold III)
→ `Leman` × LANDSCAPE (proper name for the lake — both name and lake refer to the same single mention here)