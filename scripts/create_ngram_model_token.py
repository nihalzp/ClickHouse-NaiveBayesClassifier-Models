#!/usr/bin/env python3
"""
Encodes an n-gram model from training data and serializes it to a binary file.
Reads training data in TSV format where each line is:
   <language_code> <text ...>
Uses a language mapping file (JSON) to convert language codes to class IDs.

The n-gram model is built as follows:
  - For each document, (n-1) start tokens (provided) are added at the beginning and
    (n-1) end tokens (provided) are added at the end. These tokens are hard-coded as:
       start token: <s>
       end token:   </s>
  - All n-grams are generated and their counts computed.
  - The binary format for each tuple is:
      <unsigned int: class_id>
      <unsigned int: length of ngram in bytes>
      <ngram in utf-8 bytes>
      <unsigned int: count>

Usage:
  python create_ngram_model_token.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>
"""

import sys
import collections
import struct
from util.helpers import load_language_mapping  # assumes your helper exists


def generate_ngrams(words, n):
    """
    Generates n-grams from a list of words.
    """
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


def encode_ngram_model(train_file, n, lang_mapping_file):
    """
    Reads training data and returns a dictionary with keys (class_id, ngram) and values as counts.
    The provided start_token and end_token are repeated (n-1) times as boundaries.
    """
    lang_mapping = load_language_mapping(lang_mapping_file)
    model_counts = collections.defaultdict(int)

    start_token = "<s>"
    end_token = "</s>"

    with open(train_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            parts = line.split("\t")
            if len(parts) < 2:
                print(f"Warning: line '{line}' does not have enough parts; skipping.")
                continue
            lang_code = parts[0].strip()
            sentence = " ".join(parts[1:]).strip()
            if not sentence:
                print(f"Warning: empty sentence in line '{line}'; skipping.")
                continue
            if lang_code not in lang_mapping:
                print(f"Warning: language code '{lang_code}' not in mapping; skipping.")
                continue
            class_id = lang_mapping[lang_code]

            # Add (n-1) start and end tokens using the provided tokens
            start_tokens = " ".join([start_token] * (n - 1))
            end_tokens = " ".join([end_token] * (n - 1))
            sentence = f"{start_tokens} {sentence} {end_tokens}"
            words = sentence.split()
            if len(words) < n:
                continue

            for ngram in generate_ngrams(words, n):
                model_counts[(class_id, ngram)] += 1

    return model_counts


def serialize_model(model_counts, output_file):
    """
    Serializes the model counts dictionary into binary format and writes it to output_file.
    Format for each tuple:
      <unsigned int: class_id>
      <unsigned int: length of ngram (in bytes)>
      <ngram (utf-8 bytes)>
      <unsigned int: count>
    """
    binary_output = bytearray()
    for (class_id, ngram), count in model_counts.items():
        binary_output += struct.pack("I", class_id)
        ngram_bytes = ngram.encode("utf-8")
        binary_output += struct.pack("I", len(ngram_bytes))
        binary_output += ngram_bytes
        binary_output += struct.pack("I", count)

    with open(output_file, "wb") as f_out:
        f_out.write(binary_output)
    print(
        f"Conversion complete. Written binary model to '{output_file}'. Total tuples: {len(model_counts)}"
    )


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python3 create_ngram_model_token.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>"
        )
        sys.exit(1)

    train_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        n = int(sys.argv[3])
    except ValueError:
        print("Error: n must be an integer.")
        sys.exit(1)
    lang_mapping_file = sys.argv[4]
    model_counts = encode_ngram_model(train_file, n, lang_mapping_file)
    serialize_model(model_counts, output_file)


if __name__ == "__main__":
    main()
