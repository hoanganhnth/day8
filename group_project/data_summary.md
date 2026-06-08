# Data Summary

Người phụ trách: **Đoàn Minh Hiếu** (`feature/data-preprocessing`).

Tài liệu này kiểm kê bộ dữ liệu dùng chung của nhóm cho RAG pipeline về
**pháp luật ma tuý Việt Nam** và **tin tức nghệ sĩ liên quan tới ma tuý**.
Dữ liệu chuẩn hoá nằm trong `group_project/data/standardized/`, metadata nguồn
bài báo nằm trong `group_project/data/landing/news/`.

> **Cập nhật:** Bộ dữ liệu đã được thay bằng **nguồn thật, kiểm chứng được**.
> Mỗi văn bản luật có link nguồn chính thức; mỗi bài báo có URL gốc còn truy cập được.

## Legal Documents

| Source file | Văn bản | Nguồn chính thức |
|---|---|---|
| `standardized/legal/luat-phong-chong-ma-tuy-2021.md` | Luật Phòng, chống ma túy 2021 — số **73/2021/QH14**, hiệu lực 01/01/2022 | [thuvienphapluat](https://thuvienphapluat.vn/van-ban/Trach-nhiem-hinh-su/Luat-Phong-chong-ma-tuy-2021-445185.aspx) |
| `standardized/legal/nghi-dinh-105-2021-huong-dan-luat-phong-chong-ma-tuy.md` | Nghị định 105/2021/NĐ-CP — phối hợp, kiểm soát hoạt động hợp pháp, quản lý người sử dụng | [thuvienphapluat](https://thuvienphapluat.vn/van-ban/Van-hoa-Xa-hoi/Nghi-dinh-105-2021-ND-CP-huong-dan-Luat-Phong-chong-ma-tuy-496664.aspx) |
| `standardized/legal/nghi-dinh-57-2022-danh-muc-chat-ma-tuy.md` | Nghị định 57/2022/NĐ-CP — danh mục chất ma túy và tiền chất (25/08/2022) | [thuvienphapluat](https://thuvienphapluat.vn/van-ban/Van-hoa-Xa-hoi/Nghi-dinh-57-2022-ND-CP-danh-muc-chat-ma-tuy-va-tien-chat-527507.aspx) |
| `standardized/legal/bo-luat-hinh-su-2015-chuong-xx-ma-tuy.md` | Bộ luật Hình sự 2015 (số 100/2015/QH13, sửa đổi 2017) — Chương XX | [thuvienphapluat](https://thuvienphapluat.vn/van-ban/Trach-nhiem-hinh-su/Bo-luat-hinh-su-2015-296661.aspx) |

## News Articles

| Source file | Vụ việc | Nguồn / URL | Ngày đăng |
|---|---|---|---|
| `standardized/news/article_01.md` | Ca sĩ Châu Việt Cường — xét xử tội giết người (cơn ngáo đá) | [tuoitre.vn](https://tuoitre.vn/xet-xu-ca-si-chau-viet-cuong-vu-giet-nu-sinh-trong-con-ngao-da-20190307070436744.htm) | 07/03/2019 |
| `standardized/news/article_02.md` | Diễn viên hài Hữu Tín — 7 năm 6 tháng tù | [tuoitre.vn](https://tuoitre.vn/dien-vien-huu-tin-lanh-7-nam-6-thang-tu-20230428114919793.htm) | 28/04/2023 |
| `standardized/news/article_03.md` | Chi Dân, An Tây, Trúc Phương bị bắt vì ma túy | [tuoitre.vn](https://tuoitre.vn/bat-nguoi-mau-an-tay-ca-si-chi-dan-co-tien-truc-phuong-do-lien-quan-ma-tuy-20241114114826655.htm) | 14/11/2024 |
| `standardized/news/article_04.md` | NTK Nguyễn Công Trí bị bắt liên quan ma túy | [tuoitre.vn](https://tuoitre.vn/nha-thiet-ke-nguyen-cong-tri-bi-bat-vi-lien-quan-ma-tuy-20250723135411525.htm) | 23/07/2025 |
| `standardized/news/article_05.md` | Tổng hợp các nghệ sĩ bị bắt vì ma túy | [vietnamnet.vn](https://vietnamnet.vn/ngoai-nguyen-cong-tri-nhung-nghe-si-nao-tung-bi-bat-vi-ma-tuy-2424971.html) | 23/07/2025 |
| `standardized/news/article_06.md` | Chuyên án VN10 — truy tố 227 bị can (có Chi Dân, An Tây) | [tuoitre.vn](https://tuoitre.vn/chuyen-an-vn10-truy-to-227-bi-can-trong-do-co-ca-si-chi-dan-an-tay-2026040308051239.htm) | 03/04/2026 |

> Metadata đầy đủ (URL gốc, nguồn, tác giả, ngày đăng, ngày crawl) lưu trong file
> JSON tương ứng tại `group_project/data/landing/news/`.

## Dataset Quality Notes

- **Tổng số raw documents:** 10 (4 văn bản pháp luật + 6 bài báo).
- **Tổng số standardized markdown files:** 10 (`legal/`: 4, `news/`: 6).
- **Nguồn:** văn bản luật từ thuvienphapluat.vn (cổng văn bản); bài báo từ
  Tuổi Trẻ Online và VietNamNet, URL gốc còn truy cập được.
- **Chuẩn hoá:** toàn bộ ở dạng Markdown, giữ cấu trúc thư mục con `legal/` và
  `news/` để retrieval phân biệt loại nguồn.
- **Đã sửa các lỗi của bộ dữ liệu demo cũ:**
  - Thay 6 bài báo có URL bịa (không tồn tại) bằng 6 bài báo thật.
  - Sửa số hiệu Luật Phòng chống ma túy: **73/2021/QH15 → 73/2021/QH14** (đúng Quốc hội khoá XIV).
  - Sửa Nghị định 105/2021: nội dung cũ chép nhầm sang phần cai nghiện (thuộc Nghị định 116/2021), nay đã viết lại đúng phạm vi (phối hợp, kiểm soát hoạt động hợp pháp, quản lý người sử dụng).
- **Hạn chế còn lại:** nội dung văn bản luật là bản tóm lược các điều chính, chưa
  phải toàn văn — đã ghi rõ link nguồn ở đầu mỗi file để tra cứu đầy đủ.
- **Quyết định giữ/bỏ:** giữ toàn bộ 10 tài liệu; không nạp PDF gốc (dung lượng lớn),
  chỉ dùng bản Markdown đã chuẩn hoá cho indexing.

## Hand-off cho các task khác

- `feature/retrieval-pipeline`: index từ `group_project/data/standardized/`.
- Chunking gợi ý: tách theo heading cho văn bản luật (điều/khoản), recursive cho bài báo.
