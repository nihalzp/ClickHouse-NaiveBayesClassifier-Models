## Performance

Tatoeba's sentences data from 8 different languages were used to create the model. The training dataset includes **80% of the data** – a total of **4,014,690 sentences**. The test set contains **1,003,675 sentences**.


### **Mode**: Token

#### Unigram
Model Size: 25 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 98.64%  | 3,114              | 3,157           |
| Mandarin Chinese | 1.18%   | 178                | 15,141          |
| German           | 99.90%  | 143,529            | 143,677         |
| Greek            | 98.23%  | 7,871              | 8,013           |
| English          | 99.95%  | 394,440            | 394,642         |
| French           | 99.52%  | 131,609            | 132,246         |
| Russian          | 99.93%  | 223,809            | 223,964         |
| Spanish          | 99.23%  | 82,200             | 82,835          |
| **Overall**      | **98.31%** | **986,750**       | **1,003,675**   |

#### Bigram
Model Size: 174 MB
| Language         | Accuracy | Correct Predictions | Total Sentences |
|------------------|--------:|--------------------:|----------------:|
| Bengali          | 92.81%  | 2,930              | 3,157           |
| Mandarin Chinese | 0.11%   | 16                 | 15,141          |
| German           | 99.81%  | 143,408            | 143,677         |
| Greek            | 97.33%  | 7,799              | 8,013           |
| English          | 99.87%  | 394,123            | 394,642         |
| French           | 99.45%  | 131,520            | 132,246         |
| Russian          | 99.72%  | 223,334            | 223,964         |
| Spanish          | 99.17%  | 82,148             | 82,835          |
| **Overall**      | **98.17%** | **985,278**       | **1,003,675**   |