"""Validation scaffold for the group golden dataset and future A/B evaluation."""

from __future__ import annotations

import json
from pathlib import Path


DATASET_PATH = Path(__file__).with_name("golden_dataset.json")


def load_golden_dataset() -> list[dict]:
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))


def validate_golden_dataset(dataset: list[dict]) -> None:
    if len(dataset) < 15:
        raise ValueError(f"Golden dataset cần ít nhất 15 cases, hiện có {len(dataset)}")

    required = {"question", "expected_answer", "expected_context"}
    for index, item in enumerate(dataset, start=1):
        missing = required - item.keys()
        if missing:
            raise ValueError(f"Case {index} thiếu fields: {sorted(missing)}")


if __name__ == "__main__":
    golden_dataset = load_golden_dataset()
    validate_golden_dataset(golden_dataset)
    print(f"Golden dataset hợp lệ: {len(golden_dataset)} cases")
    print("Bước tiếp theo: tích hợp Config A/B và xuất evaluation/results.md.")
