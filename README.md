# ch-nb-accuracy-test

## Data Attribution

The files in the `data.zip` contain sentence data from [Tatoeba](https://tatoeba.org).  
This data is licensed under the [CC-BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) license.

## Usage

Make sure to unzip the `data.zip` file first, and update your clickhouse-client path in `config.sh`.

### `split_dataset.py`
Combines all TSV files from a specified directory, shuffles the lines, and splits the data into training and testing files based on a given split ratio.

**Usage:**
```bash
python3 split_dataset.py <input_dir> <train_file> <test_file> <split_ratio>
```

```bash
python3 ./scripts/split_dataset.py data train.tsv test.tsv 0.8
```

- `<input_dir>`: Directory containing TSV files to be combined.
- `<train_file>`: Output file for training data.
- `<test_file>`: Output file for testing data.
- `<split_ratio>`: Ratio of training data to total data (e.g., 0.8 for 80% training, 20% testing).
  
---

### `encode_ngram_model.py`
Encodes an n-gram model from the training data. It reads a TSV file, processes each sentence (adding start/end tokens), generates n-grams, and writes counts to a model file.

**Usage:**
```bash
python3 encode_ngram_model.py <train_file> <encoded_model> <n> <lang_mapping>
```

```bash
python3 ./scripts/encode_ngram_model.py train.tsv model.txt 3 lang_mapping.json
```

- `<train_file>`: TSV file with training data (for example, outputted `train_file` from `split_dataset.py`).
- `<encoded_model>`: File to write the n-gram model.
- `<n>`: The n-gram length (integer).
- `<lang_mapping>`: JSON file mapping language codes to class IDs.

---

### `serialize_model.py`
Converts a human-readable model file into a binary format to be used by ClickHouse.

**Usage:**
```bash
python3 serialize_model.py <input_model> <output_model>
```

```bash
python3 ./scripts/serialize_model.py model.txt model.bin
```

- `<input_model>`: Text file containing encoded model data (for example, outputted `encoded_model` from `encode_ngram_model.py`).
- `<output_model>`: Output binary file.

---

### `calculate_prior.py`
Calculates and writes the prior probability for each language based on the training dataset.

**Usage:**
```bash
python3 calculate_prior.py <train_file> <lang_mapping> <prior_file>
```

```bash
python3 ./scripts/calculate_prior.py train.tsv lang_mapping.json prior.txt
```

- `<train_file>`: TSV file with training data (for example, outputted `train_file` from `split_dataset.py`).
- `<lang_mapping>`: JSON file mapping language codes to class IDs.
- `<prior_file>`: Output file where language priors are written.

---

### `prepare_bulk_input.py`
Prepares a bulk input file from test data to pass to ClickHouse for prediction.

**Usage:**
```bash
python3 prepare_bulk_input.py <test_file> <lang_mapping> <model_name> <out_file>
```

```bash
python3 ./scripts/prepare_bulk_input.py test.tsv lang_mapping.json lang_model input.tsv
```

- `<test_file>`: TSV file with test data (columns: `<sentence_id>`, `<lang_code>`, `<sentence>`).
- `<lang_mapping>`: JSON file mapping language codes to numeric IDs.
- `<model_name>`: Name of the model to be used with `naiveBayesClassifier(model_name, ...)`.
- `<out_file>`: Output file for the prepared bulk input.

---

### `predict.sh`
Executes a prediction pipeline using ClickHouse and a naive Bayes classifier.

**Usage:**
```bash
./run_prediction.sh <input_file> <prediction_file>
```

```bash
./scripts/run_prediction.sh input.tsv predictions.tsv
```
- `<input_file>`: TSV file with input data for prediction (for example, outputted `out_file` from `prepare_bulk_input.py`).
- `<prediction_file>`: Output file for predictions from ClickHouse.

---

### `evaluate_accuracy.py`
Evaluates classification accuracy overall and per language using test data and predictions.

**Usage:**
```bash
python3 evaluate_accuracy.py <test_file> <predictions_file> <lang_mapping> <lang_names>
```

```bash
python3 ./scripts/evaluate_accuracy.py test.tsv predictions.tsv lang_mapping.json lang_names.json
```

- `<test_file>`: TSV file with test data (for example, outputted `test_file` from `split_dataset.py`).
- `<predictions_file>`: TSV file with predictions from ClickHouse (for example, outputted `prediction_file` from `predict.sh`).
- `<lang_mapping>`: JSON file mapping language codes to class IDs.
- `<lang_names>`: JSON file mapping language codes to human-readable names.
---
