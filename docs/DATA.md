# Data

## Minet v2
Put your unzipped Minet v2 data in `data/raw/minet_v2/`.
Ensure it has the folder structure with classes and the `Minerals_5640.csv`.

## HIDSAG
Put your HIDSAG `.h5` files and metadata in `data/hidsag/`.

Sample-level split logic in `src/data/splits.py` guarantees no leakage between different crops of the same sample.
