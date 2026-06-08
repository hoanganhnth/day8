# Group Project - RAG Chatbot and Evaluation

## Goal

Tích hợp phần tốt nhất từ bài cá nhân của các thành viên thành chatbot RAG trả
lời câu hỏi về pháp luật ma túy và tin tức liên quan.

## Required Deliverables

- Chat UI chạy được.
- Trả lời có citation và hiển thị nguồn.
- Hỗ trợ follow-up questions.
- Golden dataset tối thiểu 15 câu.
- Evaluation: faithfulness, answer relevance, context recall, context precision.
- So sánh A/B ít nhất hai cấu hình.
- Báo cáo kết quả và phân tích ba trường hợp tệ nhất.

## Architecture

```text
Chat UI
  -> Integrated Retrieval
     -> Semantic Search
     -> Lexical Search
     -> Hybrid Merge
     -> Reranking / Fallback
  -> Generation with Citation
  -> Source Display
  -> Evaluation
```

## Project Structure

```text
group_project/
├── app.py
├── src/
│   ├── retrieval.py
│   ├── generation.py
│   ├── rag_pipeline.py
│   └── utils.py
├── evaluation/
│   ├── golden_dataset.json
│   ├── eval_pipeline.py
│   └── results.md
├── data_summary.md
└── README.md
```

## Branch Ownership

```text
feature/data-preprocessing  -> group_project/data_summary.md
feature/retrieval-pipeline  -> group_project/src/retrieval.py
feature/generation-citation -> group_project/src/generation.py
feature/chatbot-ui          -> group_project/app.py
feature/evaluation-report   -> group_project/evaluation/
```

Chi tiết xem `BRANCH_RULES.md` ở root repo.

## Integration Contract

`group_project/src/rag_pipeline.py` là boundary chung cho UI và evaluation:

```python
generate_answer(question: str, history: list[dict] | None = None) -> dict
```

Output bắt buộc:

```python
{
    "answer": "... [source.md]",
    "sources": [...],
    "history": [...],
    "question": "..."
}
```

## Team Assignment

| Thành viên | MSSV | Nhiệm vụ | Trạng thái |
|---|---|---|---|
| Phạm Hoàng Anh | 2A202600631 | Chat UI + conversation memory + source display (`feature/chatbot-ui`) | Đang làm |
| TBD | TBD | Data preprocessing + data summary (`feature/data-preprocessing`) | Chưa phân công |
| Nguyễn Dương Hiếu | 2A202600822 | Retrieval pipeline: semantic, BM25, hybrid, fallback (`feature/retrieval-pipeline`) | Hoàn thành |
| TBD | TBD | Generation + citation formatting (`feature/generation-citation`) | Chưa phân công |
| TBD | TBD | Evaluation A/B + `results.md` (`feature/evaluation-report`) | Chưa phân công |

## Run Scaffold

```bash
python3 -m pip install streamlit
streamlit run group_project/app.py
```

Scaffold hiện chỉ xác nhận giao diện chạy. Nhóm cần thay implementation trong
`group_project/src/rag_pipeline.py` bằng pipeline tích hợp đã thống nhất.
