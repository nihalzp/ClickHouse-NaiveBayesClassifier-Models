#!/usr/bin/env python3
"""
Combines multiple TSV files from an input directory and splits them into training and testing datasets.
Then creates class mapping and prior probability files based on the training data.
"""

import sys
import os
import random
import json


def combine_and_split_files(input_dir, train_file, test_file, split_ratio=0.8):
    """
    Combines all TSV files in the input directory and splits them into train and test files.

    Parameters:
      input_dir (str): Directory containing TSV files.
      train_file (str): Output file for training data.
      test_file (str): Output file for testing data.
      split_ratio (float): Fraction of lines to use for training.
    """
    with open(train_file, "w", encoding="utf-8") as train_out, open(
        test_file, "w", encoding="utf-8"
    ) as test_out:
        for filename in sorted(os.listdir(input_dir)):
            if not filename.endswith(".tsv"):
                continue
            filepath = os.path.join(input_dir, filename)
            print(f"Processing file: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    continue
                random.shuffle(lines)
                train_cutoff = int(len(lines) * split_ratio)
                train_out.writelines(lines[:train_cutoff])
                test_out.writelines(lines[train_cutoff:])
                print(
                    f"  {len(lines)} lines: {train_cutoff} training, {len(lines) - train_cutoff} testing"
                )


def create_class_mapping_and_prior(train_file, class_id_json, prior_file):
    """
    Reads the training file to compute the frequency of each unique value in the first column.
    Generates a mapping (0 to n-1) and writes two files:
      - class_id.json: JSON file mapping each class (first column value) to an id.
      - prior.txt: Each line contains the class name, its numeric id, and the ratio it appears in the file.
    """
    freq = {}
    total = 0
    with open(train_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            columns = line.split("\t")
            class_val = columns[0]
            freq[class_val] = freq.get(class_val, 0) + 1
            total += 1

    # Create a mapping from class value to an ID, sorting to ensure consistency
    labels = sorted(freq.keys())
    mapping = {label: idx for idx, label in enumerate(labels)}

    # Write the mapping to a JSON file
    with open(class_id_json, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Write the prior probabilities to a text file
    with open(prior_file, "w", encoding="utf-8") as f:
        for label in labels:
            ratio = freq[label] / total
            f.write(f"{label}\t{mapping[label]}\t{ratio}\n")


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python ./scripts/split_dataset.py <input_dir> <train_file> <test_file> <split_ratio>"
        )
        sys.exit(1)
    input_dir = sys.argv[1]
    train_file = sys.argv[2]
    test_file = sys.argv[3]
    split_ratio_str = sys.argv[4]
    try:
        split_ratio = float(split_ratio_str)
        if not (0 < split_ratio < 1):
            raise ValueError
    except ValueError:
        print("Error: split_ratio must be a float between 0 and 1.")
        sys.exit(1)

    combine_and_split_files(input_dir, train_file, test_file, split_ratio)
    print("Shuffled and combined train and test TSV files created.")

    # Create class mapping and prior files based on the training file
    create_class_mapping_and_prior(train_file, "class_id.json", "prior.txt")
    print("Class mapping and prior probability files created: class_id.json, prior.txt")


if __name__ == "__main__":
    main()
