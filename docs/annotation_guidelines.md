# Annotation Guidelines

This document serves as the methodological record for the annotation process, detailing every refinement, rule, and edge-case decision made while constructing the gold-standard corpus.


## 1. The five entity categories

| Category | Definition | Typical words |
|---|---|---|
| **FLORA** | Individual plants, trees, flowers, or vegetation | tree, oak, moss, grove, foliage |
| **FAUNA** | Animals, birds, insects - literal, non-human creatures | albatross, bird, snake |
| **WEATHER** | Weather, atmospherical and celestial phenomena | wind, storm, ice, sun, moon, sky |
| **LANDSCAPE** | Topographic / geological features, including named places | river, mountain, glacier, rock, Mont Blanc, Jungfrau |
| **NATURE** | Personified nature as a unified force. This includes direct abstract addresses, named spirit-characters, or forces described without the specific word "Nature." | "Nature, thou great..."; "the Witch of the Alps" |


## 2. What counts as a mention (span rules)

- **Tag the head noun.** For phrases like "the frozen lake", tag only `lake`.

- **Proper and compound names stay together.** "Mont Blanc", "Lake Leman", "the West Wind" function as single named entities and should be tagged as one span.

- **One tag per mention.** If a pronoun refers back to an entity ("the river... it glideth"), tag only the original noun (`river`). However, if a new independent noun phrase appears in a later clause, it receives its own tag.

- **Generic vs. specific mentions are not distinguished.** "the trees" and "an oak" are both tagged FLORA - no sub-categorization is needed.

- **Only tag nouns, never verbs** - even if they share nature vocabulary (e.g. "Melancholy clouded every thought" -> do not tag).

- **"X of Y" constructions.** Test: does X have a specific, independent meaning without Y?
  - **Yes -> tag both**: "caves of ice", "icy wall of the glacier" - X already names something real and specific on its own.
  - **No -> tag as ONE span**: "skeletons of leaves", "sea of ice", "dome of air" - X is an abstract shape that becomes concrete when combined with Y.

- **Possessives ("[entity]'s [word]"):**
  - **One combined span** when the possessed word is a literal geographic/anatomical feature or an active substantive noun: "mountain's head" (summit), "Sun's rim"
  - **Excluded entirely** when the possessed word is purely decorative: wilderness's "tongue", the Cloud's "wings", "Sun's throne" -> Tag only the possessor.
  - **Split as composition** when both halves are robust, independent entities recognized elsewhere in the corpus: "summits of the mountains".
  - **Intensity/manner descriptors are excluded**: words denoting volume or intensity do not count as second entities. "roar of torrents", "thunder sound of the avalanche", "pouring in torrents" (idiom for "heavily")

- **Reduplicative idioms are one mention.** "From **peak** to peak", "from **steep** to steep" -> tag once

- **"[Being] of [domain1] AND [domain2]" = one epithet.** "Daughter of Earth and Water" -> one NATURE span. // **"[Being1] OR [Being2]" = two separate tags**. "Teach us, Sprite **or** Bird" → `Sprite` (NATURE) + `Bird` (FAUNA), each its own row.

