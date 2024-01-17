from typing import Any, overload
from datasets import Dataset,DatasetDict, IterableDataset, IterableDatasetDict
from cryptography.fernet import Fernet

@overload
def encrypt_dataset(dataset: Dataset, key:str|bytes) -> Dataset: ...

@overload
def encrypt_dataset(dataset: DatasetDict, key:str|bytes) -> DatasetDict: ...

@overload
def encrypt_dataset(dataset: IterableDatasetDict, key:str|bytes) -> IterableDatasetDict: ...

@overload
def encrypt_dataset(dataset: IterableDataset, key:str|bytes) -> IterableDataset: ...

def encrypt_dataset(dataset:  Dataset | DatasetDict | IterableDatasetDict | IterableDataset, key:str|bytes):
    f= Fernet(key)
    def encrypt_row(row: dict[str, Any]):
        return {k: f.encrypt(str(v).encode('utf-8')) for k, v in row.items()}
    return dataset.map(encrypt_row)


@overload
def decrypt_dataset(dataset: Dataset, key:str|bytes) -> Dataset: ...

@overload
def decrypt_dataset(dataset: DatasetDict, key:str|bytes) -> DatasetDict: ...

@overload
def decrypt_dataset(dataset: IterableDatasetDict, key:str|bytes) -> IterableDatasetDict: ...

@overload
def decrypt_dataset(dataset: IterableDataset, key:str|bytes) -> IterableDataset: ...

def decrypt_dataset(dataset: Dataset | DatasetDict | IterableDatasetDict | IterableDataset, key:str|bytes):
    f= Fernet(key)
    
    def decrypt_row(row: dict[str, Any]):
        return {k: f.decrypt(v).decode('utf-8') for k, v in row.items()}
    
    return dataset.map(decrypt_row)
