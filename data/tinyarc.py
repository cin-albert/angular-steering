from pydantic import BaseModel
from typing import Any
from datasets import load_dataset
import random


class ArcSample(BaseModel):
    id: str
    question: str
    choices: dict[str, Any]
    answerKey: str
    grade: int
    
    @property
    def formatted_choices(self) -> list[str]:
        return [f"{key}. {text}" for key, text in zip(self.choices["label"], self.choices["text"])]

    @property
    def user_message(self) -> str:
        choices_str = "\n".join(self.formatted_choices)
        return f"{self.question}\nChoices: {choices_str}\nReturn the key of the correct choice only."


def load_arc_samples(
    data_files: str, num_samples: int | None = None, shuffle: bool = False, seed: int = 42) -> list[ArcSample]:
    ds = load_dataset("LoneResearch/TinyARC", data_files=data_files)["train"]

    samples = []
    iter = ds.iter(batch_size=1)
    for sample in iter:
        item = ArcSample(
            id=sample["id"][0],
            question=sample["question"][0],
            choices=sample["choices"][0],
            answerKey=sample["answerKey"][0],
            grade=sample["grade"][0],
        )
        samples.append(item)

    if shuffle:
        random.seed(seed)
        random.shuffle(samples)
    if num_samples is not None:
        samples = samples[:num_samples]
    return samples