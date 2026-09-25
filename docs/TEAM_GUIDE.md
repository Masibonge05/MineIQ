# Team Guide

## Person 1 (Data Lead)
**Files to edit:**
- `src/data/loader.py`
- `src/data/preprocessing.py`
- `src/data/augmentation.py`

**Expected Deliverables:**
- Working PyTorch DataLoaders for HIDSAG (5 subsets).
- Complete data preprocessing functions.

## Person 2 (Mineral AI Lead)
**Files to edit:**
- `src/models/mineral_classifier.py`
- `src/models/uncertainty.py`
- `src/training/train_classifier.py`
- `src/training/evaluate.py`
- `app/pages/4_Model_Performance.py`

**Expected Deliverables:**
- Functioning ResNet50 baseline.
- Metrics visualization in the dashboard.

## Person 3 (Process & System Lead)
**Files to edit:**
- `src/models/processability.py`
- `src/training/train_processability.py`
- `src/inference/realtime.py`
- `app/pages/2_Batch_Analysis.py`
- `app/pages/3_Realtime_Conveyor.py`

**Expected Deliverables:**
- XGBoost regression pipelines.
- Fully working Realtime UI and Batch UI.
