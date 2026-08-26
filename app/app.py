import os
import html as html_module
import torch
import spacy
from flask import Flask, render_template, request
from transformers import AutoModelForTokenClassification, AutoTokenizer

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FINAL_MODEL_DIR = os.path.join(PROJECT_ROOT, "checkpoints", "final", "saved_model")

CONFIDENCE_THRESHOLD = 0.6
ENTITY_TYPES = ["FLORA", "FAUNA", "WEATHER", "LANDSCAPE", "NATURE"]
label_list = ["O"] + [f"{p}-{t}" for t in ENTITY_TYPES for p in ("B", "I")]
label_to_id = {l: i for i, l in enumerate(label_list)}
id_to_label = {i: l for l, i in label_to_id.items()}

CATEGORY_COLORS = {
    "WEATHER":   "#FCDC4D",
    "LANDSCAPE": "#56A3A6",
    "FLORA":     "#A5BE00",
    "FAUNA":     "#A30000",
    "NATURE":    "#331E38",
}

DEP_LABEL_NAME = {
    "nsubj": "Active Subject",
    "nsubjpass": "Passive Subject",
    "dobj": "Direct Object",
    "dative": "Indirect Object",
    "pobj": "Object of Preposition",
    "attr": "Attribute",
    "appos": "Appositive",
    "conj": "Conjoined Element",
    "ROOT": "Root",
}

# Load models ONCE at startup, not per-request
print("Loading NER model...")
if not os.path.exists(FINAL_MODEL_DIR):
    raise FileNotFoundError(
        f"No trained model found at {FINAL_MODEL_DIR}. "
        f"Run ner_model.ipynb first to train and save the final model."
    )
final_model = AutoModelForTokenClassification.from_pretrained(FINAL_MODEL_DIR)
tokenizer = AutoTokenizer.from_pretrained(FINAL_MODEL_DIR)
final_model.eval()

print("Loading spaCy parser...")
nlp = spacy.load("en_core_web_trf")


# Reused functions from notebooks
def decode_bio_to_spans(offsets, word_ids, labels, id_to_label):
    spans, current, current_word_id = [], None, None
    previous_word_id = None
    for (start, end), wid, lab_id in zip(offsets, word_ids, labels):
        if wid is None:
            previous_word_id = wid
            continue
        if wid == previous_word_id:
            if current is not None and wid == current_word_id:
                current["end"] = end
            previous_word_id = wid
            continue
        if lab_id != -100:
            lab = id_to_label[lab_id]
            if lab == "O":
                if current: spans.append(current); current = None
            elif lab.startswith("B-"):
                if current: spans.append(current)
                current = {"start": start, "end": end, "label": lab[2:]}
                current_word_id = wid
            elif lab.startswith("I-"):
                if current and current["label"] == lab[2:]:
                    current["end"] = end; current_word_id = wid
                else:
                    if current: spans.append(current)
                    current = {"start": start, "end": end, "label": lab[2:]}
                    current_word_id = wid
        previous_word_id = wid
    if current: spans.append(current)
    return spans


def predict_with_threshold(text, model, tokenizer, label_to_id, id_to_label, threshold=CONFIDENCE_THRESHOLD):
    device = next(model.parameters()).device
    encoding = tokenizer(text, return_offsets_mapping=True, truncation=True, return_tensors="pt")
    offsets = encoding["offset_mapping"][0].tolist()
    word_ids = encoding.word_ids(batch_index=0)
    model_inputs = {k: v.to(device) for k, v in encoding.items() if k != "offset_mapping"}

    with torch.no_grad():
        logits = model(**model_inputs).logits[0]
    probs = torch.softmax(logits, dim=-1)
    confidences, pred_ids = torch.max(probs, dim=-1)

    o_id = label_to_id["O"]
    pred_ids = torch.where(confidences < threshold, torch.full_like(pred_ids, o_id), pred_ids)

    return decode_bio_to_spans(offsets, word_ids, pred_ids.tolist(), id_to_label)


def get_entity_role(start_char, end_char, doc):
    span = doc.char_span(start_char, end_char, alignment_mode="expand")
    if span is None or len(span) == 0:
        return "unknown"
    dep = span.root.dep_
    return DEP_LABEL_NAME.get(dep, dep)


def luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4)]
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def build_highlighted_html(text, entities):
    entities = sorted(entities, key=lambda e: e["start"])
    html_parts = []
    cursor = 0
    for e in entities:
        # Escape plain text segments to prevent broken HTML
        plain = html_module.escape(text[cursor:e["start"]])
        html_parts.append(plain.replace("\n", "<br>"))
        color = CATEGORY_COLORS.get(e["label"], "#CCCCCC")
        text_color = "white" if luminance(color) < 0.4 else "black"
        label = html_module.escape(e["label"])
        role  = html_module.escape(e["role"])
        etext = html_module.escape(e["text"])
        html_parts.append(
            f'<span class="entity" data-category="{label}" '
            f'style="background-color:{color}; color:{text_color};" '
            f'title="{label} \u2014 {role}">{etext}</span>'
        )
        cursor = e["end"]
    tail = html_module.escape(text[cursor:])
    html_parts.append(tail.replace("\n", "<br>"))
    return "".join(html_parts)

# Flask app
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", highlighted_html=None, entities=None, input_text="")


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()

    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename:
        raw_bytes = uploaded_file.read()
        try:
            text = raw_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            return render_template("index.html", highlighted_html=None, entities=None,
                                    input_text="", error="Could not read file -- please upload a plain UTF-8 .txt file.")

    if not text:
        return render_template("index.html", highlighted_html=None, entities=None, input_text="")

    MAX_CHARS = 5000
    truncated = len(text) > MAX_CHARS
    if truncated:
        text = text[:MAX_CHARS]

    doc = nlp(text)
    spans = predict_with_threshold(text, final_model, tokenizer, label_to_id, id_to_label)

    entities = []
    for s in spans:
        role = get_entity_role(s["start"], s["end"], doc)
        entities.append({
            "start": s["start"], "end": s["end"],
            "text": text[s["start"]:s["end"]],
            "label": s["label"], "role": role,
        })

    highlighted_html = build_highlighted_html(text, entities)
    return render_template("index.html", highlighted_html=highlighted_html, entities=entities,
                            input_text=text, truncated=truncated)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)