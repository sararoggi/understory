<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/dark_header.png">
    <source media="(prefers-color-scheme: light)" srcset="./assets/light_header.png">
    <img src="./assets/light_header.png" alt="Understory Header" width="100%">
  </picture>
</div>

---

## About

**Understory** is an NLP project exploring the presence and agency of the natural world in literary texts. A BERT-based named entity recognizer, fine-tuned on a manually annotated corpus of Romantic-era English literature, first **identifies non-human natural entities** across the texts and classifies them into flora, fauna, weather, landscape, or personified natural force. Then, a dependency-based grammatical analysis **examines the role** each one plays within its sentence.

Together, these two steps investigate how nature acts within these texts - and how often it doesn't.

The project takes its name from the forest understory, a less visible layer of interconnected life, used here as a metaphor for identifying the hidden structures and patterns within literary texts.

## Corpus

13 passages spanning 6 authors, ~30,000 words total, sourced from Project Gutenberg:

| Author | Works |
|---|---|
| Samuel Taylor Coleridge | The Rime of the Ancient Mariner |
| William Wordsworth | Tintern Abbey, Lines Written in Early Spring, The Tables Turned |
| Percy Shelley | Ode to the West Wind, Mont Blanc, The Cloud, To a Skylark |
| Mary Shelley | Frankenstein (Letters 1–4, Chapter 10) |
| Lord Byron | Childe Harold's Pilgrimage (Canto III), Manfred (Act I Scene II, Act II Scene II) |

## Pipeline

```
notebooks/setup.ipynb        →  download + clean corpus, cache BERT/spaCy/WordNet resources
notebooks/annotation.ipynb   →  WordNet-based candidate pooling for annotation
        ↓
   (manual annotation)
        ↓
notebooks/ner_model.ipynb                →  (1) fine-tune BERT for NER, (2) run the final model over the unannotated corpus
notebooks/dependency_analysis.ipynb  →  classify grammatical role per entity, verify parser choice
notebooks/llm_analysis.ipynb         →  cross-genre LLM simulation, compared against the real corpus
```

Each notebook has its own purpose and can be run independently, provided its prerequisites have already been run once.

## Entity schema

| Category | Covers |
|---|---|
| **FLORA** | Trees, flowers, moss, woods, foliage |
| **FAUNA** | Animals, birds - literal, non-human creatures |
| **WEATHER** | Weather, atmospheric, and celestial phenomena |
| **LANDSCAPE** | Topographic and geological features, including named places |
| **NATURE** | Personified nature-as-force - embodied spirit-characters, pantheistic animating forces |

Full annotation methodology is documented in [`docs/annotation_guidelines.md`](docs/annotation_guidelines.md).

## Setup

```bash
pip install -r requirements.txt
```

Run `notebooks/setup.ipynb` first - it downloads the corpus and caches the needed resources for later notebooks.

## Try the App

**Live at https://sidereus.dev/understory/**

Or run it locally:

**Prerequisite:** `notebooks/ner_model.ipynb` must have been run first, so `checkpoints/final/saved_model` exists.

```bash
cd app
python app.py
```

Then open **http://127.0.0.1:5001** in your browser to explore the understory of your own text.