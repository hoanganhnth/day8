"""A/B Evaluation pipeline for the group RAG system using DeepEval.

Config A: top_k=3, use_reranking=False  (baseline - semantic only)
Config B: top_k=5, use_reranking=True   (full pipeline - hybrid + reranking)

Run:
    cd d:/PROJECT/VinAi/day8
    python group_project/evaluation/eval_pipeline.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ── stdout encoding fix (Windows terminal) ───────────────────────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── Load API keys ─────────────────────────────────────────────────────────────
_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_root / ".env", override=True)  # repo root .env
load_dotenv(override=True)                            # cwd fallback

# ── DeepEval imports ──────────────────────────────────────────────────────────
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    FaithfulnessMetric,
)
from deepeval.models import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from openai import OpenAI

# ── Group RAG pipeline ────────────────────────────────────────────────────────
sys.path.insert(0, str(_root / "group_project"))
from src.rag_pipeline import generate_answer  # noqa: E402

DATASET_PATH = Path(__file__).with_name("golden_dataset.json")


# ── Custom LLM judge (supports both OpenAI and OpenRouter keys) ───────────────
class _JudgeLLM(DeepEvalBaseLLM):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key.startswith("sk-or-"):
            self._client = OpenAI(
                base_url="https://openrouter.ai/api/v1", api_key=api_key
            )
        else:
            self._client = OpenAI(api_key=api_key)

    def load_model(self):
        return self._client

    def generate(self, prompt: str) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=512,   # giới hạn để tiết kiệm credits OpenRouter
        )
        return resp.choices[0].message.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return self.model


# ── Core helpers ──────────────────────────────────────────────────────────────

def load_golden_dataset() -> list[dict]:
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))


def _build_metrics(judge: _JudgeLLM) -> list:
    kwargs = dict(threshold=0.5, strict_mode=False, model=judge)
    return [
        FaithfulnessMetric(**kwargs),
        AnswerRelevancyMetric(**kwargs),
        ContextualRecallMetric(**kwargs),
        ContextualPrecisionMetric(**kwargs),
    ]


def run_evaluation(
    dataset: list[dict],
    *,
    top_k: int,
    use_reranking: bool,
    label: str,
) -> tuple[list[LLMTestCase], object]:
    print(f"\n{'='*55}")
    print(f"  Config {label}  |  top_k={top_k}  |  reranking={use_reranking}")
    print(f"{'='*55}")

    test_cases: list[LLMTestCase] = []

    for idx, item in enumerate(dataset, start=1):
        q = item["question"]
        print(f"  [{idx}/{len(dataset)}] {q}")

        response = generate_answer(q, top_k=top_k, use_reranking=use_reranking)

        contexts = [
            (doc.get("content") or "") for doc in response.get("sources", [])
        ]
        if not contexts:
            contexts = [""]

        test_cases.append(
            LLMTestCase(
                input=q,
                actual_output=response["answer"],
                expected_output=item["expected_answer"],
                retrieval_context=contexts,
            )
        )

    judge = _JudgeLLM()
    metrics = _build_metrics(judge)
    print("\n  Đang chấm điểm bằng DeepEval …")
    results = evaluate(test_cases, metrics)
    return test_cases, results


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dataset = load_golden_dataset()

    # Chạy 3 câu đầu để tiết kiệm API (đổi thành `dataset` để chạy tất cả 16)
    subset = dataset[:3]

    print("🔬  Bắt đầu A/B Testing …")

    # Config A – Baseline: chỉ semantic search, top_k nhỏ
    cases_a, results_a = run_evaluation(
        subset, top_k=3, use_reranking=False, label="A"
    )

    # Config B – Full pipeline: hybrid search + reranking, top_k lớn hơn
    cases_b, results_b = run_evaluation(
        subset, top_k=5, use_reranking=True, label="B"
    )

    print("\n✅  Evaluation hoàn tất!")
    print("    Xem kết quả chi tiết ở trên rồi cập nhật evaluation/results.md.")
