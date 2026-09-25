# MineIQ Data Links and Download Guide

Here are all the links you need for MineIQ, organized by dataset.

## 1. HIDSAG Dataset (Your Primary Data Source)
This is the hyperspectral dataset with real metallurgical ground truth. It has 5 subsets.

*   **Main Collection Page (Figshare):** [https://doi.org/10.6084/m9.figshare.c.5983921.v1](https://doi.org/10.6084/m9.figshare.c.5983921.v1)
    *(This is the master collection. From here you can access all 5 subsets.)*

### Direct Links to Individual Subsets
| Subset | What It Contains | Direct Link |
| :--- | :--- | :--- |
| **GEOMET** | 146 samples with Cu rec, Mo rec, pH, lime cons, WI | Search "HIDSAG GEOMET Figshare" |
| **PORPHYRY** | 28 samples with known mineral mixtures | [PORPHYRY Data](https://springernature.figshare.com/articles/dataset/HIDSAG_Hyperspectral_Image_Database_for_Supervised_Analysis_in_Geometallurgy_-_PORPHYRY_data/19726822) |
| **MINERAL1** | 99 samples with 33 QEMSCAN mineral variables | [MINERAL1 Data](https://springernature.figshare.com/articles/dataset/HIDSAG_Hyperspectral_Image_Database_for_Supervised_Analysis_in_Geometallurgy_-_MINERAL1_data/19726804) |
| **MINERAL2** | 20 samples with XRD mineralogy | [MINERAL2 Data](https://springernature.figshare.com/articles/dataset/HIDSAG_Hyperspectral_Image_Database_for_Supervised_Analysis_in_Geometallurgy_-_MINERAL2_data/19726801) |
| **GEOCHEM** | 28 samples with 18 XRF elements | [GEOCHEM Data](https://springernature.figshare.com/articles/dataset/HIDSAG_Hyperspectral_Image_Database_for_Supervised_Analysis_in_Geometallurgy_-_GEOCHEM_data/19726807) |

### HIDSAG Python Library (For Loading Data)
*   **GitHub:** [https://github.com/alges/hidsag](https://github.com/alges/hidsag)
*   This library is essential for loading the HDF5 files and metadata. Person 1 will use this.

### File Format Inside Each Subset
Each subset ZIP contains:
*   Sample folders (e.g., `GMET-0001/`)
    *   `metadata.json` — response variables (Cu rec, Mo rec, etc.)
    *   Measurement folders (e.g., `01/`, `02/`)
        *   `swir_low.h5`, `vnir_low.h5`, `vnir_high.h5` — hyperspectral data
        *   `swir_low.png`, `vnir_low.png`, `vnir_high.png` — RGB previews
*   Spreadsheet (`GEOMET.xlsx`, etc.) — summary of all samples

---

## 2. Minet v2 Dataset (Optional Validation Only)
This is the 5,640-image mineral classification dataset. Use only as a transferability check — not the primary pipeline.

*   **Kaggle Dataset:** [Minerals Identification Classification](https://www.kaggle.com/datasets/youcefattallah97/minerals-identification-classification)
*   **What it contains:** 5,640 images across 7 mineral classes: Biotite, Bornite, Chrysocolla, Malachite, Muscovite, Pyrite, Quartz.

**Download code:**
```python
import kagglehub
path = kagglehub.dataset_download("youcefattallah97/minerals-identification-classification")
print("Path to dataset files:", path)
```
*   **Source Code & Paper (GitHub):** [https://github.com/YoucefAttallah/Minet_V2](https://github.com/YoucefAttallah/Minet_V2)

---

## 3. Flotation Plant Data (For Decision Engine Validation)
These datasets have real plant process variables (reagent flow, pH, air flow) but they are not paired with HIDSAG mineralogy. Use them to understand what control variables exist in a real plant.

### Kaggle: Quality Prediction in a Mining Process
*   **Link:** [Quality Prediction in a Mining Process](https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process)
*   **What it contains:** Real iron ore flotation plant data from March–September 2017. Over 400,000 records sampled every 20 seconds.
*   **Key columns:**
    *   `% Silica Feed`, `% Iron Feed` (quality measures)
    *   `Ore Pulp Flow`, `Starch Flow`, `Amina Flow` (reagent dosages)
    *   `Ore Pulp pH`, `Ore Pulp Density`
    *   `Air Flow` (7 flotation columns), `Column Levels`
    *   **Target:** `% Silica Concentrate` (impurity level)
*   **Why use it:** This shows what real flotation control variables look like. Use it to design your `rules.yaml` based on realistic plant parameters.

### Other Mining Process Datasets
| Dataset | Link | What It Contains |
| :--- | :--- | :--- |
| **Metalúrgica Data** | [GitHub Repo](https://github.com/elqvixote/metalurgica-data) | Synthetic flotation datasets, CC BY 4.0 |
| **HZDR Flotation Kinetics** | [HZDR Database](https://www.hzdr.de/db/!Publications?pNid=head&pSelMenu=0&pSelTitle=33111) | Flotation kinetics + water composition data |

---

## 4. Quick Download Checklist

### For Person 1 (Data Lead)
- [ ] Download HIDSAG GEOMET (146 samples + recovery data)
- [ ] Download HIDSAG PORPHYRY (28 samples + mineral mixtures)
- [ ] Download HIDSAG MINERAL1 (99 samples + 33 mineral variables)
- [ ] Install hidsag library: `pip install git+https://github.com/alges/hidsag.git`
- [ ] Download Kaggle flotation dataset (for reference only)

### For Person 2 (Mineral AI Lead)
- [ ] Verify HIDSAG PORPHYRY and MINERAL1 are loaded correctly
- [ ] (Optional) Download Minet v2 for transfer validation

### For Person 3 (Process Lead)
- [ ] Verify HIDSAG GEOMET is loaded correctly
- [ ] Review Kaggle flotation dataset to understand control variables

---

## 5. Important Notes
1. **HIDSAG is your primary dataset.** Everything comes from it. Minet v2 is optional validation only.
2. **The HIDSAG Python library is required.** It handles the HDF5 loading and metadata parsing. Without it, you'll waste hours on file format issues.
3. **HIDSAG file sizes:** Each subset ZIP is 1–5 GB. Total download is approximately 10–15 GB. Plan your disk space.
4. **Kaggle flotation dataset is NOT paired with HIDSAG.** Do not try to join them. Use it only to understand what real flotation control variables look like when designing your decision rules.
5. All HIDSAG data is free under Creative Commons license. Cite *Ehrenfeld et al., 2023, Scientific Data*.
