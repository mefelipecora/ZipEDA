\# ZipEDA



\[!\[PyPI](https://img.shields.io/pypi/v/zipeda.svg)](https://pypi.org/project/zipeda/)

\[!\[Python](https://img.shields.io/pypi/pyversions/zipeda.svg)](https://pypi.org/project/zipeda/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



\*\*ZipEDA\*\* is a lightweight, plug-and-play exploratory data analysis (EDA) tool for pandas DataFrames.  

It quickly summarizes your dataset, visualizes distributions, and highlights key data quality issues — all in a single call.

Use the target\_column parameter to get class-wise views.



\## Installation



```bash

pip install zipeda



\## QuickStart



import pandas as pd

from zipeda import perform\_eda



df = pd.read\_csv("your\_data.csv")

perform\_eda(df) # Without specifying a target column



\# Or include your target column to add class-wise views

perform\_eda(df, target\_column="Survived") # Example from the Titanic dataset



\## What you get



1. Dataset overview (head)
2. Shape
3. Missing values
4. Duplicated rows (with sample)
5. Boxplots for numeric features (+ by target if provided)
6. Unique counts \& “all unique” flags
7. Feature types distribution
8. Descriptive statistics
9. Target distribution (+ count plot)
10. Histograms with normal curve overlay
11. Categorical feature counts
12. Correlation heatmap



\## Requirements



1. Python ≥ 3.8
2. pandas, numpy, matplotlib, seaborn
