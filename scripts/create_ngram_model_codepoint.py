#!/usr/bin/env python3
"""
Encodes an n-gram model from training data at the Unicode code point level and serializes it to a binary file.
Reads training data in TSV format where each line is:
   <language_code> <text ...>
Uses a language mapping file (JSON) to convert language codes to class IDs.

The n-gram model is built as follows:
  - For each document, (n-1) start tokens and (n-1) end tokens are added at the beginning and end,
    respectively. These tokens are hard-coded as:
       start token: U+10FFFE
       end token:   U+10FFFF
  - The sentence is split into individual Unicode (UTF-8) code points.
  - All n-grams (as contiguous sequences of code points) are generated and their counts computed.
  - The binary format for each tuple is:
      <unsigned int: class_id>
      <unsigned int: length of ngram in bytes>
      <ngram in utf-8 bytes>
      <unsigned int: count>

Usage:
  python create_ngram_model_codepoint.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>
"""

import sys
import collections
import struct
from util.helpers import load_language_mapping  # assumes your helper exists


def generate_codepoint_ngrams(codepoints, n):
    """
    Generates n-grams from a list of Unicode code points.
    Each n-gram is the concatenation of n code points.
    """
    return ["".join(codepoints[i : i + n]) for i in range(len(codepoints) - n + 1)]


def encode_ngram_model(train_file, n, lang_mapping_file):
    """
    Reads training data and returns a dictionary with keys (class_id, ngram) and values as counts.
    Instead of tokenizing by whitespace, this function tokenizes the sentence into its individual Unicode code points.
    Padding tokens for boundaries are hard-coded as:
      start token: U+10FFFE
      end token:   U+10FFFF
    Each is repeated (n-1) times as boundaries.
    """
    lang_mapping = load_language_mapping(lang_mapping_file)
    model_counts = collections.defaultdict(int)

    start_token = "\U0010fffe"
    end_token = "\U0010ffff"

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

            # Create start and end boundary tokens repeated (n-1) times.
            start_tokens = [start_token] * (n - 1)
            end_tokens = [end_token] * (n - 1)

            # Split the sentence into individual Unicode code points.
            codepoints = list(sentence)
            tokens = start_tokens + codepoints + end_tokens

            if len(tokens) < n:
                continue

            ngrams = generate_codepoint_ngrams(tokens, n)
            for ngram in ngrams:
                model_counts[(class_id, ngram)] += 1

        # write out the model counts to human-readable format
    with open("model_counts.txt", "w", encoding="utf-8") as f_out:
        for (class_id, ngram), count in model_counts.items():
            f_out.write(f"{class_id}\t{ngram}\t{count}\n")

    return model_counts


def serialize_model(model_counts, output_file):
    """
    Serializes the model counts dictionary into binary format and writes it to output_file.
    Format for each tuple:
      <unsigned int: class_id>
      <unsigned int: length of ngram in bytes>
      <ngram in utf-8 bytes>
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
            "Usage: python create_ngram_model_codepoint.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>"
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
