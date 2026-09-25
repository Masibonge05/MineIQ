import pytest
import pandas as pd
from src.data.loader import HIDSAGLoader

def test_hidsag_loader_geomet():
    loader = HIDSAGLoader("dummy_path")
    df = loader.load_geomet()
    assert isinstance(df, pd.DataFrame)
    assert 'sample_id' in df.columns
    assert 'vnir_path' in df.columns
    assert 'cu_recovery' in df.columns

def test_hidsag_loader_mineral1():
    loader = HIDSAGLoader("dummy_path")
    df = loader.load_mineral1()
    assert isinstance(df, pd.DataFrame)
    assert 'sample_id' in df.columns
    assert 'qemscan_quartz' in df.columns
