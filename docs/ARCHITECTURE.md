# System Architecture

```text
[ Incoming Stream ] ---> (Realtime Watcher)
                                |
[ Uploaded Image ] --------> [ Pipeline ]
                                |
                      +---------+---------+
                      |                   |
               [Classifier]       [Processability]
               (Minerals)          (Recoveries)
                      |                   |
                      +---------+---------+
                                |
                         [Decision Engine]
                         (Rules & Alerts)
                                |
                           [Dashboard]
```

## Stages
1. **Classifier**: ResNet-50 based classification of minerals (Stage 1).
2. **Processability**: XGBoost regressor predicting Cu/Mo recoveries, Bond Work Index, Lime consumption (Stage 2).
3. **Decision Engine**: Rule-based alerts based on predictions and confidence limits.
