## Performance

Tatoeba's sentences data from 8 different languages were used to create the model. The training dataset includes **80% of the data** – a total of **4,014,690 sentences**. The test set contains **1,003,675 sentences**.


### **Mode**: UTF-8 Code Point

#### Unigram
Model Size: 100 KB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 99.94%  | 15,132             | 15,141          |
| German           | 89.63%  | 128,774            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 95.08%  | 375,244            | 394,642         |
| French           | 89.71%  | 118,639            | 132,246         |
| Russian          | 100.00% | 223,964            | 223,964         |
| Spanish          | 86.10%  | 71,321             | 82,835          |
| **Overall**      | **94.08%** | **984,241**       | **1,003,675**   |

#### Bigram
Model Size: 2.7 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 99.96%  | 15,135             | 15,141          |
| German           | 99.30%  | 142,671            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 99.44%  | 392,437            | 394,642         |
| French           | 98.87%  | 130,751            | 132,246         |
| Russian          | 100.00% | 223,963            | 223,964         |
| Spanish          | 98.84%  | 81,875             | 82,835          |
| **Overall**      | **99.43%** | **997,029**       | **1,003,675**   |

#### Trigram
Model Size: 9.7 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 99.97%  | 3,156              | 3,157           |
| Mandarin Chinese | 99.93%  | 15,130             | 15,141          |
| German           | 99.84%  | 143,452            | 143,677         |
| Greek            | 99.98%  | 8,011              | 8,013           |
| English          | 99.88%  | 394,180            | 394,642         |
| French           | 99.69%  | 131,841            | 132,246         |
| Russian          | 100.00% | 223,961            | 223,964         |
| Spanish          | 99.83%  | 82,698             | 82,835          |
| **Overall**      | **99.88%** | **1,002,429**     | **1,003,675**   |
