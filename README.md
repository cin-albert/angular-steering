## How to run this repo

### 1. Installation
```bash
pip install -r requirements.txt --no-cache-dir
```

### 2. Configure and Run
Individual runs apply steering to a single model/dataset pair. Edit the settings in vllm_angular_steering.sh using the following priority list:
- Models: `DeepSeek-R1-Distill-Qwen-14B`, `Qwen3-32B`
- Datasets: `math500`, `livecodebench`, `arc`

**Execute the run:**
```bash
bash vllm_angular_steering.sh
```

### 3. Upload result to HuggingFace dataset
Upload your generation files to the `LoneResearch` Hugging Face organization after each model/dataset completion.

**Prerequisites:**
- Authenticated via: `huggingface-cli login`
- Write access to the `LoneResearch` organization.

**Usage:**
```bash
python upload_result.py <local_folder_path> <model_name> <dataset_name>
```
- `<local_folder_path>`: Path to the directory containing your generation files.

- `<model_name>`: Name of the model (e.g., DeepSeek-R1-Distill-Qwen-14B).

- `<dataset_name>`: Name of the evaluation dataset (e.g., math500).

