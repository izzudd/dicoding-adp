# Proyek Analisis Data: Bike Sharing Dataset ✨

## Setup environment
```bash
python -m venv .venv
source .venv/bin/activate # on windows replace with "./venv/bin/activate"
pip install -r requirements.txt
```

## Prepare Dataset
```bash
gdown 1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ -O dataset.zip
unzip dataset.zip -d dataset
```

## Run steamlit app
```bash
streamlit run main.py
```