# Branch Rules for Day 8 Group Project

File này là quy định làm việc nhóm. Mục tiêu là giảm conflict khi merge và đảm
bảo repo cuối cùng đúng yêu cầu bài nhóm.

## Branch Ownership

| Branch | Nhiệm vụ | Chỉ sửa các file/thư mục này |
|---|---|---|
| `feature/data-preprocessing` | Data inventory, chuẩn hóa dữ liệu, data summary | `group_project/data_summary.md`, `group_project/data/` nếu nhóm tạo data chung, `individual_submissions/<your-folder>/` của chính người đó |
| `feature/retrieval-pipeline` | Semantic search, lexical search, hybrid retrieval, fallback retrieval | `group_project/src/retrieval.py`, `group_project/src/utils.py`, có thể đọc từ `individual_submissions/` nhưng không sửa bài cá nhân của người khác |
| `feature/generation-citation` | Generation, citation formatting, source formatting, answer policy | `group_project/src/generation.py`, `group_project/src/utils.py` |
| `feature/chatbot-ui` | Streamlit UI, chat history, source display | `group_project/app.py` |
| `feature/evaluation-report` | Golden dataset, A/B evaluation, results report | `group_project/evaluation/`, `group_project/README.md` phần evaluation |

## Protected Files

Không tự ý sửa các file sau nếu không báo nhóm trước:

- `README.md`
- `group_project/README.md`
- `requirements.txt`
- `.gitignore`
- `.env.example`
- `group_project/src/rag_pipeline.py`

Nếu cần sửa protected file, ghi rõ trong Pull Request vì sao cần sửa.

## Merge Order

Merge theo thứ tự này để giảm lỗi phụ thuộc:

1. `feature/data-preprocessing`
2. `feature/retrieval-pipeline`
3. `feature/generation-citation`
4. `feature/chatbot-ui`
5. `feature/evaluation-report`
6. README final trên một branch nhỏ riêng nếu cần

## Required Group Deliverables

Trước khi nộp, repo nhóm phải có:

- Chat UI chạy được bằng Streamlit, Gradio hoặc Chainlit.
- Câu trả lời có citation.
- Hiển thị source documents đã dùng.
- Hỗ trợ follow-up questions hoặc conversation memory.
- Golden dataset tối thiểu 15 Q&A.
- Evaluation với faithfulness, answer relevance, context recall, context precision.
- So sánh A/B ít nhất hai cấu hình.
- `group_project/evaluation/results.md` có bảng điểm và phân tích lỗi.
- `README.md` hoặc `group_project/README.md` có kiến trúc, phân công, hướng dẫn chạy.

## Do Not Commit

Không commit:

- `.env`
- API keys
- `venv/`, `.venv/`
- `__pycache__/`, `*.pyc`
- `.deepeval/`
- generated vector DB/index files

## Pull Request Checklist

Trước khi mở PR:

- Chỉ sửa đúng file thuộc branch của mình.
- Chạy được phần mình phụ trách.
- Không làm hỏng import chung trong `group_project/src/rag_pipeline.py`.
- Mô tả rõ đã làm gì và cách test.
