# MineIQ: Real-Time Mineral Intelligence 🚀

Welcome to the MineIQ project skeleton. This document tells each team member exactly what to build. Read it carefully before you start.

## 🛠️ Getting Started

Everyone runs these commands to set up and verify the skeleton works:

```bash
git clone https://github.com/Masibonge05/MineIQ.git
cd mineiq
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
make dashboard
```

Required Reading for Everyone:
*   `README.md` (this file)
*   `docs/TEAM_GUIDE.md`
*   `docs/ARCHITECTURE.md`
*   `docs/DATA.md`
*   `docs/DECISION_RULES.md`

## 👑 The Golden Rule

**Never push directly to main. Always work on a branch. Always open a PR.**

## 👥 Team Roles at a Glance

| Person | Role | Owns | Primary Deliverable |
| :--- | :--- | :--- | :--- |
| **Person 1** | Data & Pipeline Lead | `src/data/`, `src/inference/realtime.py`, `data/` | HIDSAG loaders + conveyor simulator |
| **Person 2** | Mineral AI Lead | `src/models/mineral_classifier.py`, `src/training/train_classifier.py` | Trained mineral classifier (≥3 phases) on HIDSAG |
| **Person 3** | Process & System Lead | `src/models/processability.py`, `src/decision/`, `app/` | Trained processability model + polished dashboard |

> Everyone shares responsibility for README updates, demo rehearsal, and presentation slides.

---

## 👷‍♂️ PERSON 1 — Data & Pipeline Lead

**Your Mission:** Make sure data flows cleanly from HIDSAG to the models to the dashboard, with no leakage, and build the conveyor simulator that makes the real-time demo possible.

### 1. HIDSAG Data Loader
*   **File:** `src/data/loader.py`
*   Complete the `HIDSAGLoader` class:
    *   Use the `hidsag` library from https://github.com/alges/hidsag
    *   Support all 5 subsets, each with its own method:
        *   `load_geomet()` → 146 samples with cu_recovery, mo_recovery, ph, lime_consumption, bwi
        *   `load_porphyry()` → 28 artificial mixtures with known mineral compositions (8 groups: Q1–Q8)
        *   `load_mineral1()` → 99 monthly composites with 33 QEMSCAN mineral abundances
        *   `load_mineral2()` → 20 drill core samples with XRD mineralogy
        *   `load_geochem()` → 28 samples with 18 XRF elements
    *   For each sample: read `metadata.json` for response variables, load VNIR / SWIR / RGB cubes from `.h5`
    *   Return a `pd.DataFrame` with `sample_id`, `vnir_path`, `swir_path`, `rgb_path`, plus subset-specific targets
*   **Acceptance test:**
    ```bash
    python -c "from src.data.loader import HIDSAGLoader; \
    loader = HIDSAGLoader('configs/config.yaml'); \
    print(loader.load_geomet().head()); \
    print(loader.load_mineral1().head())"
    ```
    Both subsets must print real rows.

### 2. Sample-Level Splits
*   **File:** `src/data/splits.py`
*   Implement `make_sample_level_splits(df, seed=42)`:
    *   CRITICAL: All crops/measurements from the same `sample_id` go to the same split
    *   Returns DataFrame with a split column: train, val, test (70/15/15 stratified)
*   Implement `assert_no_leakage(df)`:
    *   Asserts no `sample_id` appears in more than one split
    *   Raises ValueError with a clear message if leakage is found
*   **Acceptance test:**
    ```bash
    pytest tests/test_no_leakage.py -v
    ```

### 3. Preprocessing & Augmentation
*   **File:** `src/data/preprocessing.py`
    *   `preprocess_image(path, size=224)` — loads PNG/JPG, resizes, normalizes with ImageNet stats
    *   `preprocess_hsi(path, band_range)` — loads HDF5, selects VNIR or SWIR bands, normalizes per-band
    *   `extract_texture_features(image)` — returns grain size estimate, edge density, texture entropy using OpenCV
