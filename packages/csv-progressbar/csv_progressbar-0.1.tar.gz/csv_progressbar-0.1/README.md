# CSVProgressBar

This package provides a progress bar wrapper for the standard csv library

# Usage

To use csv reader you must specify  `ProgressBar object`, witch must have **update** method: 

```python
from csv_progress_bar import read_with_pbar

pbar = MyPbar(...) 
with open('my_file.csv') as csvfile:
    reader = read_with_pbar(csvfile, pbar)
    for row in reader:
        ...
```
When reading a csv file, the reader calls the update method of the progerss bar, where the argument is the number of readed bytes. So set the progressbar total as the file size in bytes.

Personally, I like to use [tqdm](https://github.com/tqdm/tqdm):

```python
import os
from csv_progress_bar import read_with_pbar
from tqdm import tqdm

path = 'my_file.csv'
total_size = os.path.getsize(path)
pbar = tqdm(total= total_size)
with open(path) as csvfile:
    reader = read_with_pbar(csvfile, pbar)
    for row in reader:
        ...
```

# Performance

Unfortunately, due to frequent iterations and additional function calls, reading is **~ 30% slower**

# Cooming soon

- readers objecs for pupular progressbars
- progressbar for [pandas](https://github.com/pandas-dev/pandas) reader!