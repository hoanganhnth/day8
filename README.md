# Day 08 RAG - Group Repository

Repository chung cho bài Day 8 của nhóm.

## Structure

```text
day8/
├── group_project/                         # Sản phẩm và evaluation chung của nhóm
└── individual_submissions/                # Bài cá nhân của từng thành viên
    └── Day08-2A202600631-phamhoanganh/
```

`individual_submissions/` chỉ dùng để nộp kèm bài cá nhân trong cùng repo cho
thầy dễ chấm. Phần nhóm cần tập trung làm nằm trong `group_project/`.

## Collaboration Workflow

Mỗi thành viên đưa bài cá nhân vào:

```text
individual_submissions/Day08-<MSSV>-<hoten>/
```

Phần project nhóm chỉ được phát triển trong `group_project/`.

Mỗi nhiệm vụ dùng một branch riêng:

```bash
feature/data-preprocessing
feature/retrieval-pipeline
feature/generation-citation
feature/chatbot-ui
feature/evaluation-report
```

Không commit `.env`, API key, virtual environment, cache hoặc index được sinh tự động.

Đọc [BRANCH_RULES.md](BRANCH_RULES.md) trước khi làm. Mỗi branch chỉ sửa đúng
nhóm file được phân công để tránh conflict khi merge.

## Current Status

- Bài cá nhân: Tất cả các thành viên đã nộp kèm trong `individual_submissions/`.
- Group project: Tất cả các thành viên đã hoàn thành phần công việc của mình. Pipeline đã được tích hợp hoàn chỉnh (Chat UI, Retrieval, Generation có citation, và Evaluation A/B).
