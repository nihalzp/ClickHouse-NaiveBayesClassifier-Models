## Performance

Tatoeba's sentences data from 8 different languages were used to create the model. The training dataset includes **80% of the data** – a total of **4,014,690 sentences**. The test set contains **1,003,675 sentences**.

### **Mode**: Byte

#### Unigram
Model Size: 20 KB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 99.99%  | 15,139             | 15,141          |
| German           | 87.32%  | 125,459            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 96.63%  | 381,359            | 394,642         |
| French           | 87.47%  | 115,678            | 132,246         |
| Russian          | 100.00% | 223,964            | 223,964         |
| Spanish          | 83.95%  | 69,540             | 82,835          |
| **Overall**      | **93.89%** | **942,306**       | **1,003,675**   |

#### Bigram
Model Size: 396 KB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 100.00% | 15,141             | 15,141          |
| German           | 99.26%  | 142,615            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 99.50%  | 392,684            | 394,642         |
| French           | 98.74%  | 130,585            | 132,246         |
| Russian          | 100.00% | 223,964            | 223,964         |
| Spanish          | 98.79%  | 81,829             | 82,835          |
| **Overall**      | **99.43%** | **997,985**       | **1,003,675**   |

#### Trigram
Model Size: 2.6 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 100.00% | 15,141             | 15,141          |
| German           | 99.84%  | 143,444            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 99.88%  | 394,180            | 394,642         |
| French           | 99.68%  | 131,821            | 132,246         |
| Russian          | 100.00% | 223,964            | 223,964         |
| Spanish          | 99.83%  | 82,696             | 82,835          |
| **Overall**      | **99.87%** | **1,002,413**     | **1,003,675**   |

#### 4-gram
Model Size: 12 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 100.00% | 15,141             | 15,141          |
| German           | 99.96%  | 143,616            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 99.96%  | 394,484            | 394,642         |
| French           | 99.91%  | 132,125            | 132,246         |
| Russian          | 100.00% | 223,963            | 223,964         |
| Spanish          | 99.93%  | 82,781             | 82,835          |
| **Overall**      | **99.96%** | **1,003,277**     | **1,003,675**   |

#### 5-gram
Model Size: 33 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 100.00% | 15,141             | 15,141          |
| German           | 99.97%  | 143,635            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 99.97%  | 394,518            | 394,642         |
| French           | 99.94%  | 132,172            | 132,246         |
| Russian          | 100.00% | 223,963            | 223,964         |
| Spanish          | 99.97%  | 82,808             | 82,835          |
| **Overall**      | **99.97%** | **1,003,404**     | **1,003,675**   |