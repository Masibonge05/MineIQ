# MineIQ Data Guide

## HIDSAG Dataset
This project strictly uses the HIDSAG (Hyperspectral Images Dataset for South African Gold and Copper) dataset.
Figshare DOI: 10.6084/m9.figshare.c.5983921.v1

Place your downloaded HIDSAG data inside the `data/hidsag/` directory.

### Subsets
1. **GEOMET**: 146 samples with `cu_recovery`, `mo_recovery`, `ph`, `lime_consumption`, `bwi`.
2. **PORPHYRY**: 28 artificial mixtures with known mineral compositions (8 groups: Q1–Q8).
3. **MINERAL1**: 99 monthly composites with 33 QEMSCAN mineral abundances.
4. **MINERAL2**: 20 drill core samples with XRD mineralogy.
5. **GEOCHEM**: 28 samples with 18 XRF elements.

### Directory Structure
```text
data/
└── hidsag/
    ├── geomet/
    ├── porphyry/
    ├── mineral1/
    ├── mineral2/
    └── geochem/
```
