#!/usr/bin/env python3
"""
Calculates prior probabilities of languages from training data.
"""

import sys
import csv
import json


def compute_prior(train_file, mapping_file, output_file):
    """
    Computes and writes prior probabilities for languages based on training data.

    Parameters:
      train_file (str): Path to the training TSV file.
      mapping_file (str): Path to the JSON file containing language mapping.
      output_file (str): Path to the output file where priors will be written.
    """
    with open(mapping_file, "r", encoding="utf-8") as f:
        lang_mapping = json.load(f)

    lang_counts = {}
    total_rows = 0

    with open(train_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) < 2:
                continue
            lang_code = row[1].strip()
            if lang_code not in lang_mapping:
                continue
            lang_counts[lang_code] = lang_counts.get(lang_code, 0) + 1
            total_rows += 1

    if total_rows == 0:
        print("No rows found in the training file matching the language mapping.")
        sys.exit(1)

    with open(output_file, "w", encoding="utf-8") as out:
        for lang_code, lang_id in lang_mapping.items():
            count = lang_counts.get(lang_code, 0)
            ratio = count / total_rows
            out.write(f"{lang_id}\t{ratio:.6f}\n")
            print(
                f"Language {lang_code} (id {lang_id}): {count} rows, ratio: {ratio:.6f}"
            )

    print(f"Prior file written to {output_file}")


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python ./scripts/calculate_prior.py <train.tsv> <lang_mapping.json> <prior.txt>"
        )
        sys.exit(1)
    train_file, mapping_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    compute_prior(train_file, mapping_file, output_file)


if __name__ == "__main__":
    main()
