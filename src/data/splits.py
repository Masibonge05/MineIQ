import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

def make_sample_level_splits(df: pd.DataFrame, seed: int = 42, train_frac: float = 0.7, val_frac: float = 0.15) -> pd.DataFrame:
    """
    Creates sample-level train/val/test splits to prevent pixel-level leakage.
    Samples with the same sample_id will be placed in the same split.
    """
    if df.empty or 'sample_id' not in df.columns:
        return df
        
    unique_samples = df['sample_id'].unique()
    
    # First split into train and temp (val+test)
    train_ids, temp_ids = train_test_split(unique_samples, train_size=train_frac, random_state=seed)
    
    # Split temp into val and test
    test_frac_of_temp = (1.0 - train_frac - val_frac) / (1.0 - train_frac)
    # Handle float precision
    test_frac_of_temp = min(max(test_frac_of_temp, 0.0), 1.0)
    
    val_ids, test_ids = train_test_split(temp_ids, test_size=test_frac_of_temp, random_state=seed)
    
    df = df.copy()
    df['split'] = 'unassigned'
    df.loc[df['sample_id'].isin(train_ids), 'split'] = 'train'
    df.loc[df['sample_id'].isin(val_ids), 'split'] = 'val'
    df.loc[df['sample_id'].isin(test_ids), 'split'] = 'test'
    
    return df