*   **File:** `src/data/augmentation.py`
    *   `get_train_transforms()` — random flip, rotation ±15°, color jitter, random crop
    *   `get_val_transforms()` — resize + normalize only

### 4. Conveyor Simulator (Your Signature Deliverable)
*   **File:** `src/simulate_conveyor.py`
    *   Copy random HIDSAG test images into `data/incoming/` every N seconds
    *   Filenames with timestamps: `ore_20241001_143201.png`
    *   Log each copy to console
    *   Flags: `--loop` (continuous), `--speed` (default 3s), `--max` (stop after N)
*   **Acceptance test:**
    ```bash
    python src/simulate_conveyor.py --loop --speed 3
    ```
    New images must appear in `data/incoming/` every 3 seconds.

### 5. Real-Time Watcher
*   **File:** `src/inference/realtime.py`
    *   Watch `data/incoming/` using `watchdog`
    *   When a new file appears:
        1. Call `analyze(image_path)` from `src.inference.pipeline`
        2. Append result to `outputs/predictions/realtime_log.csv`
        3. Print branded console output:
           ```text
           [14:32:01] MINERALOGY: Quartz 41.2% | Pyrite 17.6% | Chalcopyrite 8.3%
           [14:32:01] PREDICTION: Cu Recovery 82.1% [78.4–85.6] HIGH
           [14:32:01] DECISION: No immediate alert
           [14:32:01] LATENCY: 284 ms
           ```
    *   Handle errors gracefully
*   **Acceptance test:** Run simulator in one terminal, watcher in another. Results must log successfully.

### 6. Tests & Documentation
*   `tests/test_data_loader.py` — test `load_geomet()` returns 146 rows, `load_mineral1()` returns 99, `load_porphyry()` returns 28, no null values in critical columns
*   `tests/test_no_leakage.py` — test sample-level split has no overlap, and `assert_no_leakage` raises on deliberate leakage
*   Update `docs/DATA.md` with subset descriptions (GEOMET, PORPHYRY, MINERAL1, MINERAL2, GEOCHEM), HIDSAG download instructions (Figshare DOI: 10.6084/m9.figshare.c.5983921.v1), and column meanings

#### Person 1 Deliverables Checklist
- [ ] `src/data/loader.py` — HIDSAG loaders (all 5 subsets)
- [ ] `src/data/splits.py` — sample-level splits, no leakage
- [ ] `src/data/preprocessing.py` — image and HSI preprocessing
- [ ] `src/data/augmentation.py` — train/val transforms
- [ ] `src/simulate_conveyor.py` — working simulator
- [ ] `src/inference/realtime.py` — working folder watcher
- [ ] `tests/test_data_loader.py` — passing
- [ ] `tests/test_no_leakage.py` — passing
- [ ] `docs/DATA.md` — documented

---

## 🧠 PERSON 2 — Mineral AI Lead

**Your Mission:** Deliver a trained model that identifies at least 3 mineral phases from HIDSAG hyperspectral images, with per-class accuracy reporting and confidence scores.

### 1. Baseline Mineral Classifier
*   **File:** `src/models/mineral_classifier.py`
    *   Rule: Do NOT start with a Transformer. Start with the simplest thing that works.
    *   Implement the `MineralClassifier` class:
        *   `__init__(config)` — loads config, sets device
        *   `build()` — for spectral data, use a 1D-CNN or Random Forest on spectral features. For image data, use ResNet-50.
        *   `train(train_loader, val_loader)` — full training loop
        *   `predict(input)` — returns `{"minerals": {name: prob}, "confidence": float, "uncertainty": float}`
        *   `save(path)` / `load(path)`
    *   Training data: HIDSAG MINERAL1 (33 mineral targets) OR PORPHYRY (8 classes)
    *   Implement Monte Carlo Dropout for uncertainty:
        *   N=30 forward passes with dropout enabled
        *   confidence = mean max probability
        *   uncertainty = std dev of predictions
