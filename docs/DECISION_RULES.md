# Minerals and Flotation Processes in HIDSAG for Training Your AI

## 1. Minerals Available in HIDSAG
HIDSAG contains copper porphyry ore samples from several Chilean deposits. The minerals present are documented in the dataset and related literature.

### Copper-Bearing Minerals (Valuable)
- **Chalcopyrite (CuFeS₂)** — the main copper ore mineral
- **Bornite (Cu₅FeS₄)** — secondary copper mineral, occurs in deeper zones
- **Chalcocite/Digenite** — copper sulfide minerals
- **Covellite (CuS)** — secondary copper sulfide
- **Malachite and Chrysocolla** — oxidized copper minerals in supergene zones

### Gangue Minerals (Waste)
- **Quartz (SiO₂)** — the dominant gangue mineral
- **Pyrite (FeS₂)** — the main sulfide gangue, a key problem mineral
- **Biotite and Muscovite/Sericite** — mica minerals
- **K-Feldspar** — can cause high Work Index
- **Plagioclase** — common silicate gangue
- **Clays (Kaolinite, Chlorite)** — cause rheology problems
- **Magnetite and Hematite** — iron oxides

**For your classifier:** The HIDSAG PORPHYRY subset explicitly contains quartz, biotite, kaolinite, specular hematite, pyrite, molybdenite, magnetite, and chalcopyrite. This is your best starting point for training a mineral classifier with at least 3 phases.

## 2. Flotation Processes and Ground Truth in HIDSAG

### What HIDSAG GEOMET Provides
The GEOMET subset contains 146 samples with real metallurgical test results from closed-cycle laboratory batch flotation tests. For each sample, the following response variables are available:
- **Cu rec**: Copper recovery (%)
- **Mo rec**: Molybdenum recovery (%)
- **pH**: Steady-state pH
- **Lime cons**: Lime consumption (kg/t)
- **WI**: Bond Work Index (kWh/t)

### Specific Mineral-to-Control Relationships
Based on the literature, here are the mineral-to-action mappings your AI should learn:

**If pyrite is high:**
- Increase pH with lime to depress pyrite
- Add depressant (sodium humate, CMC)
- Control grind size — pyrite recovery increases at coarse sizes when locked with chalcopyrite

**If chalcopyrite is locked in silicates (poor liberation):**
- Finer grind required to liberate
- Consider regrinding
- Higher collector dosage may help but risks non-selective flotation

**If clay minerals are high:**
- Add dispersants (sodium silicate, polyacrylates)
- Consider blending with low-clay ore
- Monitor pulp rheology

**If Work Index (WI) is high:**
- Indicates harder ore — more grinding energy required
- May correlate with K-feldspar content
- Adjust mill feed rate or grind target

**If copper oxides present (malachite, chrysocolla):**
- Sulfidation with sodium sulfide followed by xanthate collector
- Standard xanthate collectors are ineffective on oxides

**If Alunite is detected (Soluble mineral):**
- Alunite drops the natural pH of the pulp.
- Significantly higher lime consumption is required to reach the target pH for pyrite depression.
- Pre-emptively increase lime dosage.

**If Potassium Feldspar (K-Feldspar) is high:**
- Directly correlates with a high Bond Work Index (WI) (hard ore).
- Grinding effort must increase. Adjust the mill feed rate down or increase grinding power.
- Conversely, high Quartz often indicates a lower WI in this specific deposit.

**If Chalcopyrite is associated with high Pyrite (Phyllic alteration):**
- Chalcopyrite is often enclosed within the pyrite and poorly liberated.
- A finer grind (regrind) is strictly necessary to liberate the copper before rougher flotation.

**If Molybdenite (MoS2) and Chalcopyrite are both present:**
- Initiate bulk Cu-Mo flotation followed by selective separation.
- Depress chalcopyrite using inorganic sulfides (NaHS, Na2S) or organic depressants.
- Molybdenite is naturally hydrophobic; enhance with kerosene collector.
- Maintain careful pH control to avoid toxic H2S gas release from NaHS.

### Advanced Process Control Strategies
- **Hierarchical Control:** Modern plants use stabilizing control (PID loops for pulp level/air flow) and optimization control (Model Predictive Control) to adjust setpoints dynamically.
- **Froth Profiling:** Mass pull should be highest in the initial rougher cells and decrease toward scavenger cells.
- **Mine-to-Mill Integration:** Anticipating ore hardness (via high Bond Work Index or high K-Feldspar) allows the flotation circuit to proactively adjust to the grinding circuit's throughput.

## 3. What Your AI Will Learn
### Stage 1: Mineral Classifier
**Input:** Hyperspectral image (VNIR + SWIR)
**Output:** Mineral composition vector (e.g. Quartz 45%, Pyrite 18%, Chalcopyrite 12%)
**Training data:** HIDSAG PORPHYRY (8 classes) and/or MINERAL1 (33 mineral targets)

### Stage 2: Processability Model
**Input:** Mineral composition + spectral features + textural features
**Output:** Predicted process outcomes with uncertainty (Cu rec, Mo rec, pH, Lime cons, WI)
**Training data:** HIDSAG GEOMET (146 samples)

### Stage 3: Decision Engine
**Input:** Mineral composition + process predictions + confidence
**Output:** Decision-support alerts based on published mineral processing literature.
