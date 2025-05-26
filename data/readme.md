## 📦 Dataset

We release **100 ImageNet papers** with page-level ground-truth labels.

```

data/
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
df = pd.read_csv('data/dev_labels.csv')
print(df.head(8))
````

```
       arxiv_name  top1_acc  
0   1312.6229v4.pdf     85.82
1   1406.2732v1.pdf    404.00
2   1412.0296v1.pdf    404.00
3   1412.6598v2.pdf    404.00
4  1502.03167v3.pdf    404.00
5  1503.01224v2.pdf    404.00
6  1506.04701v3.pdf    404.00
7  1510.00921v6.pdf    404.00   
```

`404` → metric absent (e.g.\ only Top-5 or validation split).

> All PDFs are distributed for research and benchmarking only; copyright remains with the original publishers.