*   **Acceptance test:**
    ```bash
    python -c "from src.models.mineral_classifier import MineralClassifier; \
    m = MineralClassifier('configs/config.yaml'); \
    m.build(); print('Model built:', sum(p.numel() for p in m.model.parameters()))"
    ```

### 2. Training Script
*   **File:** `src/training/train_classifier.py`
    *   Load HIDSAG MINERAL1 or PORPHYRY via `HIDSAGLoader` → `make_sample_level_splits`
    *   Build DataLoaders with augmentation
    *   Compute class weights for imbalanced data
    *   Train with:
        *   CrossEntropyLoss (weighted)
        *   AdamW, lr=1e-4, weight_decay=1e-4
        *   Cosine annealing scheduler
        *   Early stopping (patience=7)
    *   Log per epoch: train loss, val loss, val accuracy, val macro F1, per-class precision/recall/F1
    *   Save best checkpoint to `outputs/checkpoints/mineral_classifier_best.pt`
    *   Save metrics to `outputs/metrics/classifier_history.json`
    *   Save confusion matrix PNG to `outputs/metrics/confusion_matrix.png`
*   **Acceptance test:**
    ```bash
    python src/training/train_classifier.py
    ```
    Must run end-to-end and produce all outputs.

### 3. Train and Tune
*   Run training (expect 20–50 epochs)
*   Target accuracy: ≥ 85% on validation
*   If accuracy < 85%:
    *   Try different spectral preprocessing (SNV, first derivative)
    *   Try PCA dimensionality reduction
    *   Try Random Forest on spectral bands as a baseline
*   If accuracy ≥ 90%: stop. Don't over-tune. Move on.
*   Back up best model to Google Drive

### 4. Uncertainty Calibration
*   **File:** `src/models/uncertainty.py`
    *   Implement `calibrate_confidence_thresholds(model, val_loader)`:
        *   Run MC Dropout on validation set
        *   Compute confidence distribution for correct vs. incorrect predictions
        *   Find thresholds:
            *   HIGH confidence: ≥ 80% chance of correct
            *   MEDIUM confidence: 60–80% chance
            *   LOW confidence: < 60% chance
        *   Report thresholds to team — used in the dashboard
        *   Save thresholds to `configs/config.yaml`

### 5. Validation Report
*   **File:** `src/training/evaluate.py`
    *   Generate full accuracy report:
        *   Overall accuracy
        *   Per-class precision, recall, F1
        *   Confusion matrix (visual + numeric)
        *   Inference latency (mean, p95) in ms
        *   Calibration plot (predicted confidence vs. actual accuracy)
    *   Save report as `outputs/metrics/classification_report.json` and `.pdf`
    *   Write `docs/MODEL_PERFORMANCE.md` explaining model choice, accuracy numbers, confidence thresholds, and limitations (small dataset, single deposit, etc.)

### 6. Integration
*   Wire classifier into `src/inference/pipeline.py`
*   Help Person 3 display mineral composition in the dashboard

#### Person 2 Deliverables Checklist
- [ ] `src/models/mineral_classifier.py` — trained model class
- [ ] `src/models/uncertainty.py` — MC Dropout + calibration
- [ ] `src/training/train_classifier.py` — working training script
- [ ] `src/training/evaluate.py` — full evaluation report
- [ ] `outputs/checkpoints/mineral_classifier_best.pt` — trained weights
- [ ] `outputs/metrics/classification_report.json` — accuracy report
- [ ] `outputs/metrics/confusion_matrix.png` — confusion matrix
- [ ] `docs/MODEL_PERFORMANCE.md` — model documentation
- [ ] Accuracy ≥ 85% on held-out HIDSAG test set

---

## ⚙️ PERSON 3 — Process & System Lead

**Your Mission:** Deliver a processability model that predicts Cu recovery, Mo recovery, and Bond WI from HIDSAG GEOMET, plus a polished dashboard that makes the system demo-ready.

