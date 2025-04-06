#!/usr/bin/env python3
"""
Encodes an ngram model from training data in the format:
<class_id> <ngram> <count>
"""

import sys
import csv
import collections
from util.helpers import load_language_mapping


def generate_ngrams(words, n):
    """
    Generates n-grams from a list of words.

    Parameters:
      words (list): List of tokens.
      n (int): The n-gram length.

    Returns:
      list: List of n-grams as strings.
    """
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


def encode_ngram_model(train_file, output_model_file, n, lang_mapping_file):
    """
    Reads training data and writes the n-gram model counts to a file.

    Model file format:
    <class_id> <ngram> <count>

    Parameters:
      train_file (str): Path to the training TSV file.
      output_model_file (str): Path to the output model file.
      n (int): n-gram length.
      lang_mapping_file (str): Path to the JSON file with language mapping.
    """
    lang_mapping = load_language_mapping(lang_mapping_file)
    model_counts = collections.defaultdict(int)

    with open(train_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) < 3:
                continue
            lang_code = row[1].strip()
            sentence = row[2].strip()
            if not sentence:
                continue
            if lang_code not in lang_mapping:
                print(f"Warning: language code '{lang_code}' not in mapping; skipping.")
                continue
            class_id = lang_mapping[lang_code]
            # Add (n-1) start and end tokens.
            start_tokens = " ".join(["<s>"] * (n - 1))
            end_tokens = " ".join(["</s>"] * (n - 1))
            sentence = f"{start_tokens} {sentence} {end_tokens}"
            words = sentence.split()
            if len(words) < n:
                continue
            for ngram in generate_ngrams(words, n):
                model_counts[(class_id, ngram)] += 1

    with open(output_model_file, "w", encoding="utf-8") as out_f:
        for (class_id, ngram), count in model_counts.items():
            out_f.write(f"{class_id} {ngram} {count}\n")

    print(
        f"Model file '{output_model_file}' generated with {len(model_counts)} tuples."
    )


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python ./scripts/encode_ngram_model.py <train.tsv> <output_model.txt> <n> <lang_mapping.json>"
        )
        sys.exit(1)

    train_file = sys.argv[1]
    output_model_file = sys.argv[2]
    n_str = sys.argv[3]
    lang_mapping_file = sys.argv[4]

    try:
        n = int(n_str)
    except ValueError:
        print("n must be an integer.")
        sys.exit(1)
    encode_ngram_model(train_file, output_model_file, n, lang_mapping_file)


if __name__ == "__main__":
    main()
