# The current file fills in start_char/end_char for the finished manual annotation file, producing the gold-standard dataset (annotated_final.csv) ready for training.

import os
import sys
import csv
from collections import defaultdict

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
 
if os.path.basename(SCRIPT_DIR) == "scripts":
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
else:
    PROJECT_ROOT = SCRIPT_DIR
 
DEFAULT_INPUT = os.path.join(PROJECT_ROOT, "data", "annotations", "manual_annotation.csv")
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "data", "annotations", "final_annotation.csv")


def find_all_occurrences(text: str, span: str):
    # Return a list of every start index where span occurs in text, in order.
    occurrences = []
    start = 0
    while True:
        idx = text.find(span, start)
        if idx == -1:
            break
        occurrences.append(idx)
        start = idx + 1
    return occurrences


def compute_offsets(input_path: str, output_path: str):
    with open(input_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Group row indices by (sentence_id, target_span). Rows within a group are kept in their original file order, which is assumed to match the left-to-right order the mentions appear in the text.

    groups = defaultdict(list)
    for i, row in enumerate(rows):
        span = (row.get("target_span") or "").strip()
        if not span:
            continue
        key = (row.get("sentence_id"), span)
        groups[key].append(i)

    warnings = []
    processed = 0
    skipped_blank = sum(1 for r in rows if not (r.get("target_span") or "").strip())

    for (sentence_id, span), row_indices in groups.items():
        sentence = rows[row_indices[0]].get("sentence_text") or ""
        occurrences = find_all_occurrences(sentence, span)

        n_rows = len(row_indices)
        n_occ = len(occurrences)

        if n_occ == 0:
            for ridx in row_indices:
                warnings.append(
                    f"Row {ridx + 2} (sentence_id={sentence_id}): target_span {span!r} NOT FOUND in sentence_text. Left unfilled -- check for a typo or a mismatched quote/apostrophe character."
                )
            continue

        if n_rows == n_occ:
            # The common case: N tagged rows, N occurrences in the text - including reduplicative idioms with a single row (n_rows=1, n_occ could be 1 or more, handled below) and genuinely repeated independent mentions where the counts line up exactly (e.g. three 'Ice' rows, three 'Ice' occurrences).
            pairs = list(zip(row_indices, occurrences))

        elif n_rows == 1 and n_occ > 1:
            # Reduplicative idiom case: one tagged row, the word repeats in the text (e.g. "peak" in "from peak to peak"). Only one occurrence needs an offset - take the first, since the guideline's intent is a single representative span.
            pairs = [(row_indices[0], occurrences[0])]

        elif n_rows > n_occ:
            # More tagged rows than the text actually contains - a real problem (duplicate row, or a typo in target_span/sentence_text).
            warnings.append(
                f"sentence_id={sentence_id}, span={span!r}: {n_rows} annotated row(s) but only {n_occ} occurrence(s) found in the text. Filled the first {n_occ} row(s) in file order; the remaining {n_rows - n_occ} row(s) left unfilled -- check for an accidental duplicate row."
            )
            pairs = list(zip(row_indices, occurrences))

        else:
            # n_rows > 1 and n_rows < n_occ: more repeats in the text than tagged rows, but more than one row exists, so it isn't the simple single-idiom case either. Match in file order to the first n_rows occurrences and flag for a manual check, since which occurrences were intended is genuinely ambiguous here.
            warnings.append(
                f"sentence_id={sentence_id}, span={span!r}: {n_rows} annotated row(s), {n_occ} occurrence(s) in the text - matched to the first {n_rows} occurrences in file order; please verify this is the intended set."
            )
            pairs = list(zip(row_indices, occurrences[:n_rows]))

        for ridx, start_char in pairs:
            end_char = start_char + len(span)
            rows[ridx]["start_char"] = start_char
            rows[ridx]["end_char"] = end_char
            processed += 1

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processed {processed} annotated mentions ({skipped_blank} blank rows skipped, as expected).")
    if warnings:
        print(f"\n{len(warnings)} warning(s) -- review these manually:")
        for w in warnings:
            print(w)
    else:
        print("\nNo warnings -- every span matched cleanly.")
    print(f"\nWrote {output_path}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT
    compute_offsets(input_path, output_path)