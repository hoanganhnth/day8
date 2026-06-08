# Day 08 RAG - Group Repository

Repository chung cho bài Day 8 của nhóm.

## Structure

```text
day8/
├── group_project/                         # Sản phẩm và evaluation chung của nhóm
└── individual_submissions/                # Bài cá nhân của từng thành viên
    └── Day08-2A202600631-phamhoanganh/
```

## Collaboration Workflow

Mỗi thành viên đưa bài cá nhân vào:

```text
individual_submissions/Day08-<MSSV>-<hoten>/
```

Phần tích hợp chung chỉ được phát triển trong `group_project/`.

Khuyến nghị mỗi nhiệm vụ dùng một branch riêng:

```bash
git checkout -b feature/chatbot-ui
git checkout -b feature/integrated-retrieval
git checkout -b feature/evaluation
```

Không commit `.env`, API key, virtual environment, cache hoặc index được sinh tự động.

## Current Status

- Bài cá nhân Phạm Hoàng Anh: đã thêm, test cá nhân đạt 35/35.
- Group project: đã tạo scaffold, chưa tích hợp sản phẩm hoàn chỉnh.
