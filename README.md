# MineIQ: Real-Time Mineral Intelligence 🚀

Welcome to the **MineIQ** project skeleton! This document outlines everything you need to know to build upon this foundation. Please read it carefully.

## 🛠️ Getting Started

Everyone on the team must run the following commands to set up their environment and verify the skeleton works:

```bash
# Clone the repository
git clone https://github.com/[your-org]/mineiq.git
cd mineiq

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # On Mac/Linux
# venv\Scripts\activate        # On Windows

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard to confirm it works
make dashboard
```

**Required Reading for Everyone:**
- `README.md` (this file)
- `docs/TEAM_GUIDE.md`
- `docs/ARCHITECTURE.md`

### 👑 The Golden Rule
> **Never push directly to main. Always work on a branch. Always open a PR.**

---

## 👥 Team Roles at a Glance

| Person | Role | Owns | Primary Deliverable |
| :--- | :--- | :--- | :--- |
| **Person 1** | Data & Pipeline Lead | `src/data/`, `src/inference/realtime.py`, `data/` | Working data loaders + conveyor simulator |
| **Person 2** | Mineral AI Lead | `src/models/mineral_classifier.py`, `src/training/train_classifier.py` | Trained mineral classifier (≥3 phases) |
| **Person 3** | Process & System Lead | `src/models/processability.py`, `src/decision/`, `app/` | Trained processability model + polished dashboard |

*Note: Everyone shares responsibility for README.md updates, final demo rehearsal, and final presentation slides.*

---

## 👷‍♂️ PERSON 1 — Data & Pipeline Lead

**Your Mission:** Make sure data flows cleanly from disk to model to dashboard, with no leakage, and build the conveyor simulator that makes the real-time demo possible.

### Day 1: Data Loading (Morning)
**File to edit:** `src/data/loader.py`
- Complete the `MinetV2Loader` class:
  - Read `data/raw/minet_v2/minerals_dataset/Minet 5640 Images/`
  - Parse `Minerals_5640.csv`
  - Return `pd.DataFrame` with columns: `sample_id, image_path, label, label_idx`
  - Log: total images, images per class
