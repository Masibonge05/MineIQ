import pytest
import pandas as pd
from src.data.loader import MinetV2Loader, HIDSAGLoader

def test_minet_loader():
    loader = MinetV2Loader("dummy_path")
    df = loader.load()
    assert isinstance(df, pd.DataFrame)
    assert 'sample_id' in df.columns
    assert 'image_path' in df.columns
    assert 'label' in df.columns

def test_hidsag_loader():
    loader = HIDSAGLoader("dummy_path")
    df = loader.load()
    assert isinstance(df, pd.DataFrame)
    assert 'sample_id' in df.columns
    assert 'h5_path' in df.columns
    assert 'targets' in df.columns
