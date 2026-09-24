import pytest
import pandas as pd
from src.data.splits import make_sample_level_splits

def test_sample_level_leakage():
    # Mock dataframe with multiple crops per sample
    data = [
        {"sample_id": "S1", "crop": 1},
        {"sample_id": "S1", "crop": 2},
        {"sample_id": "S2", "crop": 1},
        {"sample_id": "S3", "crop": 1},
        {"sample_id": "S3", "crop": 2},
        {"sample_id": "S4", "crop": 1},
        {"sample_id": "S5", "crop": 1},
        {"sample_id": "S6", "crop": 1},
        {"sample_id": "S7", "crop": 1},
        {"sample_id": "S8", "crop": 1},
        {"sample_id": "S9", "crop": 1},
        {"sample_id": "S10", "crop": 1},
    ]
    df = pd.DataFrame(data)
    
    split_df = make_sample_level_splits(df, seed=42)
    
    # Check that crops of the same sample are in the same split
    s1_splits = split_df[split_df['sample_id'] == 'S1']['split'].unique()
    assert len(s1_splits) == 1, "Leakage detected: crops of S1 are in different splits."
    
    s3_splits = split_df[split_df['sample_id'] == 'S3']['split'].unique()
    assert len(s3_splits) == 1, "Leakage detected: crops of S3 are in different splits."
