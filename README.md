# ch-nb-accuracy-test

## Data Attribution

The files in the `data.zip` contain sentence data from [Tatoeba](https://tatoeba.org).  
This data is licensed under the [CC-BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) license.

## Usage

Make sure to unzip the `data.zip` file first, and update your clickhouse-client path in `config.sh`.

### `split_dataset.py`
Combines all TSV files from a specified directory, shuffles the lines, and splits the data into training and testing files based on a given split ratio.

TSV input file format:

`<lang_code> \t <sentence>`
- `<lang_code>`: Language code (e.g., `en`, `fr`).
- `<sentence>`: The sentence in the respective language.

**Usage:**
```bash
python3 split_dataset.py <input_dir> <train_file.tsv> <test_file.tsv> <split_ratio>
```

```bash
python3 ./scripts/split_dataset.py data train.tsv test.tsv 0.8
```

- `<input_dir>`: Directory containing TSV files to be combined.
- `<train_file.tsv>`: Output file for training data.
- `<test_file.tsv>`: Output file for testing data.
- `<split_ratio>`: Ratio of training data to total data (e.g., 0.8 for 80% training, 20% testing).
  
---

### `create_ngram_model_token.py`
Creates a serialized binary model file for `token` mode to be used by ClickHouse.

**Usage:**
```bash
python3 ./scripts/create_ngram_model_token.py <train.tsv> <output_model.bin> <n> <lang_mapping.json>
```

```bash
python3 create_ngram_model_token.py train.tsv lang_token_1.bin 1 class_id.json
```

- `<train.tsv>`: TSV file with training data (for example, outputted `train_file.tsv` from `split_dataset.py`).
- `<output_model.bin>`: Output file for the serialized model.
- `<n>`: N-gram size (1 for unigrams, 2 for bigrams, etc.).
- `<lang_mapping.json>`: JSON file mapping language codes to numeric IDs. (for example, outputted `lang_mapping.json` from `split_dataset.py`).                       

---

### `create_ngram_model_codepoint.py`
Creates a serialized binary model file for `codepoint` mode to be used by ClickHouse.

Same as `create_ngram_model_token.py`, but for `codepoint` mode.
---

### `create_ngram_model_byte.py`
Creates a serialized binary model file for `byte` mode to be used by ClickHouse.

Same as `create_ngram_model_token.py`, but for `byte` mode.
---

### `evaluate_predictions.py`
Evaluates the predictions made by a model on a test dataset. It compares the predicted language codes with the actual language codes in the test dataset and calculates the accuracy.

**Usage:**
```bash
python3 ./scripts/evaluate_predictions.py <test.tsv> <model_name> <class_id.json> <results_file> <directory
```

```bash
python3 ./scripts/evaluate_predictions.py test.tsv lang_token_1.bin class_id.json results.txt ./token_1_result
```

- `<test.tsv>`: TSV file with test data (for example, outputted `test_file.tsv` from `split_dataset.py`).
- `<model_name>`: Name of the model specified in the .xml file (e.g., `lang_token_1`).
- `<class_id.json>`: JSON file mapping language codes to numeric IDs (for example, outputted `lang_mapping.json` from `split_dataset.py`).
- `<results_file>`: Output file for the evaluation results.
- `<directory>`: Directory where the results will be saved.
