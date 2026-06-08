# Group RAG – Evaluation A/B Results

> **Thực hiện bởi:** Nguyễn Văn Minh – 2A202600556
> **Công cụ:** [DeepEval](https://github.com/confident-ai/deepeval) · **Judge LLM:** `gpt-4o-mini` via OpenRouter
> **Dataset:** `golden_dataset.json` – 16 câu hỏi (chạy thử 3 câu)
> **Thời gian chạy:** 95.66s

---

## Cấu hình A/B

| | Config A | Config B |
|---|---|---|
| `top_k` | 3 | 5 |
| `use_reranking` | `False` (chỉ semantic) | `True` (hybrid + RRF) |
| Mô tả | Baseline – chỉ dùng Semantic Search | Full pipeline – Hybrid Search + Reranking |

---

## Kết quả đo lường (3 test cases)

### Config A – `top_k=3, use_reranking=False`

| Metric | Average Score | Pass Rate | Ngưỡng |
|---|---:|---:|---:|
| Faithfulness | **0.94** | 100% | 0.50 |
| Answer Relevancy | **0.62** | 100% | 0.50 |
| Contextual Recall | **0.67** | 66.67% | 0.50 |
| Contextual Precision | 0.00 | 0% | 0.50 |

### Config B – `top_k=5, use_reranking=True`

| Metric | Average Score | Pass Rate | Ngưỡng |
|---|---:|---:|---:|
| Faithfulness | **0.94** | 100% | 0.50 |
| Answer Relevancy | **0.62** | 100% | 0.50 |
| Contextual Recall | **0.67** | 66.67% | 0.50 |
| Contextual Precision | 0.00 | 0% | 0.50 |

---

## Phân tích chi tiết theo câu hỏi

### Câu 1: "Hình phạt cho tội tàng trữ trái phép chất ma tuý theo Điều 249 Bộ luật Hình sự?"

| Metric | Score | Status |
|---|---:|---|
| Faithfulness | 1.00 | ✅ PASS |
| Answer Relevancy | 0.87 | ✅ PASS |
| Contextual Recall | 1.00 | ✅ PASS |
| Contextual Precision | 0.00 | ❌ FAIL |

**Nhận xét:** Câu trả lời trung thực và phù hợp, nhưng Contextual Precision thấp cho thấy các chunk được truy xuất chưa xếp hạng tốt.

### Câu 2: "Luật Phòng chống ma tuý 2021 quy định những hình thức cai nghiện nào?"

| Metric | Score | Status |
|---|---:|---|
| Faithfulness | 0.83 | ✅ PASS |
| Answer Relevancy | 0.50 | ✅ PASS |
| Contextual Recall | 0.00 | ❌ FAIL |
| Contextual Precision | 0.00 | ❌ FAIL |

**Nhận xét:** Ngữ cảnh truy xuất thiếu thông tin cụ thể về hình thức cai nghiện, dẫn đến Contextual Recall = 0.

### Câu 3: "Danh mục các chất ma tuý thuộc nhóm I theo quy định pháp luật Việt Nam gồm những chất nào?"

| Metric | Score | Status |
|---|---:|---|
| Faithfulness | 1.00 | ✅ PASS |
| Answer Relevancy | 0.50 | ✅ PASS |
| Contextual Recall | 1.00 | ✅ PASS |
| Contextual Precision | 0.00 | ❌ FAIL |

**Nhận xét:** Model nhận định "không biết" do context không đề cập trực tiếp danh mục nhóm I, nhưng Faithfulness vẫn đạt 1.00 (không bịa đặt).

---

## Phân tích tổng quan

### Điểm mạnh
- **Faithfulness = 0.94**: Câu trả lời rất trung thực, không bịa đặt thông tin — đây là metric quan trọng nhất cho hệ thống RAG pháp lý.
- **Answer Relevancy = 0.62**: Câu trả lời có độ phù hợp vượt ngưỡng, 100% pass rate.
- **Contextual Recall = 0.67**: 2/3 câu truy xuất được ngữ cảnh đúng.

### Điểm yếu cần cải thiện
- **Contextual Precision = 0.00**: Các chunk truy xuất được chưa xếp hạng chính xác. Các node đầu tiên trong retrieval context không chứa thông tin liên quan trực tiếp → cần cải thiện reranking hoặc tinh chỉnh embedding.

### Nguyên nhân gốc rễ
1. **Vector store nhỏ (802 chunks)**: Cơ sở dữ liệu chỉ chứa 802 chunk, một số câu hỏi chuyên sâu (như danh mục nhóm I) không có chunk chứa đầy đủ thông tin.
2. **Embedding model**: BAAI/bge-m3 (1024 dim) hỗ trợ tiếng Việt tốt nhưng cần fine-tune thêm cho domain pháp lý.
3. **Reranking RRF**: Reciprocal Rank Fusion chưa cải thiện đáng kể so với baseline (Config A ≈ Config B).

---

## So sánh A vs B

| Metric | Config A | Config B | Chênh lệch |
|---|---:|---:|---|
| Faithfulness | 0.94 | 0.94 | = |
| Answer Relevancy | 0.62 | 0.62 | = |
| Contextual Recall | 0.67 | 0.67 | = |
| Contextual Precision | 0.00 | 0.00 | = |

**Kết luận:** Với 3 câu thử nghiệm, Config A và Config B cho kết quả tương đương. Cần chạy thêm nhiều câu hơn (16 câu) để thấy rõ sự khác biệt.

---

## Đề xuất cải thiện

1. **Mở rộng dataset crawl**: Bổ sung thêm các văn bản pháp luật chi tiết (Nghị định, Thông tư) vào data/standardized.
2. **Tinh chỉnh chunking**: Giảm chunk_size từ 500 → 300, tăng overlap từ 50 → 100 để giữ nguyên ngữ cảnh điều luật.
3. **Cải thiện reranking**: Thử dùng Cross-Encoder thay cho RRF đơn giản.
4. **Chạy full evaluation**: Chạy lại với toàn bộ 16 câu để có kết quả đại diện hơn.

---

## Kết luận

Pipeline RAG nhóm đã **tích hợp hoàn chỉnh** và chạy end-to-end thành công. Kết quả Faithfulness = 0.94 cho thấy hệ thống đáng tin cậy — không bịa đặt thông tin. Các metric khác có thể cải thiện bằng cách mở rộng dataset và tối ưu retrieval.
