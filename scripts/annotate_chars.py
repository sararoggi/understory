# The current file fills in start_char/end_char for the finished manual annotation file, producing the gold-standard dataset (final_annotation.csv).

import os
import sys
import csv
import re
from collections import defaultdict

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

if os.path.basename(SCRIPT_DIR) == "scripts":
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
else:
    PROJECT_ROOT = SCRIPT_DIR
 
DEFAULT_INPUT = os.path.join(PROJECT_ROOT, "data", "annotations", "manual_annotation.csv")
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "data", "annotations", "final_annotation.csv")


# Return a list of every start index where span occurs in text, in order - matching span as a standalone word/phrase only, not as a fragment embedded inside a longer word (e.g. "moon" must not match inside "moonlight").
def find_all_occurrences(text: str, span: str):
    pattern = r"\b" + re.escape(span) + r"\b"
    return [m.start() for m in re.finditer(pattern, text)]


def compute_offsets(input_path: str, output_path: str):
    with open(input_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Group row indices by (sentence_id, target_span). Rows within a group are kept in their original file order.
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
            for r_idx in row_indices:
                warnings.append(f"Row {r_idx + 2} [{sentence_id}] {span!r}: NOT FOUND in text.")
            continue

        # Covers both reduplicative idioms (1 row) and genuinely repeated mentions where the counts line up.
        if n_rows == n_occ:
            pairs = list(zip(row_indices, occurrences))

        # Reduplicative idiom case: one tagged row, the word repeats in the text (e.g. "peak" in "from peak to peak"). Only one occurrence needs an offset -> take the first.
        elif n_rows == 1 and n_occ > 1:
            pairs = [(row_indices[0], occurrences[0])]

        # More tagged rows than the text actually contains - a real problem (duplicate row, or a typo in target_span/sentence_text).
        elif n_rows > n_occ:
            warnings.append(
                f"[{sentence_id}] {span!r}: {n_rows} rows, only {n_occ} occurrence(s) -- check for a duplicate row."
            )
            pairs = list(zip(row_indices, occurrences))

        # More occurrences than rows, and more than one row -- genuinely ambiguous which occurrences were meant. Match in file order and flag for a manual check.
        else:
            warnings.append(
                f"[{sentence_id}] {span!r}: {n_rows} rows, {n_occ} occurrences -- matched in order, verify."
            )
            pairs = list(zip(row_indices, occurrences[:n_rows]))

        for r_idx, start_char in pairs:
            end_char = start_char + len(span)
            rows[r_idx]["start_char"] = start_char
            rows[r_idx]["end_char"] = end_char
            processed += 1

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processed {processed} mentions, {skipped_blank} blank rows skipped.")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(w)
    else:
        print("\nNo warnings.")
    print(f"\nWrote {output_path}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT
    compute_offsets(input_path, output_path)