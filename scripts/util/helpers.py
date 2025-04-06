#!/usr/bin/env python3
import json


def load_language_mapping(mapping_file):
    """
    Loads language mapping from a JSON file.

    Parameters:
      mapping_file (str): Path to the JSON file containing language mappings.

    Returns:
      dict: Dictionary mapping language codes to class IDs.
    """
    with open(mapping_file, "r", encoding="utf-8") as f:
        return json.load(f)