- Complete the `HIDSAGLoader` class:
  - Use the hidsag library from [https://github.com/alges/hidsag](https://github.com/alges/hidsag)
  - Load `data/hidsag/GEOMET/` first
  - For each sample: read `metadata.json` → extract Cu rec, Mo rec, PH, Lime cons, WI
  - Load VNIR, SWIR, RGB cubes from `.h5` files
  - Return `pd.DataFrame` with: `sample_id, vnir_path, swir_path, rgb_path, cu_recovery, mo_recovery, ph, lime_consumption, bwi`
- **Acceptance test:** Both loaders must print real rows when run.
  ```bash
  python -c "from src.data.loader import MinetV2Loader, HIDSAGLoader; print(MinetV2Loader('configs/config.yaml').load().head()); print(HIDSAGLoader('configs/config.yaml').load().head())"
  ```

### Day 1: Splits (Afternoon)
**File to edit:** `src/data/splits.py`
- Implement `make_sample_level_splits(df, seed=42)`:
  - **CRITICAL:** All crops/measurements from the same `sample_id` go to the SAME split.
  - Returns a DataFrame with a split column: train, val, test (70/15/15 split, stratified by class or target quantile).
- Implement `assert_no_leakage(df)`:
  - Asserts that no `sample_id` appears in more than one split. Raises ValueError if leakage is found.
- **Acceptance test:** `tests/test_no_leakage.py` must pass.
  ```bash
  pytest tests/test_no_leakage.py -v
  ```

### Day 2: Preprocessing & Augmentation
**File to edit:** `src/data/preprocessing.py`
- `preprocess_image(path, size=224)`: loads PNG/JPG, resizes, normalizes with ImageNet stats.
- `preprocess_hsi(path, band_range)`: loads HDF5, selects VNIR/SWIR bands, normalizes per-band.
- `extract_texture_features(image)`: returns grain size estimate, edge density, texture entropy using OpenCV.

**File to edit:** `src/data/augmentation.py`
- `get_train_transforms()`: random flip, rotation ±15°, color jitter, random crop.
- `get_val_transforms()`: resize + normalize only.

### Day 3: Conveyor Simulator (Your Signature Deliverable)
**File to edit:** `src/simulate_conveyor.py`
- Create a script that copies random test images into `data/incoming/` every N seconds (configurable).
- Uses filenames with timestamps: `ore_20241001_143201.png`
- Logs each copy to console.
- Add flags: `--loop` (continuous), `--speed` (interval, default 3s), `--max` (stop after N images).
- **Acceptance test:** New images must appear in `data/incoming/` every 3 seconds.
  ```bash
  python src/simulate_conveyor.py --loop --speed 3
  ```

### Day 4: Real-Time Watcher
**File to edit:** `src/inference/realtime.py`
- Watch `data/incoming/` using watchdog library.
- When a new file appears:
  - Call `analyze(image_path)` from `src.inference.pipeline`
  - Append result to `outputs/predictions/realtime_log.csv`
  - Print branded console output:
    ```text
    [14:32:01] MINERALOGY: Quartz 41.2% | Pyrite 17.6% | Chalcopyrite 8.3%
    [14:32:01] PREDICTION: Cu Recovery 82.1% [78.4–85.6] HIGH
    [14:32:01] DECISION: No immediate alert
    [14:32:01] LATENCY: 284 ms
    ```
  - Handle errors gracefully.
- **Acceptance test:** Run simulator in one terminal and watcher in another. Results must log successfully.

### Day 5: Testing & Documentation
- Write `tests/test_data_loader.py`: Test row counts and null values.
- Write `tests/test_no_leakage.py`: Test sample-level split overlaps.
- Update `docs/DATA.md` with download locations, folder structures, and column meanings.

### Day 6-7: Support & Integration
- Help Person 2 and 3 with data formatting and dashboard wiring. Run full demo end-to-end.

---

## 🧠 PERSON 2 — Mineral AI Lead

**Your Mission:** Deliver a trained model that identifies at least 3 mineral phases from images, with per-class accuracy reporting and confidence scores.

### Day 1: Baseline First (Critical)
**File to edit:** `src/models/mineral_classifier.py`
- **Rule:** Do NOT start with a Transformer. Start with the simplest thing that works.
- Implement the `MineralClassifier` class (`__init__`, `build` using ResNet-50 linear head, `train`, `predict`, `save`, `load`).
- Implement Monte Carlo Dropout for uncertainty (run N=30 forward passes during inference).
  - Confidence = mean max probability across passes
  - Uncertainty = std dev of predictions
- **Acceptance test:** Model builds successfully.
  ```bash
  python -c "from src.models.mineral_classifier import MineralClassifier; m = MineralClassifier('configs/config.yaml'); m.build(); print('Model built:', sum(p.numel() for p in m.model.parameters()))"
  ```

### Day 2: Training Script
**File to edit:** `src/training/train_classifier.py`
- Load data, build DataLoaders, compute class weights.
- Train with: CrossEntropyLoss (weighted), AdamW (lr=1e-4), Cosine annealing, Early stopping (patience=7).
- Log: Train/val loss, val accuracy, val macro F1, per-class metrics.
- Save best checkpoint, metrics JSON, and confusion matrix PNG.
- **Acceptance test:** Script must run end-to-end and produce all outputs.
  ```bash
  python src/training/train_classifier.py
  ```

### Day 3: Train and Tune
- Run training. Target accuracy: ≥ 90% on validation.
- If < 90%: Try EfficientNet-B0, more augmentation, different learning rates.
- If ≥ 95%: Stop. Don't over-tune. Back up best model to Google Drive.

### Day 4: Uncertainty Calibration
**File to edit:** `src/models/uncertainty.py`
- Implement `calibrate_confidence_thresholds(model, val_loader)`:
  - Find thresholds: HIGH (≥80% chance correct), MEDIUM (60-80%), LOW (<60%).
- Report thresholds to team and save to `configs/config.yaml`.

### Day 5: Validation Report
**File to edit:** `src/training/evaluate.py`
- Generate full accuracy report (overall acc, per-class metrics, confusion matrix, latency stats, calibration plot).
- Save as JSON and PDF in `outputs/metrics/`.
- Write `docs/MODEL_PERFORMANCE.md` explaining model choice, accuracy, thresholds, and limitations.

### Day 6-7: Integration & Polish
- Wire classifier into `src/inference/pipeline.py`.
- Help Person 3 display mineral composition.

---

## ⚙️ PERSON 3 — Process & System Lead

**Your Mission:** Deliver a processability model that predicts Cu recovery, Mo recovery, and Bond WI, plus a polished dashboard that makes the system demo-ready.

### Day 1: Processability Model
**File to edit:** `src/models/processability.py`
- Complete `ProcessabilityModel` class (`build` using XGBoost/sklearn, `train`, `predict`, `save`, `load`).
- Use quantile regression for uncertainty: Train 3 models per target (0.05, 0.5, 0.95 quantiles).
- **Acceptance test:**
  ```bash
  python -c "from src.models.processability import ProcessabilityModel; m = ProcessabilityModel('configs/config.yaml'); m.build(); print('Model built')"
  ```

### Day 2: Training Script
**File to edit:** `src/training/train_processability.py`
- Load HIDSAG GEOMET data, extract features (mineral, spectral, textural).
- Target variables: cu_recovery, mo_recovery, ph, lime_consumption, bwi.
- Evaluate MAE, RMSE, and coverage of prediction intervals (~90%).
- Save models and metrics.
- **Acceptance test:** Script runs end-to-end.
  ```bash
  python src/training/train_processability.py
  ```

### Day 3: Decision Engine
**File to edit:** `src/decision/engine.py`
- Complete `DecisionEngine` class to evaluate `configs/rules.yaml`.
- Returns decisions with priority, message, reason, and Lucide icon.
- Support rules based on mineral fractions, predictions, and confidence.
- *Do NOT hardcode setpoint dosages. Flag for review, don't prescribe values.*
- **Acceptance test:**
  ```bash
  pytest tests/test_decision_engine.py -v
  ```

### Day 4: Dashboard — Components
**Files to edit:** `app/components/*.py`
- Implement branded components: header, mineral card, prediction card, confidence badge, decision panel, latency panel.
- **Acceptance test:** Dashboard launches and components render without errors.

### Day 5: Dashboard — Pages
**Files to edit:** `app/pages/*.py`
- **Page 1 (Single):** File uploader, analyse button, display results, LOW CONFIDENCE red banner.
- **Page 2 (Batch):** Batch upload, table display, CSV download.
- **Page 3 (Real-Time):** Simulator trigger, live feed, latency chart, counters.
- **Page 4 (Performance):** Confusion matrix, metrics, latency histogram.
- **Page 5 (About):** Team credits, HIDSAG citation, Mintek branding.

### Day 6-7: Polish & Test & Rehearse
- Test pages with mock and real data. Apply Mintek theme consistently.
- Write `docs/DASHBOARD.md`.
- **Demo Rehearsal:** Time the 60-second demo. Cut anything slow. Perfect the "I'm not sure" moment. Have a video backup.

---

## 🤝 Shared Responsibilities (All 3 People)

### Git Workflow (Non-Negotiable)
- Never push directly to main. Create feature branches: `git checkout -b feature/person1-data-loader`
- Commit often with clear messages. Open PRs for review.
- Pull daily: `git checkout main`, `git pull`, `git checkout your-branch`, `git merge main`

### Daily Routines
- **Daily Standup (Morning, 15 min):** What did I finish? What am I doing today? What's blocking me?
- **Daily Integration (Evening, 30 min):** Merge PRs, run `make test`, run `make dashboard`. Update README.

### Communication
- Slack/WhatsApp for quick questions, GitHub Issues for bugs/tasks.
- Shared Google Doc for presentation, Google Drive for large files (checkpoints, datasets).

---

## 🏆 Final Submission Checklist (Everyone)

Before submission day, verify:
- [ ] All tests pass: `make test`
- [ ] Dashboard runs: `make dashboard`
- [ ] Real-time demo works: `simulate_conveyor.py` + `realtime.py`
- [ ] README is up to date
- [ ] Accuracy report is complete
- [ ] Demo is rehearsed, slides are ready, backup plan exists

---

## 📅 Weekly Schedule (At a Glance)

| Day | Person 1 | Person 2 | Person 3 |
| :--- | :--- | :--- | :--- |
| **Mon** | Data loaders | Baseline classifier | Processability model |
| **Tue** | Splits + preprocessing | Training script | Training script |
| **Wed** | Conveyor simulator | Train + tune | Decision engine |
| **Thu** | Real-time watcher | Uncertainty calibration | Dashboard components |
| **Fri** | Tests + docs | Validation report | Dashboard pages |
| **Sat** | Integration support | Integration support | Polish + test |
| **Sun** | Demo rehearsal | Demo rehearsal | Demo rehearsal |

---

## 🌟 The Golden Rules
1. **Ship something every day.** A working partial system beats a perfect unfinished one.
2. **Test before you commit.** Run `make test` locally.
3. **Commit small, commit often.** One feature per commit.
4. **Ask for help early.** Don't spend 4 hours stuck.
5. **No hardcoded paths/values.** Use `configs/config.yaml`.
6. **No pixel-level leakage.** Always split by sample.
7. **No setpoint dosages without evidence.** Flag, don't prescribe.
8. **Cite HIDSAG.** Use it as foundation, not competitor.
9. **Keep the demo rehearsed.** Time it. Cut anything slow.
10. **Protect the "I'm not sure" moment.** That's what wins.

---

## ✅ What "Done" Looks Like
By submission day, anyone should be able to:
1. Clone the repo.
2. Run `make install`.
3. Run `make dashboard`.
4. Upload an image and see minerals, predictions, decisions, and latency.
5. Run `make demo` and watch the conveyor simulator stream images.
6. See the "LOW CONFIDENCE" banner appear on a hard sample.
7. Read the accuracy report and see ≥ 90% classification accuracy.
8. Understand the system by reading `docs/ARCHITECTURE.md`.

*If all 8 are true, you have a winning project.* Let's win this.