### 1. Processability Model
*   **File:** `src/models/processability.py`
    *   Complete the `ProcessabilityModel` class:
        *   `build()` — returns an XGBoost regressor (or sklearn GradientBoosting)
        *   `train(X, y)` — trains on features → process targets
        *   `predict(X)` — returns `{"cu_recovery": {"value": 82.1, "low": 78.4, "high": 85.6}, ...}`
        *   `save(path)` / `load(path)`
    *   Use quantile regression for uncertainty:
        *   Train 3 models per target: quantiles 0.05, 0.5, 0.95
        *   The 0.5 model gives the point prediction
        *   The 0.05 and 0.95 give the 90% prediction interval
*   **Acceptance test:**
    ```bash
    python -c "from src.models.processability import ProcessabilityModel; \
    m = ProcessabilityModel('configs/config.yaml'); \
    m.build(); print('Model built')"
    ```

### 2. Training Script
*   **File:** `src/training/train_processability.py`
    *   Load HIDSAG GEOMET via `HIDSAGLoader.load_geomet()`
    *   Extract features:
        *   Mineral composition (from GEOMET metadata if available, or derived from spectral features)
        *   Spectral features: mean spectrum, band ratios, PCA components from VNIR+SWIR
        *   Textural features: grain size estimate, edge density
    *   Target variables: `cu_recovery`, `mo_recovery`, `ph`, `lime_consumption`, `bwi`
    *   Train quantile regressors
    *   Evaluate:
        *   MAE, RMSE per target
        *   Compare to HIDSAG paper benchmark (Table 3): MAE < 5% for most variables
        *   Coverage of prediction intervals (should be ~90%)
    *   Save models to `outputs/checkpoints/processability_*.pkl`
    *   Save metrics to `outputs/metrics/processability_metrics.json`
*   **Acceptance test:**
    ```bash
    python src/training/train_processability.py
    ```

### 3. Decision Engine
*   **File:** `src/decision/engine.py`
    *   Complete `DecisionEngine` class:
        *   `__init__(rules_path)` — loads `configs/rules.yaml`
        *   `evaluate(minerals, predictions, confidence)` — returns list of decisions
    *   Each decision has:
        *   `priority`: HIGH / MEDIUM / LOW
        *   `message`: human-readable recommendation
        *   `reason`: which minerals/predictions drove it
        *   `icon`: Lucide icon name
    *   Support rules based on:
        *   Mineral fractions (e.g., pyrite > 20%)
        *   Predictions (e.g., Cu recovery < 70%)
        *   Confidence (e.g., confidence < 0.60)
    *   **Do NOT hardcode setpoint dosages.** Flag for review, don't prescribe values.
*   **Acceptance test:**
    ```bash
    pytest tests/test_decision_engine.py -v
    ```

### 4. Dashboard — Components
*   **Files:** `app/components/*.py`
    *   `header.py` — branded MineIQ header with logo, tagline, Mintek colours
    *   `mineral_card.py` — displays mineral composition with progress bars
    *   `prediction_card.py` — displays predictions with confidence intervals, colour-coded
    *   `confidence_badge.py` — HIGH / MEDIUM / LOW badge with Lucide icon
    *   `decision_panel.py` — displays decision alerts with priority colours
    *   `latency_panel.py` — displays inference latency and throughput
*   **Acceptance test:** Launch dashboard, all components render without errors.

### 5. Dashboard — Pages
*   **Files:** `app/pages/*.py`
    *   **Page 1 — Single Analysis:**
        *   File uploader (.png, .jpg, .h5)
        *   Display uploaded image
        *   "Analyse" button → runs `analyze()`
        *   Display: minerals, predictions, decisions, latency
        *   If confidence is LOW: show large red banner
    *   **Page 2 — Batch Analysis:**
        *   Upload multiple images or select from test set
        *   Display table: filename, minerals, prediction, decision
        *   Download results as CSV
    *   **Page 3 — Real-Time Conveyor:**
        *   "Start Conveyor Simulation" button
        *   Live feed of incoming samples
        *   Latest prediction, latest decision
        *   Running latency chart
        *   Counter: samples processed, alerts triggered
    *   **Page 4 — Model Performance:**
        *   Confusion matrix (from Person 2)
        *   Per-class precision/recall/F1
        *   Processability MAE/RMSE
        *   Inference latency histogram
    *   **Page 5 — About:**
        *   Team credits
        *   HIDSAG citation (Ehrenfeld et al., 2023, Scientific Data)
        *   Mintek branding and mission
    *   **Page 6 — Live Camera:**
        *   Live webcam feed using OpenCV for real-time inference
        *   Computer vision UI targeting box
        *   Live classification and process rule triggers based on HIDSAG parameters

