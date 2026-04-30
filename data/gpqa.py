from pydantic import BaseModel
from datasets import load_dataset
import random

LABELS = ["A", "B", "C", "D"]


class GpqaSample(BaseModel):
    question: str
    correct_answer: str
    incorrect_answers: list[str]  # exactly 3 items
    gold_index: int  # 0–3, position of correct_answer after shuffling

    @property
    def choices(self) -> list[str]:
        """Ordered [A, B, C, D] choices with correct answer at gold_index."""
        opts = list(self.incorrect_answers)
        opts.insert(self.gold_index, self.correct_answer)
        return opts

    @property
    def answer_key(self) -> str:
        """Letter label of the correct answer ('A'–'D')."""
        return LABELS[self.gold_index]

    @property
    def formatted_choices(self) -> list[str]:
        return [f"{label}) {text.strip()}" for label, text in zip(LABELS, self.choices)]

    @property
    def user_message(self) -> str:
        choices_str = "\n".join(self.formatted_choices)
        return f"{self.question.strip()}\nChoices: {choices_str}\nReturn the key of the correct choice only."


def load_gpqa_diamond_samples(
    num_samples: int | None = None,
    shuffle: bool = False,
    seed: int = 42,
) -> list[GpqaSample]:
    """
    Load GPQA-Diamond samples from Idavidrein/gpqa (config: gpqa_diamond).

    The dataset is gated on Hugging Face; run `huggingface-cli login` and
    accept the terms on the dataset page before calling this function.

    Args:
        num_samples: If set, truncate to this many samples after optional shuffle.
        shuffle:     If True, shuffle the sample order using `seed`.
        seed:        RNG seed for both answer-option ordering and sample shuffle.
    """
    dataset = load_dataset("Idavidrein/gpqa", "gpqa_diamond", split="train")
    rng = random.Random(seed)

    samples: list[GpqaSample] = []
    for row in dataset:
        gold_index = rng.randint(0, 3)
        samples.append(
            GpqaSample(
                question=row["Question"],
                correct_answer=row["Correct Answer"],
                incorrect_answers=[
                    row["Incorrect Answer 1"],
                    row["Incorrect Answer 2"],
                    row["Incorrect Answer 3"],
                ],
                gold_index=gold_index,
            )
        )

    if shuffle:
        random.seed(seed)
        random.shuffle(samples)
    if num_samples is not None:
        samples = samples[:num_samples]
    return samples
