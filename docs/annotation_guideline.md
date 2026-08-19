# Annotation Guidelines — Non-Human Natural Entities NER

**Project:** Tracing Non-Human Agency in Romantic Literature through NLP
**Purpose of this document:** a single reference to annotate consistently.



## 1. The five entity categories

| Category | Definition | Typical words |
|---|---|---|
| **FLORA** | Individual plants, trees, flowers, or vegetation as a mass (woods, foliage) | tree, oak, flower, moss, grove, foliage |
| **FAUNA** | Animals, birds, insects — literal, non-human creatures | albatross, wolf, bird, snake |
| **WEATHER** | Weather, sky, and celestial phenomena | wind, storm, rain, cloud, snow, ice, sun, moon, stars, sky |
| **LANDSCAPE** | Topographic / geological features, including named places | river, mountain, glacier, lake, valley, rock, Mont Blanc, the Rhine, the Jungfrau |
| **NATURE** | Personified nature-as-a-unified-force — not a specific plant/animal/weather/landform. Covers both abstract address ("Nature, thou...") **and** nature manifested as a character (e.g. the Witch of the Alps in Manfred) — same underlying phenomenon, two literary devices. Not limited to the literal word "Nature": "Mother Earth," "the great Power," or a pronoun clearly referring to personified nature all qualify | "Nature, thou great and unconquerable force..."; "the Witch of the Alps" |

Four concrete categories (FLORA/FAUNA/WEATHER/LANDSCAPE) plus NATURE for the abstract personification, since that's central to the agency question this project is actually asking.



## 2. What counts as a mention (span rules)

- **Tag the head noun.** For "the frozen lake," tag only `lake`, not the full noun phrase — this keeps spans consistent for a machine learning model to learn from.
- **Exception — proper/compound names stay together.** "Mont Blanc," "Lake Leman," "the West Wind," "the Jungfrau" are tagged as one span, since they function as a single named entity, not a generic noun with a modifier.
- **One tag per mention**, even if a pronoun refers back to it later in the sentence ("the river... it glideth" → tag "river" only; don't tag "it").
- **Generic vs. specific mentions are not distinguished.** "the trees" and "an oak" are both tagged FLORA — no special sub-marking needed.



## 3. Boundary rules — the hard cases

These are the calls that will actually vary between annotators. To keep data consistent, use this table as a source of truth during the pilot.


| Case | Decision | Example |
|---|---|---|
| **Named landscape features** | Tag as LANDSCAPE, even though they're proper nouns | "Mont Blanc," "the Arveiron," "the Rhine" |
| **Sun/moon/stars** | Tag as WEATHER (not a separate CELESTIAL category) | "the horned Moon," "the Sun came up" |
| **Directly addressed / personified entity (vocative "thou")** | Still tag the underlying entity by its concrete category — personification is captured by the *dependency-role* layer later, not by inventing a new NER category | "thou fresh breaking Day" → WEATHER; "you, ye Mountains" → LANDSCAPE |
| **Supernatural nature-spirits as characters** (Witch of the Alps, "Spirits of the unbounded Universe") | **Tag as NATURE** whenever she is named or clearly the subject of a clause (not every pronoun referring back to her — see §2, one tag per mention). She is a personified embodiment of nature-as-force, the same phenomenon as abstract "Nature," just manifested as a character rather than an address. |
| **"Mother Earth" / "Earth" as addressee** | Tag as LANDSCAPE if it clearly means the planet/ground; tag as NATURE if it's functioning as an abstract personified force interchangeable with "Nature" — use judgment, and flag ambiguous cases in a comments column for later review | "My mother Earth!" → borderline; default to LANDSCAPE unless context clearly frames it as an abstract cosmic force |
| **Similes/metaphors** | Tag them, and set `is_figurative = TRUE` (see §4) | "he wandered like a wolf" → tag "wolf" as FAUNA, `is_figurative=TRUE` |
| **Wood/stone as material, not entity** | Do NOT tag — this is about the substance, not the living/topographic thing | "a wooden door," "a stone wall" — no tag |
| **Weather-word used as a name/title, not literally** | Do NOT tag | (rare in this corpus, but e.g. a ship literally named "The Tempest" wouldn't count) |

**General rule when still unsure:** tag it and leave a note in a comments column, rather than silently skipping it.



## 4. The figurative flag

Every tagged span gets `is_figurative`:
- **FALSE** — the entity is literally present/referenced in the scene ("the albatross followed the ship")
- **TRUE** — the entity is invoked only as a comparison, not literally present ("he wandered like a wolf")

This lets report the literal vs. figurative role distribution separately in the transitivity analysis later — figurative mentions are grammatically real (they can still be Actor/Goal in their own clause) but represent a different kind of ecocritical fact (association/comparison rather than depiction), so keeping them distinguishable, rather than either merging or discarding them, is what gives the most flexibility in the final analysis.



## 5. Known automatic-detection gaps (read before annotating)

The `annotation.ipynb` notebook pre-selects sentences using a WordNet-based candidate lexicon, plus a keyword boost for capitalised "Nature." Both are heuristics, not ground truth:

- **NATURE mentions won't reliably surface via the lexicon** — WordNet has no synset for "Nature-as-abstract-force," so only the keyword boost (`\bNature\b`) catches these, and it will miss cases phrased as "the Mother" or "the great Power" without the literal word "Nature". Noting a passage personifies Nature without using the word, add it to the pool manually.
- **Poetic/inverted syntax can fool the POS tagger** (documented in the
  script itself) — a list-like line such as "Rocks, caves, lakes, fens..." may score artificially low because spaCy mis-tags some of those nouns as verbs. This is due to the fact that poetic syntax often tricks the automated tagger. Periodically spot-check band_0 sentences in nature-heavy poems to ensure valid entities weren't missed.
- **`candidate_words` is a hint, not a label** — always read the full sentence before tagging; the automatic match can be the wrong word sense.



## 6. Worked examples from the corpus

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



## 7. How to fill out the annotation CSV

**Important**: One must create one row per entity mention, not per sentence. If a sentence has three mentions, duplicate the row so there are three identical `sentence_id` rows, and fill out a distinct entity for each.

Fill out the blank target columns as follows:
- `target_span`: The exact text of the mention (e.g., "Albatross").
- `start_char` and `end_char`: They will be generated automatically once annotation is complete.
- `entity_type`: The category label (FLORA, FAUNA, WEATHER, LANDSCAPE, or NATURE).
- `is_figurative`: TRUE if it is a simile/metaphor, FALSE if literal.
- `lemma`: The root form of the target span.