### 6. Polish, Test, and Rehearse
*   Test every page with mock and real data
*   Fix any UI glitches
*   Apply Mintek theme consistently
*   Ensure every page loads in < 2 seconds
*   Write `docs/DASHBOARD.md` explaining each page
*   Rehearse the 60-second demo end-to-end. Time it. Cut anything slow.
*   Ensure the "I'm not sure" moment is dramatic.
*   Prepare fallback if the live demo fails (recorded video)

#### Person 3 Deliverables Checklist
- [ ] `src/models/processability.py` — trained model class
- [ ] `src/training/train_processability.py` — working training script
- [ ] `outputs/checkpoints/processability_*.pkl` — trained weights
- [ ] `outputs/metrics/processability_metrics.json` — accuracy report
- [ ] `src/decision/engine.py` — working rules engine
- [ ] `configs/rules.yaml` — populated with real rules
- [ ] `app/components/*.py` — all 6 components
- [ ] `app/pages/*.py` — all 5 pages
- [ ] `app/theme/styles.css` — full Mintek theme
- [ ] `docs/DASHBOARD.md` — dashboard documentation
- [ ] Demo rehearsed and timed

---

## 🤝 Shared Responsibilities (All 3 People)

### Git Workflow (Non-Negotiable)
Never push directly to main. Always create a feature branch:
```bash
git checkout -b feature/person1-data-loader
```
Commit often. Small commits with clear messages.
Open a PR when your feature is ready.
Another person reviews before merging.
Pull from main daily:
```bash
git checkout main && git pull
git checkout your-branch && git merge main
```

### Daily Standup (15 min, every morning)
Each person answers:
1. What did I finish yesterday?
2. What am I doing today?
3. What's blocking me?

### Daily Integration (30 min, every evening)
1. Merge all PRs
2. Run `make test` together — all tests must pass
3. Run `make dashboard` — all pages must load
4. Update `README.md` if anything changed

### Communication
*   Slack / WhatsApp group for quick questions
*   GitHub Issues for bugs and tasks
*   Shared Google Doc for the presentation outline
*   Google Drive folder for large files (checkpoints, datasets)

---

## 🌟 The Golden Rules
1. HIDSAG is our only dataset. Everything comes from it.
2. Ship something every day. A working partial system beats a perfect unfinished one.
3. Test before you commit. Run `make test` locally.
4. Commit small, commit often. One feature per commit.
5. Ask for help early. Don't spend 4 hours stuck.
6. No hardcoded paths or values. Use `configs/config.yaml`.
7. No pixel-level leakage. Always split by sample.
8. No setpoint dosages without evidence. Flag, don't prescribe.
9. Cite HIDSAG. Use it as foundation, not competitor.
10. Keep the demo rehearsed. Time it. Cut anything slow.
11. Protect the "I'm not sure" moment. That's what wins.

## ✅ What "Done" Looks Like
By submission day, anyone should be able to:
1. Clone the repo
2. Run `make install`
3. Run `make dashboard`
4. Upload a HIDSAG image and see minerals, predictions, decisions, and latency
5. Run `make demo` and watch the conveyor simulator stream HIDSAG images
6. See the "LOW CONFIDENCE" banner appear on a hard sample
7. Read the accuracy report and see ≥ 85% classification accuracy on HIDSAG
8. Understand the system by reading `docs/ARCHITECTURE.md`

If all 8 are true, you have a winning project. Let's win this.
