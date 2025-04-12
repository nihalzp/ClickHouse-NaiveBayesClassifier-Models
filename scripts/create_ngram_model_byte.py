#!/usr/bin/env python3
"""
Encodes an n-gram model from training data at the byte level and serializes it to a binary file.
Reads training data in TSV format where each line is:
   <language_code> <text ...>
Uses a language mapping file (JSON) to convert language codes to class IDs.

The n-gram model is built as follows:
  - For each document, (n-1) start tokens and (n-1) end tokens are added at the beginning and end,
    respectively. These tokens are hard-coded as:
       start token: 0x01
       end token:   0xFF
  - The sentence is encoded to bytes (UTF-8) and treated as a sequence of bytes.
  - All n-grams (as contiguous sequences of bytes) are generated and their counts computed.
  - The binary format for each tuple is:
      <unsigned int: class_id>
      <unsigned int: length of ngram in bytes>
      <ngram in utf-8 bytes>
      <unsigned int: count>

Usage:
  python encode_and_serialize_ngram_model_byte.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>
"""

import sys
import collections
import struct
from util.helpers import load_language_mapping

def generate_byte_ngrams(byte_seq, n):
    """
    Generates n-grams from a bytes object.
    Each n-gram is a contiguous sequence of n bytes.
    """
    return [byte_seq[i:i+n] for i in range(len(byte_seq) - n + 1)]

def encode_ngram_model(train_file, n, lang_mapping_file):
    """
    Reads training data and returns a dictionary with keys (class_id, ngram) and values as counts.
    This function tokenizes each sentence at the byte level.
    Padding tokens for boundaries are hard-coded as:
      start token: 0x01
      end token:   0xFF
    Each is repeated (n-1) times as boundaries.
    """
    lang_mapping = load_language_mapping(lang_mapping_file)
    model_counts = collections.defaultdict(int)

    start_token = b"\x01"
    end_token = b"\xff"

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
            # Encode sentence to bytes using UTF-8
            sentence_bytes = sentence.encode("utf-8")

            # Create padded byte sequence
            padded = start_token * (n - 1) + sentence_bytes + end_token * (n - 1)

            if len(padded) < n:
                continue

            # Generate byte-level n-grams
            ngrams = generate_byte_ngrams(padded, n)
            for ngram in ngrams:
                model_counts[(class_id, ngram)] += 1
    

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
        binary_output += struct.pack("I", len(ngram))
        binary_output += ngram
        binary_output += struct.pack("I", count)

    with open(output_file, "wb") as f_out:
        f_out.write(binary_output)
    print(f"Conversion complete. Written binary model to '{output_file}'. Total tuples: {len(model_counts)}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python encode_and_serialize_ngram_model_byte.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>")
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
