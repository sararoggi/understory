import pandas as pd
import random

def classify_ner_errors(true_spans, pred_spans):
    taxonomy = {"label_confusion": [], "boundary_error": [], "spurious": [], "missed": []}
    matched_true = set()
    
    for p_start, p_end, p_label, p_text in pred_spans:
        found_match = False
        for t_idx, (t_start, t_end, t_label, t_text) in enumerate(true_spans):
            overlap = max(0, min(p_end, t_end) - max(p_start, t_start))
            if overlap > 0:
                found_match = True
                matched_true.add(t_idx)
                
                if p_start == t_start and p_end == t_end and p_label != t_label:
                    taxonomy["label_confusion"].append({
                        "text": p_text, "pred_label": p_label, "true_label": t_label})
                elif p_start != t_start or p_end != t_end:
                    taxonomy["boundary_error"].append({
                        "pred_text": p_text, "true_text": t_text, 
                        "pred_label": p_label, "true_label": t_label})
                break
                
        if not found_match:
            taxonomy["spurious"].append({"text": p_text, "pred_label": p_label})
            
    for t_idx, (t_start, t_end, t_label, t_text) in enumerate(true_spans):
        if t_idx not in matched_true:
            taxonomy["missed"].append({"text": t_text, "true_label": t_label})
            
    return taxonomy


# format hugging face predictions and run the error taxonomy
def extract_and_classify_fold(val_sentences, predictions, labels, tokenizer, id_to_label, decode_fn):
    fold_errors = {"label_confusion": [], "boundary_error": [], "spurious": [], "missed": []}
    
    for sent, pred_ids, true_ids in zip(val_sentences, predictions, labels):
        encoding = tokenizer(sent["text"], return_offsets_mapping=True, truncation=True)
        
        pred_dicts = decode_fn(encoding["offset_mapping"], encoding.word_ids(), pred_ids.tolist(), id_to_label)
        true_dicts = decode_fn(encoding["offset_mapping"], encoding.word_ids(), true_ids.tolist(), id_to_label)

        pred_spans = [(s["start"], s["end"], s["label"], sent["text"][s["start"]:s["end"]]) for s in pred_dicts]
        true_spans = [(s["start"], s["end"], s["label"], sent["text"][s["start"]:s["end"]]) for s in true_dicts]

        sentence_taxonomy = classify_ner_errors(true_spans, pred_spans)
        
        for cat in fold_errors:
            for error_item in sentence_taxonomy[cat]:
                error_item["sentence_id"] = sent["sentence_id"]
                error_item["full_text"] = sent["text"]
                fold_errors[cat].append(error_item)

    return fold_errors

# return df summarizing error % across folds
def summarize_errors(all_fold_errors):
    total_counts = {cat: sum(len(fold[cat]) for fold in all_fold_errors) 
                    for cat in ["label_confusion", "boundary_error", "spurious", "missed"]}
    df = pd.DataFrame(list(total_counts.items()), columns=["Error Category", "Total Count"])
    df["Percentage"] = (df["Total Count"] / df["Total Count"].sum()) * 100
    return df.round(2)

def export_error_samples(all_fold_errors, save_path):
    rows = []
    for fold_idx, fold_errs in enumerate(all_fold_errors):
        for cat, items in fold_errs.items():
            for item in items:
                item_copy = item.copy()
                item_copy["fold"] = fold_idx
                item_copy["category"] = cat
                rows.append(item_copy)
    df = pd.DataFrame(rows)
    df.to_csv(save_path, index=False)
    return df

# print random sample of specific errors for qualitative analysis
def print_qualitative_analysis(all_fold_errors, error_type="spurious", focus_classes=None, sample_size=5):
    errors_to_show = []
    for fold_idx, fold_errs in enumerate(all_fold_errors):
        for e in fold_errs.get(error_type, []):
            e_copy = e.copy()
            e_copy["fold"] = fold_idx
            errors_to_show.append(e_copy)
            
    if focus_classes:
        errors_to_show = [
            e for e in errors_to_show 
            if e.get("pred_label") in focus_classes or e.get("true_label") in focus_classes
        ]

    if not errors_to_show:
        print(f"No {error_type} errors found for classes {focus_classes}.")
        return

    if len(errors_to_show) > sample_size:
        errors_to_show = random.sample(errors_to_show, sample_size)
        
    print(f"--- QUALITATIVE ANALYSIS: {error_type.upper()} ---")
    for e in errors_to_show:
        print(f"[Fold {e['fold']} | ID: {e['sentence_id']}] {e['full_text']}")
        details = {k: v for k, v in e.items() if k not in ["full_text", "sentence_id", "fold"]}
        print(f"   DETAILS: {details}\n")