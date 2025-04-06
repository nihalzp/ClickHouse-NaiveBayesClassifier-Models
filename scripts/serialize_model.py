#!/usr/bin/env python3
"""
Converts a human-readable model file to a binary format.
"""

import struct
import sys


def serialize_line(line):
    """
    Serializes a single line of model data into binary format.

    Expected line format: <class_id> <ngram> <count>

    Returns:
      bytearray: Serialized binary data.
    """
    tokens = line.strip().split()
    if len(tokens) < 3:
        raise ValueError(f"Expected at least 3 tokens, got {len(tokens)}: {tokens}")

    try:
        class_id = int(tokens[0])
    except ValueError as e:
        raise ValueError(f"Invalid class id '{tokens[0]}'") from e

    try:
        count = int(tokens[-1])
    except ValueError as e:
        raise ValueError(f"Invalid count '{tokens[-1]}'") from e

    ngram = " ".join(tokens[1:-1])
    binary_data = bytearray()
    binary_data += struct.pack("i", class_id)
    ngram_bytes = ngram.encode("utf-8")
    binary_data += struct.pack("I", len(ngram_bytes))
    binary_data += ngram_bytes
    binary_data += struct.pack("i", count)
    return binary_data


def convert_model_to_binary(input_file, output_file):
    """
    Converts the model file from text to binary format.

    Parameters:
      input_file (str): Path to the human-readable model file.
      output_file (str): Path where the binary model will be written.
    """
    binary_output = bytearray()
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                binary_output.extend(serialize_line(line))
            except Exception as e:
                print(f"Error processing line: {line.strip()} -> {e}")
                continue

    with open(output_file, "wb") as f_out:
        f_out.write(binary_output)
    print(f"Conversion complete. Written binary model to '{output_file}'.")


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python ./scripts/serialize_model.py <input_model.txt> <output_model.bin>"
        )
        sys.exit(1)
    input_file, output_file = sys.argv[1], sys.argv[2]
    convert_model_to_binary(input_file, output_file)


if __name__ == "__main__":
    main()
