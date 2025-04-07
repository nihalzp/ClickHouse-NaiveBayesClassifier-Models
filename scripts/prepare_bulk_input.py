#!/usr/bin/env python3
"""
Prepares a bulk input file from test data for model processing.
"""

import sys
from util.helpers import load_language_mapping


def prepare_bulk_input(test_file, mapping_file, model_name, out_file):
    """
    Reads the test data and writes a bulk input file for the specified model.

    The test file should be a TSV with three fields per line:
      <sentence_id>    <lang_code>    <sentence>

    """
    lang_mapping = load_language_mapping(mapping_file)

    with open(test_file, "r", encoding="utf-8") as fin, open(
        out_file, "w", encoding="utf-8"
    ) as fout:
        for line in fin:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue

            sentence_id = parts[0].strip()
            lang_code = parts[1].strip()
            sentence = " ".join(parts[2:]).strip()

            if not sentence or lang_code not in lang_mapping:
                continue

            fout.write(f"{sentence_id}\t{model_name}\t{sentence}\n")


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python prepare_bulk_input.py <test.tsv> <lang_mapping.json> <model_name> <out_file>"
        )
        sys.exit(1)

    test_file, mapping_file, model_name, out_file = sys.argv[1:5]
    prepare_bulk_input(test_file, mapping_file, model_name, out_file)


if __name__ == "__main__":
    main()
