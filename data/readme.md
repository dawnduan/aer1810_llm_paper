## 📦 Dataset

We release **100 ImageNet papers** with page-level ground-truth labels.

```

data/
├── papers/                # 100 PDFs named by arXiv ID  (120 MB zip)
├── dev\_labels.csv         # gold labels (see columns below)
└── dev\_labels.json        # same content in JSON

````

| Column | Description |
|--------|-------------|
| `arxiv_name` | PDF filename (`1312.6229v4.pdf`, …) |
| `top1_acc`   | Canonical Top-1 ImageNet accuracy **(in %)**; `404` means the paper never reports a usable value |

#### Quick peek
```python
import pandas as pd
df = pd.read_csv('data/groundtruth_120_kdd25_v1.csv')
print(df.head(8))
````

```
       arxiv_name  top1_acc  
0  1312.6229v4.pdf    85.82     
1  1406.2732v1.pdf   404.00    
2  1502.03167v3.pdf   404.00     
3  1607.00501v1.pdf    75.53     
4  1610.02357v3.pdf    79.00     
```

`404` → metric absent (e.g.\ only Top-5 or validation split).

#### Download links

| File                | Size   | Link                                                                                                          |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------------- |
| PDFs (`papers.zip`) | 120 MB | [https://zenodo.org/record/xxxx/files/papers.zip](https://zenodo.org/record/xxxx/files/papers.zip)            |
| `dev_labels.csv`    | 34 kB  | [https://zenodo.org/record/xxxx/files/dev\_labels.csv](https://zenodo.org/record/xxxx/files/dev_labels.csv)   |
| `dev_labels.json`   | 46 kB  | [https://zenodo.org/record/xxxx/files/dev\_labels.json](https://zenodo.org/record/xxxx/files/dev_labels.json) |

> All PDFs are distributed for research and benchmarking only; copyright remains with the original publishers.
