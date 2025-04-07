#!/usr/bin/env python3
"""
Evaluates classification accuracy overall and per language.
"""

import sys
import json


def load_json_file(filename, description):
    """
    Loads a JSON file and returns its content.

    Parameters:
      filename (str): Path to the JSON file.
      description (str): Description for error messages.

    Returns:
      dict: Parsed JSON content.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {description} file:", e)
        sys.exit(1)


def load_test_data(test_file):
    """
    Loads test data from a tab-separated file.

    Expected format per line:
      <id>    <lang_code>    <sentence>

    Parameters:
      test_file (str): Path to the test file.

    Returns:
      dict: Mapping from test id to (lang_code, sentence).
    """
    test_data = {}
    with open(test_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            test_id = parts[0].strip()
            lang_code = parts[1].strip()
            sentence = parts[2].strip()
            test_data[test_id] = (lang_code, sentence)
    return test_data


def load_predictions(predictions_file):
    """
    Loads predictions from a tab-separated file.

    Expected format per line:
      <id>    <sentence>    <predicted_id>

    Parameters:
      predictions_file (str): Path to the predictions file.

    Returns:
      dict: Mapping from id to predicted numeric id.
    """
    predictions = {}
    with open(predictions_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            pred_id = parts[0].strip()
            try:
                predicted_id = int(parts[2].strip())
            except Exception as e:
                print("Error parsing predicted id in line:", line, e)
                continue
            predictions[pred_id] = predicted_id
    return predictions


def evaluate_accuracy(test_data, predictions, lang_mapping, lang_names):
    """
    Evaluates classification accuracy overall and per language.

    Parameters:
      test_data (dict): Mapping from sentence id to (lang_code, sentence).
      predictions (dict): Mapping from sentence id to predicted numeric id.
      lang_mapping (dict): Mapping from language code to numeric id.
      lang_names (dict): Mapping from language code to full language name.
    """
    total = 0
    correct = 0
    per_lang_total = {}
    per_lang_correct = {}
    missing_predictions = 0

    for test_id, (lang_code, _) in test_data.items():
        if test_id not in predictions:
            print(f"Missing prediction for test id: {test_id}")
            missing_predictions += 1
            continue

        true_id = lang_mapping.get(lang_code)
        if true_id is None:
            print("Unknown language code in test file:", lang_code)
            continue

        predicted_id = predictions[test_id]
        total += 1
        per_lang_total[lang_code] = per_lang_total.get(lang_code, 0) + 1

        if predicted_id == true_id:
            correct += 1
            per_lang_correct[lang_code] = per_lang_correct.get(lang_code, 0) + 1
        else:
            per_lang_correct[lang_code] = per_lang_correct.get(lang_code, 0)

    overall_accuracy = correct / total if total > 0 else 0
    print("Overall accuracy: {:.2%} ({} / {})".format(overall_accuracy, correct, total))
    print("Per-language accuracy:")
    for lang_code in sorted(per_lang_total.keys()):
        tot = per_lang_total[lang_code]
        corr = per_lang_correct.get(lang_code, 0)
        acc = corr / tot if tot else 0
        full_name = lang_names.get(lang_code, lang_code)
        print(
            "  {} ({}): {:.2%} ({} / {})".format(lang_code, full_name, acc, corr, tot)
        )
    if missing_predictions:
        print(
            "Warning: {} test IDs had no corresponding prediction.".format(
                missing_predictions
            )
        )


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python evaluate_accuracy.py <test_file> <predictions_file> <lang_mapping.json> <lang_names.json>"
        )
        sys.exit(1)

    test_file = sys.argv[1]
    predictions_file = sys.argv[2]
    lang_mapping_file = sys.argv[3]
    lang_names_file = sys.argv[4]

    lang_mapping = load_json_file(lang_mapping_file, "language mapping")
    lang_names = load_json_file(lang_names_file, "language names")
    test_data = load_test_data(test_file)
    predictions = load_predictions(predictions_file)
    evaluate_accuracy(test_data, predictions, lang_mapping, lang_names)


if __name__ == "__main__":
    main()
