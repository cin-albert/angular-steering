import sys
import os
import logging
from huggingface_hub import upload_folder


logger = logging.getLogger(__name__)

def main():
    REPO_ID = "LoneResearch/thinking-steering-generations"
    repo_type = "dataset"

    if len(sys.argv) != 3:
        logger.error("Usage: python upload_result.py <model_name> <dataset_name>")
        sys.exit(1)

    model_name = sys.argv[1]
    dataset_name = sys.argv[2]
    path_in_repo = f"{model_name}/{dataset_name}"
    local_folder_path = f"output/thinking_steering_generations/{model_name}/{dataset_name}/"

    if not os.path.exists(local_folder_path):
        logger.error(f"Cannot find the generation files at: {local_folder_path}")
        sys.exit(1)

    try:
        logger.info(f"Starting upload to {REPO_ID}/{path_in_repo}...")
        
        upload_folder(
            folder_path=local_folder_path,
            repo_id=REPO_ID,
            repo_type=repo_type,
            path_in_repo=path_in_repo,
            commit_message=f"Add steering results, model={model_name}, dataset={dataset_name}",
        )
        
        logger.info("Upload completed successfully.")
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()