- **Literal anatomy** is tagged: pine's "trunk" or an eagle's "wings" are tagged normally. Borrowed or decorative anatomy (e.g., the wilderness's "tongue") is excluded.


## 3. Boundary rules for ambiguous cases

When facing ambiguous phrasing, refer to this table as the source of truth.

| Case | Decision | Example |
|---|---|---|
| **Named landscape features** | LANDSCAPE, even if WordNet fails to recognize the proper noun | "Mont Blanc", "Arveiron" |
| **Celestial bodies** | Tag as WEATHER | "the Sun came up" |
| **Direct address to a *concrete* entity** | Tag according to its specific category, not NATURE | "thou fresh breaking Day" -> WEATHER |
| **Personification that explicitly names its literal referent** | Retain the concrete category. The literal name bridges the personification back to reality. | *"that orbed maiden... **whom mortals call the Moon**"* -> WEATHER, not NATURE |
| **Personification without a literal referent** | Functions as an independent character -> NATURE | "**mother**'s breast... she dances" (never says "Earth") → NATURE |
| **Spirit-characters** | Tag as NATURE if they are tied to a natural domain or act as an abstract address to Nature. Generic religious/moral spirits are not tagged. | "the Spirits whose presence I command" |
| **Extended appositive restatements** | Tag only the first naming, unless a later restatement passes the domain-test independently. | "a presence... a motion and a **spirit**, that impels" -> `presence` + `spirit` |
| **Spatial vocabulary used for human interiority** | Do NOT tag | "thy memory be as a **dwelling-place** for all sweet sounds" (metaphor for memory, not a real place) |
| **"Mother Earth" / "Earth" as addressee** | Tag as LANDSCAPE if referring literally to the ground. Tag as NATURE only if it acts as a pantheistic, animating force. | "this green earth, on which I gaze" -> LANDSCAPE |
| **Abstract personifications (death, decay)** | Do NOT tag, even if capitalized and agentive, unless tied to a natural domain. | "Destruction's splinters" -> `splinters` tagged LANDSCAPE, "Destruction" itself excluded |
| **Material composition** | Do NOT tag | "a wooden door" |
| **"Fire" - elemental vs. literal** | Tag as WEATHER when invoked as one of the four classical elements. Exclude literal or mood-metaphor fires (e.g. a hearth). | "with hurricane, fire, and snow" -> WEATHER |

**General rule:** If you remain unsure after consulting the rules, tag the entity and leave a detailed note in the notes column rather than silently skipping it.


## 4. The figurative flag
Every tagged span must be marked as either literal or figurative.
- **FALSE** - the entity is physically present in the described scene ("the albatross followed the ship")
- **TRUE** - the entity is invoked only as a comparison or metaphor ("he wandered like a wolf")

| Case | Decision | Example |
|---|---|---|
| **Implied metaphors** | Tag as `TRUE` even without "like/as," provided supporting vocabulary keeps the literal sense active | "he wandered like a wolf" |
| **Distorted perception** | Tag as `FALSE`. An entity perceived strangely is still literally present. | "the mountains whirl spinning around me" |
| **Dreams and visions** | Tag as `FALSE`. An entity seen in a dream is still treated as literal within the context of that dream | "I dreamt... filled with dew" |
| **Negations** | Tag as `FALSE`. Negated existence or negated identity claims still refer to literal categories. | "Bird thou never wert" |



## 5. Exclusions: abstract and idiomatic uses

Test: is something actually present and being described, or is the word doing idiomatic, classificatory or relational work with no scene pictured?

Do NOT tag the following:

- **Death idioms**: "the grave closed", "a fitting tomb"
- **Atmospheric mood-words**: "dark gloom"
- **Optical/relational concepts**: horizon, shadow, depth
- **Territorial/administrative references**: land, climes, regions, latitude
- **Color/texture comparators**: "yellow as gold" (where no actual gold is depicted)
- **Human proxies**: Words like "creature," "world," or "mankind" almost always refer to humans, not FAUNA
- **Attributive place names**: "a Greenland whaler"
- **Dead metaphors**: "the channel of their earlier bent"
- **Generic abstract nouns unrelated to the literal sense**: "the power of elevating his soul".



## 6. Known automatic-detection gaps

The `annotation.ipynb` notebook pre-selects sentences using WordNet plus a keyword boost for "Nature". Both are heuristics and imperfect, be aware of the following known issues:

**Wrong-sense matches:** Always check the context. Automated taggers often misinterpret words like sound (strait vs. noise), head (cattle vs. anatomy), breath (wind vs. respiration), and halo (atmospheric ring vs. religious art).

**Poetic syntax errorsr**: Inverted, list-like poetry ("Rocks, caves, lakes, fens...") often confuses the POS tagger, causing nouns to be incorrectly tagged as verbs. Periodically review low-confidence (band_0) sentences in dense poems.

**A fixed bug worth knowing about**: excluding human-referring words (to stop "man" from matching FAUNA) accidentally also excluded "star" via an unrelated "actor" sense. Fixed in the pipeline.


## 7. How to fill out the CSV

- **Never annotate directly in `annotation_pool.csv`.** Work in a separate copy (e.g. `manual_annotation.csv`) to prevent accidental overwrites.
- **Don't edit `band`, `n_candidates`, or `candidate_words`** - provenance record of the automated pre-filter, useful for quantifying its accuracy later.
- **Duplicate the whole row**: one must create one row per entity mention, not per sentence, copying `sentence_id`/`sentence_text` exactly, for multi-entity sentences.

Fill out the blank target columns as follows:
- `target_span`: The exact text of the mention (e.g. "Albatross"), it must match the source text exactly (case-sensitive).
- `start_char` and `end_char`: Leave blank. These will be automatically generated post-annotation.
- `entity_type`: Choose the category label (FLORA, FAUNA, WEATHER, LANDSCAPE, or NATURE).
- `is_figurative`: TRUE or FALSE
- `lemma`: The root form of the target span.
- `notes`: Optional, use to explain the reasons behind a tag.