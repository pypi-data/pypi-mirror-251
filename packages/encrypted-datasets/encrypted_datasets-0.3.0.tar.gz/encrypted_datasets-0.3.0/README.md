## encrypted-datasets

### Installation
```bash
pip install encrypted-datasets
```

### Usage
```python
from datasets import load_dataset
from encrypted_datasets import encrypt_dataset, decrypt_dataset

huggingface_api_token= 'API_TOKEN'
downloaded_dataset = load_dataset('organization/dataset_repo', token=huggingface_api_token)
key = 'Your Symetric encryption key'

decrypted_dataset = decrypt_dataset(downloaded_dataset, key)

# Make modifications to decrypted_dataset...

re_encrypted_dataset = encrypt_dataset(decrypted_dataset, key)

re_encrypted_dataset.push_to_hub('organization/dataset_repo',token=huggingface_api_token)
```