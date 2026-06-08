# Day 08 — RAG Pipeline (bản cá nhân)

**Tác giả:** Đoàn Minh Hiếu — MSSV `2A202600841`

Pipeline RAG end-to-end về **pháp luật ma túy Việt Nam** và **tin tức nghệ sĩ
liên quan ma túy**: thu thập → chuẩn hoá → chunk/index → retrieval (hybrid +
vectorless fallback) → generation có citation.

> Bản này được **viết lại từ đầu** (cấu trúc lõi `rag_core.py` riêng), ưu tiên
> chạy được mọi nơi bằng thuần Python, và để sẵn "cửa" cắm thư viện/dịch vụ thật.

## Cấu trúc

```
Day08_RAG_pipeline_cohort2/
├── data/
│   ├── landing/{legal,news}/      # file gốc (PDF luật, JSON bài báo)
│   └── standardized/{legal,news}/ # markdown đã chuẩn hoá (dùng để index)
├── src/
│   ├── rag_core.py                # lõi: tokenize, TF-IDF, BM25, RRF, chunking
│   ├── task1_collect_legal_docs.py
│   ├── task2_crawl_news.py
│   ├── task3_convert_markdown.py
│   ├── task4_chunking_indexing.py # CHUNK_SIZE=800, OVERLAP=120
│   ├── task5_semantic_search.py   # TF-IDF cosine (cửa cắm sentence-transformers)
│   ├── task6_lexical_search.py    # BM25 (rank-bm25 nếu có, không thì thuần Python)
│   ├── task7_reranking.py         # re-score theo độ liên quan từ khoá (+cửa cross-encoder)
│   ├── task8_pageindex_vectorless.py # fallback vectorless
│   ├── task9_retrieval_pipeline.py   # hybrid (RRF) + rerank + fallback
│   └── task10_generation.py       # reorder chống lost-in-the-middle + citation + cửa LLM
└── tests/test_individual.py       # bộ test chấm điểm
```

## Cài đặt & chạy

```bash
pip install -r requirements.txt          # tối thiểu chỉ cần pytest
# (tuỳ chọn) cp .env.example .env  rồi điền API key để bật bản "thật"
```

## Chạy test

```bash
pytest tests/test_individual.py -v       # kỳ vọng: 35 passed
```

Chạy thử từng module:

```bash
python -m src.task5_semantic_search
python -m src.task6_lexical_search
python -m src.task9_retrieval_pipeline
python -m src.task10_generation
```

## Lựa chọn kỹ thuật (tóm tắt để demo)

| Task | Cách làm | Ghi chú |
|---|---|---|
| Chunking | cắt ký tự có overlap, ngắt theo ranh giới đoạn/câu | 800/120 |
| Semantic | TF-IDF + cosine | cửa cắm `sentence-transformers` |
| Lexical | BM25 Okapi | `rank-bm25` hoặc bản thuần Python |
| Rerank | re-score độ trùng từ khoá + điểm gốc | cửa cắm cross-encoder |
| Vectorless | tra cứu từ khoá gắn `source=pageindex` | cửa cắm PageIndex SDK |
| Hybrid | RRF gộp semantic+lexical, fallback khi điểm < ngưỡng | |
| Generation | reorder + citation; LLM nếu có `OPENAI_API_KEY`, không thì extractive | top_p=0.9, temp=0.2 |

## Nguồn dữ liệu

Văn bản luật: thuvienphapluat.vn (Luật 73/2021/QH14, NĐ 105/2021, NĐ 57/2022,
BLHS 2015 Chương XX). Bài báo: Tuổi Trẻ, VietNamNet (URL gốc lưu trong JSON tại
`data/landing/news/`).
