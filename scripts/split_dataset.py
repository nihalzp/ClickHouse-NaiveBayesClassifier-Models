#!/usr/bin/env python3
"""
Combines multiple TSV files from an input directory and splits them into training and testing datasets.
"""

import sys
import os
import random


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


if __name__ == "__main__":
    main()
