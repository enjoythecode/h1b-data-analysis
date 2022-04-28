# H-1B Data Analysis

Analysis of data available on the [USCIS H-1B Data files page](https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub/h-1b-employer-data-hub-files).

A mirror of the data files is available under the `data/` directory.

# Reproduction Steps

Make sure you have a version of Python 3 installed on your machine. The plots for the paper were created with Python version 3.7

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python analyze.py
```

The resulting files will be populated in the `result/` folder