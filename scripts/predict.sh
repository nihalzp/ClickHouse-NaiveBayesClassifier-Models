#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_file> <prediction_file>"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

source config.sh
echo "Using ClickHouse client: $CLICKHOUSE_CLIENT"

$CLICKHOUSE_CLIENT -q "DROP TABLE IF EXISTS nb_test;"

$CLICKHOUSE_CLIENT -q "
    CREATE TABLE nb_test
    (
        id Int32,
        model String,
        input String
    )
    ENGINE = Memory;
"

$CLICKHOUSE_CLIENT -q "INSERT INTO nb_test FORMAT TabSeparated" < "$INPUT_FILE"

$CLICKHOUSE_CLIENT -q "
    SELECT id, input, naiveBayesClassifier(model, input) AS predicted_class
    FROM nb_test
    FORMAT TSV
" > "$OUTPUT_FILE"

$CLICKHOUSE_CLIENT -q "DROP TABLE IF EXISTS nb_test;"

