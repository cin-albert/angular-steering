import json
import logging
from pathlib import Path
import sys
from enum import StrEnum, auto

from vllm import LLM
from vllm.sampling_params import SamplingParams
from pydantic import BaseModel
from datasets import load_dataset

logging.basicConfig(level=getattr(logging, "INFO", logging.INFO))
logger = logging.getLogger(__name__)

TEMPERATURE = 0
MAX_TOKENS = 16000

sampling_params = SamplingParams(temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
print(f"Sampling params: {sampling_params}")


class ReasoningStrategy(StrEnum):
    DEFAULT = auto()
    AVOID_OVERTHINKING = auto()
    TRY_DIFFERENT_APPROACHES = auto()


def add_prompt_postfix(
    prompt: str,
    strategy: ReasoningStrategy = ReasoningStrategy.DEFAULT
) -> str:
    if not (prompt.endswith(".") or prompt.endswith("?") or prompt.endswith("!") or prompt.endswith("\n")):
        prompt += "."
    match strategy:
        case ReasoningStrategy.DEFAULT:
            return prompt
        case ReasoningStrategy.AVOID_OVERTHINKING:
            return prompt + " Avoid overthinking, you should answer immediately when you derive the first answer."
        case ReasoningStrategy.TRY_DIFFERENT_APPROACHES:
            return prompt + " Try different approaches and verify every step carefully."
        case _:
            raise ValueError(f"Invalid reasoning strategy: {strategy}")


model_ids = [
    "deepseek-ai/DeepSeek-R1-Distill-LLama-8B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "Qwen/Qwen3-14B",
    "Qwen/Qwen3-32B",
]

reasoning_strategies = [
    ReasoningStrategy.DEFAULT,
    ReasoningStrategy.AVOID_OVERTHINKING,
    ReasoningStrategy.TRY_DIFFERENT_APPROACHES,
]


class Response(BaseModel):
    prompt: str
    response: str | int | None = None


def get_math500_instructions():
    huggingface_id = "HuggingFaceH4/MATH-500"
    dataset = load_dataset(huggingface_id, split="test")
    instructions = [sample["problem"] for sample in dataset]
    return instructions


def get_tinylivecodebench_instructions() -> list[str]:
    huggingface_id = "LoneResearch/TinyLiveCodeBench"
    dataset = load_dataset(huggingface_id)
    instructions = [sample["full_prompt"] for sample in dataset["test"]]
    return instructions


def get_gpqa_diamond_instructions() -> list[str]:
    from data.gpqa import load_gpqa_diamond_samples

    samples = load_gpqa_diamond_samples()
    return [sample.user_message for sample in samples]


def get_data_test(dataset: str) -> list[str]:
    match dataset:
        case "math500":
            return get_math500_instructions()
        case "tinylivecodebench":
            return get_tinylivecodebench_instructions()
        case "gpqa_diamond":
            return get_gpqa_diamond_instructions()
        case _:
            raise ValueError(f"Invalid dataset: {dataset}")


def run_inference(dataset: str):
    global reasoning_strategies
    global model_ids

    data_test = get_data_test(dataset)

    for model_id in model_ids:
        model_name = model_id.split("/")[-1] if "/" in model_id else model_id

        llm = LLM(
            model=model_id,
            max_model_len=16000,
            gpu_memory_utilization=0.9,
        )

        for reasoning_strategy in reasoning_strategies:
            logger.info(f"Processing model: {model_id}, reasoning strategy: {reasoning_strategy}")
            logger.info("--------------------------------")

            output_path = Path("output") / model_name / dataset
            output_path.mkdir(parents=True, exist_ok=True)

            conversations = [
                [
                    {
                        "role": "user",
                        "content": add_prompt_postfix(sample, reasoning_strategy),
                    }
                ]
                for sample in data_test
            ]

            responses = []
            outputs = llm.chat(
                conversations,
                sampling_params=sampling_params,
            )
            responses.extend(
                [
                    Response(
                        prompt=add_prompt_postfix(sample, reasoning_strategy),
                        response=item.outputs[0].text,
                    )
                    for i, (sample, item) in enumerate(zip(data_test, outputs))
                ]
            )
            with open(output_path / f"{reasoning_strategy.value}.json", "w", encoding="utf-8") as f:
                responses_dict = [response.model_dump() for response in responses]
                json.dump(responses_dict, f, indent=4, ensure_ascii=False)

        del llm


if __name__ == "__main__":
    dataset = sys.argv[1]
    run_inference(dataset)
