#!/bin/bash

DATASETS=(
    "math500"
    # "arc"
    # "tinylivecodebench"
)

MODELS=(
    # "deepseek-ai/DeepSeek-R1-Distill-LLama-8B"
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
    # "Qwen/Qwen3-14B"
    # "Qwen/Qwen3-32B"
)

SCENARIOS=(
    # "S4"
    # "S7"
    # "S8"
    "S9"
)


declare -A SCENARIOS_TO_CONFIG_FILES

SCENARIOS_TO_CONFIG_FILES=(
    # DeepSeek-R1-Distill-LLama-8B
    ["S4-DeepSeek-R1-Distill-LLama-8B-math500"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s4-pca_0-math500.npy"
    ["S7-DeepSeek-R1-Distill-LLama-8B-math500"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s7-pca_0-math500.npy"
    ["S8-DeepSeek-R1-Distill-LLama-8B-math500"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s8-pca_0-math500.npy"
    ["S9-DeepSeek-R1-Distill-LLama-8B-math500"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s9-pca_0-math500.npy"
    ["S8-DeepSeek-R1-Distill-LLama-8B-livecodebench"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-DeepSeek-R1-Distill-LLama-8B-tinylivecodebench"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-DeepSeek-R1-Distill-LLama-8B-arc"]="steering_configs/DeepSeek-R1-Distill-LLama-8B/steering_config-s8-pca_0-arc.npy"
    
    # Qwen3-32B
    ["S8-Qwen3-32B-math500"]="steering_configs/Qwen3-32B/steering_config-s8-pca_0-math500.npy"
    ["S8-Qwen3-32B-livecodebench"]="steering_configs/Qwen3-32B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-Qwen3-32B-tinylivecodebench"]="steering_configs/Qwen3-32B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-Qwen3-32B-arc"]="steering_configs/Qwen3-32B/steering_config-s8-pca_0-arc.npy"
    ["S9-Qwen3-32B-math500"]="steering_configs/Qwen3-32B/steering_config-s9-pca_0-math500-purified.npy"
    ["S9-Qwen3-32B-livecodebench"]="steering_configs/Qwen3-32B/steering_config-s9-pca_0-livecodebench-purified.npy"
    ["S9-Qwen3-32B-arc"]="steering_configs/Qwen3-32B/steering_config-s9-pca_0-arc-purified.npy"
    
    # DeepSeek-R1-Distill-Qwen-14B
    ["S8-DeepSeek-R1-Distill-Qwen-14B-math500"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s8-pca_0-math500.npy"
    ["S8-DeepSeek-R1-Distill-Qwen-14B-livecodebench"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-DeepSeek-R1-Distill-Qwen-14B-tinylivecodebench"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-DeepSeek-R1-Distill-Qwen-14B-arc"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s8-pca_0-arc.npy"
    ["S9-DeepSeek-R1-Distill-Qwen-14B-math500"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s9-pca_0-math500-purified.npy"
    ["S9-DeepSeek-R1-Distill-Qwen-14B-livecodebench"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s9-pca_0-livecodebench-purified.npy"
    ["S9-DeepSeek-R1-Distill-Qwen-14B-arc"]="steering_configs/DeepSeek-R1-Distill-Qwen-14B/steering_config-s9-pca_0-arc-purified.npy"

    # Qwen3-14B
    ["S8-Qwen3-14B-math500"]="steering_configs/Qwen3-14B/steering_config-s8-pca_0-math500.npy"
    ["S8-Qwen3-14B-livecodebench"]="steering_configs/Qwen3-14B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-Qwen3-14B-tinylivecodebench"]="steering_configs/Qwen3-14B/steering_config-s8-pca_0-livecodebench.npy"
    ["S8-Qwen3-14B-arc"]="steering_configs/Qwen3-14B/steering_config-s8-pca_0-arc.npy"
    ["S9-Qwen3-14B-math500"]="steering_configs/Qwen3-14B/steering_config-s9-pca_0-math500-purified.npy"
    ["S9-Qwen3-14B-livecodebench"]="steering_configs/Qwen3-14B/steering_config-s9-pca_0-livecodebench-purified.npy"
    ["S9-Qwen3-14B-arc"]="steering_configs/Qwen3-14B/steering_config-s9-pca_0-arc-purified.npy"
)


for model in "${MODELS[@]}"; do
    model_name=$(echo "$model" | cut -d'/' -f2)
    for dataset in "${DATASETS[@]}"; do
        for scenario in "${SCENARIOS[@]}"; do
            config_file="${SCENARIOS_TO_CONFIG_FILES[$scenario-${model_name}-$dataset]}"
            if [[ -z "$config_file" ]]; then
                echo "No config for scenario=$scenario dataset=$dataset, skipping."
                continue
            fi

            echo "================================================"
            echo "Apply Steering"
            echo "Model: $model"
            echo "Dataset: $dataset"
            echo "Scenario: $scenario"
            echo "Config File: $config_file"
            echo "================================================"
            
            python3 vllm_angular_steering.py \
                --model "$model" \
                --dataset "$dataset" \
                --scenario "$scenario" \
                --config-file "$config_file" \
                --output-dir "output/thinking_steering_generations" \
                --language en \
                --adaptive-mode 0 \
                --angle-start 0 \
                --angle-end 360 \
                --angle-step 10 \
                --max-tokens 16000 \
                --prompt-only \
                --run-baseline 
        done
    done
done