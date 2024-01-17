from typing import Any
from datasets import Dataset
from cryptography.fernet import Fernet

def encrypt_dataset(dataset: Dataset, key:str):
    f= Fernet(key)
    def encrypt_row(row: dict[str, Any]):
        return {k: f.encrypt(str(v).encode('utf-8')) for k, v in row.items()}
    return dataset.map(encrypt_row)

def decrypt_dataset(dataset: Dataset, key:str):
    f= Fernet(key)
    
    def decrypt_row(row: dict[str, Any]):
        return {k: f.decrypt(v).decode('utf-8') for k, v in row.items()}
    
    return dataset.map(decrypt_row)
