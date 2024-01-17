from typing import Any
from datasets import Dataset,DatasetDict, IterableDataset, IterableDatasetDict
from cryptography.fernet import Fernet

def encrypt_dataset(dataset: DatasetDict | Dataset | IterableDatasetDict | IterableDataset, key:str|bytes):
    f= Fernet(key)
    def encrypt_row(row: dict[str, Any]):
        return {k: f.encrypt(str(v).encode('utf-8')) for k, v in row.items()}
    return dataset.map(encrypt_row)

def decrypt_dataset(dataset: DatasetDict | Dataset | IterableDatasetDict | IterableDataset, key:str|bytes):
    f= Fernet(key)
    
    def decrypt_row(row: dict[str, Any]):
        return {k: f.decrypt(v).decode('utf-8') for k, v in row.items()}
    
    return dataset.map(decrypt_row)
