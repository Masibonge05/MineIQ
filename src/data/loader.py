import os
import pandas as pd
import logging
import json
import h5py

logger = logging.getLogger(__name__)

class MinetV2Loader:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        
    def load(self) -> pd.DataFrame:
        # TODO(person-1): Implement loading from Minet V2 folders and Minerals_5640.csv
        logger.info(f"Loading MinetV2 data from {self.root_dir}")
        
        # Mock data for out-of-the-box run
        data = [
            {"sample_id": "M_001", "image_path": "mock/m_001.jpg", "label": "bornite", "split": "train"},
            {"sample_id": "M_002", "image_path": "mock/m_002.jpg", "label": "biotite", "split": "val"},
        ]
        df = pd.DataFrame(data)
        
        class_counts = df['label'].value_counts()
        for label, count in class_counts.items():
            if count < 10:
                logger.warning(f"Class '{label}' has fewer than 10 samples ({count}).")
                
        return df

class HIDSAGLoader:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        
    def load(self) -> pd.DataFrame:
        # TODO(person-1): Implement loading from HIDSAG HDF5 files using hidsag library
        logger.info(f"Loading HIDSAG data from {self.root_dir}")
        
        # Mock data
        data = [
            {"sample_id": "H_001", "h5_path": "mock/h_001.h5", "targets": {"cu_recovery": 82.5}, "split": "train"},
            {"sample_id": "H_001", "h5_path": "mock/h_001_crop2.h5", "targets": {"cu_recovery": 82.5}, "split": "train"},
            {"sample_id": "H_002", "h5_path": "mock/h_002.h5", "targets": {"cu_recovery": 65.0}, "split": "test"},
        ]
        return pd.DataFrame(data)
