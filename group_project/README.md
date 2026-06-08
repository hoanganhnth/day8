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
│   └── rag_pipeline.py
├── evaluation/
│   ├── golden_dataset.json
│   └── eval_pipeline.py
└── README.md
```

## Team Assignment

| Thành viên | MSSV | Nhiệm vụ | Trạng thái |
|---|---|---|---|
| Phạm Hoàng Anh | 2A202600631 | Đề xuất pipeline cá nhân làm baseline | Hoàn thành baseline |
| | | Chat UI và conversation memory | Chưa phân công |
| | | Retrieval integration và reranking | Chưa phân công |
| | | Evaluation A/B và results.md | Chưa phân công |

## Run Scaffold

```bash
python3 -m pip install streamlit
streamlit run group_project/app.py
```

Scaffold hiện chỉ xác nhận giao diện chạy. Nhóm cần thay implementation trong
`group_project/src/rag_pipeline.py` bằng pipeline tích hợp đã thống nhất.
