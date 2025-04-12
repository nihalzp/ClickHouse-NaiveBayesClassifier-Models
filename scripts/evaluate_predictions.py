#!/usr/bin/env python3
"""
Evaluates predictions from ClickHouse.
Usage:
  python evaluate_predictions.py <test.tsv> <model_name> <class_id.json> <results_file> <directory>

Workflow:
  1. Reads a test.tsv file with two tab-separated columns: <lang_name> <sentence>
  2. Creates with_sentence_id.tsv in the given directory (columns: sentence_id, lang_name, sentence)
  3. Creates bulk_input.tsv in the given directory (columns: sentence_id, model_name, sentence)
     where model_name is provided as an argument to be used in the ClickHouse prediction.
  4. Calls an external bash script (predict.sh) that uses ClickHouse to read
     bulk_input.tsv and produce predictions.tsv (columns: sentence_id, input, predicted_class)
  5. Uses the class mapping (from class_id.json) to compare predicted classes to true labels.
  6. Computes overall and per-class accuracy.
  7. Writes the results in the results_file.
"""

import sys
import os
import json
import subprocess
from collections import defaultdict


def load_test_file(test_file):
    """
    Read test.tsv (two columns: lang, sentence) and attach incremental sentence_id.
    """
    data = []
    sentence_id = 1
    with open(test_file, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.rstrip("\n")
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            lang = parts[0].strip()
            sentence = parts[1].strip()
            data.append((sentence_id, lang, sentence))
            sentence_id += 1
    return data


def write_with_sentence_id(data, outfile):
    """
    Write TSV file with columns: sentence_id, lang, sentence.
    """
    with open(outfile, "w", encoding="utf-8", newline="\n") as fout:
        for rec in data:
            # rec is a tuple: (sentence_id, lang, sentence)
            line = f"{rec[0]}\t{rec[1]}\t{rec[2]}"
            fout.write(line + "\n")


def write_bulk_input(data, model_name, outfile):
    """
    Write TSV file with columns: sentence_id, model_name, sentence.
    """
    with open(outfile, "w", encoding="utf-8", newline="\n") as fout:
        for sentence_id, _, sentence in data:
            line = f"{sentence_id}\t{model_name}\t{sentence}"
            fout.write(line + "\n")


def run_clickhouse_prediction(bulk_input_path, predictions_path):
    """
    Call the external bash prediction script.
    The script is assumed to have the following usage:
      ./scripts/predict.sh <input_file> <prediction_file>
    and it will write the predictions TSV to <prediction_file>.
    """
    bash_script = "./scripts/predict.sh"
    if not os.path.isfile(bash_script):
        print(f"Error: Prediction script '{bash_script}' not found.", file=sys.stderr)
        sys.exit(1)

    cmd = ["bash", bash_script, bulk_input_path, predictions_path]
    print("Running ClickHouse prediction...")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Prediction script failed: {e}", file=sys.stderr)
        sys.exit(1)


def load_predictions(predictions_path):
    """
    Load predictions from the TSV file produced by ClickHouse.
    Each line is expected to be: sentence_id, input, predicted_class.
    """
    preds = {}
    with open(predictions_path, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.rstrip("\n")
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            try:
                sid = int(parts[0].strip())
            except ValueError:
                continue
            predicted_class = parts[2].strip()
            preds[sid] = predicted_class
    return preds


def compute_accuracy(data, predictions, class_mapping):
    """
    Compare true language with predicted classes.
    data is list of (sentence_id, true_lang, sentence).

    The class_mapping is a dict mapping language code to numeric id.
    We invert it to map numeric id (as a string) to language code.

    Returns: overall_accuracy (float), per_class_stats dict mapping language -> (correct, total),
             and predicted_counts dict mapping language -> predicted count.
    """
    # Invert mapping: numeric id (as string) -> language code.
    inv_mapping = {str(v): k for k, v in class_mapping.items()}
    total = 0
    correct = 0
    per_class_stats = defaultdict(lambda: [0, 0])  # true lang -> [correct, total]
    predicted_counts = defaultdict(
        int
    )

    # For each test sentence, count the total and update correct if predicted matches true label
    for sid, true_lang, _ in data:
        total += 1
        per_class_stats[true_lang][1] += 1
        if sid not in predictions:
            print(f"Warning: sentence_id {sid} not found in predictions; skipping.")
            exit(1)
        predicted_id = predictions[sid]
        predicted_lang = inv_mapping.get(predicted_id, None)
        if predicted_lang is None:
            print(f"Warning: predicted class '{predicted_id}' not in mapping; skipping.")
            exit(1)
        predicted_counts[predicted_lang] += 1
        if predicted_lang == true_lang:
            correct += 1
            per_class_stats[true_lang][0] += 1

    overall_accuracy = correct / total if total > 0 else 0.0
    return overall_accuracy, per_class_stats, predicted_counts


def write_results(
    results_file, overall_accuracy, per_class_stats, predicted_counts, class_mapping
):
    """
    Write results to a text file.
    Format:
      Overall Accuracy: X%
      For each class:
         Language: <lang> (ID: <id>) - Accuracy: Y% (correct/total) - Predictions: Z
    """
    with open(results_file, "w", encoding="utf-8") as fout:
        fout.write(f"Overall Accuracy: {overall_accuracy * 100:.2f}%\n")
        fout.write("Per-class accuracy:\n")
        for lang, (correct, total) in sorted(per_class_stats.items()):
            lang_id = class_mapping.get(lang, "N/A")
            accuracy = (correct / total * 100) if total > 0 else 0.0
            predicted = predicted_counts.get(lang, 0)
            fout.write(
                f"Language: {lang} (ID: {lang_id}) - Accuracy: {accuracy:.2f}% ({correct}/{total}) - Predictions: {predicted}\n"
            )
    with open(results_file, "r", encoding="utf-8") as fin:
        for line in fin:
            print(line.strip())


def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python evaluate_predictions.py <test.tsv> <model_name> <class_id.json> <results_file> <directory>"
        )
        sys.exit(1)

    test_file = sys.argv[1]
    model_name = sys.argv[2]
    class_id_json = sys.argv[3]
    results_file_name = sys.argv[4]
    directory = sys.argv[5]

    os.makedirs(directory, exist_ok=True)

    with_sentence_id_path = os.path.join(directory, "with_sentence_id.tsv")
    bulk_input_path = os.path.join(directory, "bulk_input.tsv")
    predictions_path = os.path.join(directory, "predictions.tsv")
    results_file = os.path.join(directory, results_file_name)

    # Process test data
    data = load_test_file(test_file)
    write_with_sentence_id(data, with_sentence_id_path)
    write_bulk_input(data, model_name, bulk_input_path)

    # Run ClickHouse prediction
    run_clickhouse_prediction(bulk_input_path, predictions_path)

    # Load predictions
    predictions = load_predictions(predictions_path)

    # Load class mapping
    with open(class_id_json, "r", encoding="utf-8") as f:
        class_mapping = json.load(f)

    # Compute accuracy
    overall_accuracy, per_class_stats, predicted_counts = compute_accuracy(
        data, predictions, class_mapping
    )

    # Write results
    write_results(
        results_file, overall_accuracy, per_class_stats, predicted_counts, class_mapping
    )

    print("Evaluation complete.")
    print(f"Results written to {results_file}")


if __name__ == "__main__":
    main()
