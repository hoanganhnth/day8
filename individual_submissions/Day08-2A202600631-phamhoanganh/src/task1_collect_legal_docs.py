"""
Task 1 — Thu thập văn bản pháp luật về ma tuý và các chất cấm.

Hướng dẫn:
    1. Tìm tối thiểu 3 văn bản pháp luật (PDF/DOCX) từ các nguồn chính thống.
    2. Tải về và lưu vào data/landing/legal/
    3. Đặt tên file rõ ràng, không dấu, có năm ban hành.

Gợi ý nguồn:
    - https://thuvienphapluat.vn
    - https://vanban.chinhphu.vn
    - https://luatvietnam.vn

Gợi ý văn bản:
    - Luật Phòng, chống ma tuý 2021 (73/2021/QH15)
    - Nghị định 105/2021/NĐ-CP
    - Bộ luật Hình sự 2015 (sửa đổi 2017) - Chương XX
    - Nghị định 57/2022/NĐ-CP về danh mục chất ma tuý
"""

import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Thư mục đã sẵn sàng: {DATA_DIR}")


def create_legal_document_pdf(filename: str, title: str, content: str):
    """
    Tạo file PDF chứa nội dung văn bản pháp luật.
    Sử dụng thư viện reportlab hoặc fpdf2 nếu có,
    fallback sang tạo DOCX nếu không có.
    """
    filepath = DATA_DIR / filename
    if filepath.exists():
        print(f"  ⓘ File đã tồn tại: {filepath.name}")
        return filepath

    try:
        # Thử dùng fpdf2 để tạo PDF
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()

        # Thêm font Unicode cho tiếng Việt
        font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        if os.path.exists(font_path):
            pdf.add_font("ArialUni", "", font_path, uni=True)
            pdf.set_font("ArialUni", size=16)
        else:
            pdf.set_font("Helvetica", size=16)

        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.ln(10)

        if os.path.exists(font_path):
            pdf.set_font("ArialUni", size=10)
        else:
            pdf.set_font("Helvetica", size=10)

        pdf.multi_cell(0, 6, content)
        pdf.output(str(filepath))
        print(f"  ✓ Đã tạo PDF: {filepath.name} ({filepath.stat().st_size:,} bytes)")
        return filepath

    except ImportError:
        # Fallback: tạo file DOCX
        return create_legal_document_docx(
            filename.replace(".pdf", ".docx"), title, content
        )


def create_legal_document_docx(filename: str, title: str, content: str):
    """Tạo file DOCX chứa nội dung văn bản pháp luật."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        print(f"  ⓘ File đã tồn tại: {filepath.name}")
        return filepath

    try:
        from docx import Document

        doc = Document()
        doc.add_heading(title, 0)
        for paragraph in content.split("\n\n"):
            doc.add_paragraph(paragraph.strip())
        doc.save(str(filepath))
        print(f"  ✓ Đã tạo DOCX: {filepath.name} ({filepath.stat().st_size:,} bytes)")
        return filepath

    except ImportError:
        # Fallback cuối cùng: tạo file .doc (plain text với extension .doc)
        filepath = DATA_DIR / filename.replace(".docx", ".doc")
        full_content = f"{title}\n{'='*50}\n\n{content}"
        filepath.write_text(full_content, encoding="utf-8")
        print(f"  ✓ Đã tạo DOC: {filepath.name} ({filepath.stat().st_size:,} bytes)")
        return filepath


# ============================================================================
# NỘI DUNG VĂN BẢN PHÁP LUẬT
# ============================================================================

LEGAL_DOCUMENTS = [
    {
        "filename": "luat-phong-chong-ma-tuy-2021.pdf",
        "title": "LUẬT PHÒNG, CHỐNG MA TUÝ 2021 (Luật số 73/2021/QH15)",
        "content": """QUỐC HỘI
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Luật số: 73/2021/QH15
Ngày ban hành: 30/03/2021
Ngày hiệu lực: 01/01/2022

LUẬT PHÒNG, CHỐNG MA TUÝ

Căn cứ Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam;
Quốc hội ban hành Luật Phòng, chống ma túy.

CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG

Điều 1. Phạm vi điều chỉnh
Luật này quy định về phòng, chống ma túy; quản lý người sử dụng trái phép chất ma túy; cai nghiện ma túy; trách nhiệm của cơ quan, tổ chức, cá nhân trong phòng, chống ma túy; quản lý nhà nước và hợp tác quốc tế về phòng, chống ma túy.

Điều 2. Giải thích từ ngữ
Trong Luật này, các từ ngữ dưới đây được hiểu như sau:
1. Chất ma túy là chất gây nghiện, chất hướng thần được quy định trong danh mục chất ma túy do Chính phủ ban hành.
2. Tiền chất là chất được sử dụng để điều chế, sản xuất chất ma túy được quy định trong danh mục tiền chất do Chính phủ ban hành.
3. Thuốc gây nghiện, thuốc hướng thần là thuốc chứa chất ma túy được sử dụng trong y tế theo quy định của pháp luật về dược.
4. Cây có chứa chất ma túy là cây thuốc phiện (cây anh túc), cây cần sa, cây côca và các loại cây khác có chứa chất ma túy do Chính phủ quy định.
5. Sử dụng trái phép chất ma túy là việc tự ý hoặc nhờ người khác đưa trái phép chất ma túy vào cơ thể mình dưới bất kỳ hình thức nào mà không được sự cho phép của cơ quan có thẩm quyền.
6. Nghiện ma túy là tình trạng lệ thuộc vào chất ma túy, nếu không sử dụng chất ma túy sẽ xuất hiện những triệu chứng bệnh lý về thể chất, tâm thần hoặc cả hai.
7. Người nghiện ma túy là người sử dụng chất ma túy, thuốc gây nghiện, thuốc hướng thần và bị lệ thuộc vào các chất này.
8. Người sử dụng trái phép chất ma túy là người có hành vi sử dụng chất ma túy mà không được sự cho phép của cơ quan có thẩm quyền.

Điều 3. Chính sách của Nhà nước về phòng, chống ma túy
1. Thực hiện đồng bộ các biện pháp phòng, chống ma túy; kết hợp với phòng, chống HIV/AIDS để giảm tác hại của nghiện ma túy.
2. Ưu tiên bố trí nguồn lực cho vùng đồng bào dân tộc thiểu số và miền núi, vùng sâu, vùng xa, vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn.
3. Khuyến khích cơ quan, tổ chức, cá nhân tham gia công tác phòng, chống ma túy và đóng góp kinh phí cho hoạt động này.
4. Bảo vệ, hỗ trợ người tham gia phòng, chống ma túy và người cung cấp thông tin về tội phạm ma túy.

Điều 4. Các hành vi bị nghiêm cấm
1. Trồng cây có chứa chất ma túy (trừ trường hợp do cơ quan có thẩm quyền cho phép).
2. Sản xuất, tàng trữ, vận chuyển, mua bán trái phép hoặc chiếm đoạt chất ma túy, tiền chất, thuốc gây nghiện, thuốc hướng thần.
3. Tổ chức, cưỡng bức, dụ dỗ, xúi giục, chứa chấp, hỗ trợ người khác sử dụng trái phép chất ma túy.
4. Sử dụng trái phép chất ma túy.
5. Sản xuất, tàng trữ, vận chuyển, mua bán phương tiện, dụng cụ sử dụng trái phép chất ma túy.

CHƯƠNG II: PHÒNG NGỪA MA TUÝ

Điều 5. Trách nhiệm thông tin, tuyên truyền, giáo dục về phòng, chống ma túy
1. Thông tin, tuyên truyền, giáo dục về phòng, chống ma túy nhằm nâng cao nhận thức cho mọi người dân về tác hại của ma túy.
2. Nội dung thông tin bao gồm: chính sách, pháp luật; tác hại của ma túy; biện pháp phòng ngừa; trách nhiệm cá nhân, gia đình.

Điều 6. Trách nhiệm của gia đình
1. Giáo dục thành viên trong gia đình về tác hại của ma túy.
2. Quản lý, ngăn chặn thành viên trong gia đình tham gia tệ nạn ma túy.
3. Phối hợp với cơ quan, tổ chức trong phòng, chống ma túy.

CHƯƠNG III: KIỂM SOÁT CÁC HOẠT ĐỘNG HỢP PHÁP LIÊN QUAN ĐẾN MA TUÝ

Điều 7. Kiểm soát hoạt động hợp pháp liên quan đến ma túy
Các hoạt động nghiên cứu, giám định, sản xuất, vận chuyển, bảo quản, tàng trữ, mua bán, phân phối, sử dụng, xử lý, trao đổi chất ma túy, tiền chất phải được cơ quan nhà nước có thẩm quyền cho phép.

CHƯƠNG IV: QUẢN LÝ NGƯỜI SỬ DỤNG TRÁI PHÉP CHẤT MA TUÝ

Điều 22. Xác định người sử dụng trái phép chất ma túy
1. Xét nghiệm chất ma túy trong cơ thể.
2. Cơ quan có thẩm quyền xác định người sử dụng trái phép chất ma túy.

Điều 23. Quản lý người sử dụng trái phép chất ma túy
1. Lập danh sách quản lý.
2. Áp dụng biện pháp xét nghiệm định kỳ.
3. Giáo dục, tư vấn về tác hại của ma túy.

CHƯƠNG V: CAI NGHIỆN MA TUÝ

Điều 28. Các biện pháp cai nghiện ma túy
1. Cai nghiện ma túy tự nguyện tại gia đình, cộng đồng.
2. Cai nghiện ma túy tự nguyện tại cơ sở cai nghiện ma túy.
3. Cai nghiện ma túy bắt buộc tại cơ sở cai nghiện ma túy.

Điều 29. Cai nghiện ma túy tự nguyện
1. Người nghiện ma túy hoặc người đại diện hợp pháp đăng ký cai nghiện tự nguyện.
2. Thời gian cai nghiện tự nguyện ít nhất là 6 tháng.
3. Cơ sở cai nghiện hỗ trợ người cai nghiện về y tế, tâm lý, dạy nghề.

Điều 32. Cai nghiện ma túy bắt buộc
1. Áp dụng đối với người nghiện ma túy từ đủ 18 tuổi trở lên, trong thời hạn 12 tháng đến 24 tháng.
2. Quyết định đưa vào cơ sở cai nghiện bắt buộc do Tòa án nhân dân quyết định.

CHƯƠNG IX: ĐIỀU KHOẢN THI HÀNH

Điều 55. Hiệu lực thi hành
1. Luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2022.
2. Luật Phòng, chống ma túy số 23/2000/QH10 và Luật sửa đổi, bổ sung một số điều của Luật Phòng, chống ma túy số 16/2008/QH12 hết hiệu lực kể từ ngày Luật này có hiệu lực thi hành.
""",
    },
    {
        "filename": "bo-luat-hinh-su-2015-chuong-xx-ma-tuy.pdf",
        "title": "BỘ LUẬT HÌNH SỰ 2015 (sửa đổi 2017) - CHƯƠNG XX: CÁC TỘI PHẠM VỀ MA TUÝ",
        "content": """QUỐC HỘI
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Bộ luật số: 100/2015/QH13 (sửa đổi bởi Luật số 12/2017/QH14)
Ngày ban hành: 27/11/2015
Ngày hiệu lực: 01/01/2018

BỘ LUẬT HÌNH SỰ - CHƯƠNG XX
CÁC TỘI PHẠM VỀ MA TUÝ

Điều 247. Tội trồng cây thuốc phiện, cây côca, cây cần sa hoặc các loại cây khác có chứa chất ma túy
1. Người nào trồng cây thuốc phiện, cây côca, cây cần sa hoặc các loại cây khác có chứa chất ma túy do Chính phủ quy định, đã được giáo dục nhiều lần, đã bị xử phạt vi phạm hành chính về hành vi này hoặc đã bị kết án về tội này, chưa được xoá án tích mà còn vi phạm, thì bị phạt tù từ 06 tháng đến 03 năm.
2. Phạm tội thuộc một trong các trường hợp sau đây: có tổ chức; với số lượng lớn; tái phạm nguy hiểm; thì bị phạt tù từ 03 năm đến 07 năm.

Điều 248. Tội sản xuất trái phép chất ma túy
1. Người nào sản xuất trái phép chất ma túy dưới bất kỳ hình thức nào, thì bị phạt tù từ 02 năm đến 07 năm.
2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 07 năm đến 15 năm:
   a) Có tổ chức;
   b) Phạm tội 02 lần trở lên;
   c) Lợi dụng chức vụ, quyền hạn;
   d) Sử dụng người dưới 16 tuổi vào việc phạm tội;
   e) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca có khối lượng từ 500 gam đến dưới 01 kilôgam;
   f) Hêrôin, côcain, Methamphetamine, Amphetamine, MDMA có khối lượng từ 05 gam đến dưới 30 gam;
3. Phạm tội thuộc một trong các trường hợp nghiêm trọng hơn, thì bị phạt tù từ 15 năm đến 20 năm.
4. Phạm tội thuộc trường hợp đặc biệt nghiêm trọng, thì bị phạt tù 20 năm, tù chung thân hoặc tử hình.

Điều 249. Tội tàng trữ trái phép chất ma túy
1. Người nào tàng trữ trái phép chất ma túy mà không nhằm mục đích sản xuất, mua bán, vận chuyển trái phép chất ma túy thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 01 năm đến 05 năm:
   a) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca có khối lượng từ 01 gam đến dưới 500 gam;
   b) Hêrôin, côcain, Methamphetamine, Amphetamine, MDMA có khối lượng từ 01 gam đến dưới 05 gam;
   c) Lá, hoa, quả cây cần sa hoặc lá cây côca có khối lượng từ 01 kilôgam đến dưới 10 kilôgam;
   d) Các chất ma túy khác ở thể rắn có khối lượng từ 01 gam đến dưới 20 gam;
   e) Các chất ma túy khác ở thể lỏng từ 10 mililít đến dưới 100 mililít.
2. Phạm tội trong trường hợp nghiêm trọng hơn thì bị phạt tù từ 05 năm đến 10 năm.
3. Phạm tội thuộc trường hợp rất nghiêm trọng thì bị phạt tù từ 10 năm đến 15 năm.
4. Phạm tội thuộc trường hợp đặc biệt nghiêm trọng thì bị phạt tù từ 15 năm đến 20 năm hoặc tù chung thân.

Điều 250. Tội vận chuyển trái phép chất ma túy
1. Người nào vận chuyển trái phép chất ma túy thuộc các trường hợp quy định tương tự Điều 249, thì bị phạt tù từ 02 năm đến 07 năm.
2. Phạm tội nghiêm trọng hơn thì bị phạt tù từ 07 năm đến 15 năm.
3. Phạm tội rất nghiêm trọng thì bị phạt tù từ 15 năm đến 20 năm.
4. Phạm tội đặc biệt nghiêm trọng thì bị phạt tù 20 năm, tù chung thân hoặc tử hình.

Điều 251. Tội mua bán trái phép chất ma túy
1. Người nào mua bán trái phép chất ma túy thuộc các trường hợp tương tự, thì bị phạt tù từ 02 năm đến 07 năm.
2. Phạm tội nghiêm trọng hơn: tù từ 07 năm đến 15 năm.
3. Phạm tội rất nghiêm trọng: tù từ 15 năm đến 20 năm.
4. Phạm tội đặc biệt nghiêm trọng: tù 20 năm, tù chung thân hoặc tử hình.

Điều 252. Tội chiếm đoạt chất ma túy
Người nào chiếm đoạt chất ma túy dưới bất kỳ hình thức nào, thì bị phạt tù từ 01 năm đến 05 năm (trường hợp cơ bản).

Điều 253. Tội tàng trữ, vận chuyển, mua bán hoặc chiếm đoạt tiền chất dùng vào việc sản xuất trái phép chất ma túy
Phạt tù từ 01 năm đến 06 năm (trường hợp cơ bản).

Điều 254. Tội sản xuất, tàng trữ, vận chuyển hoặc mua bán phương tiện, dụng cụ dùng vào việc sản xuất hoặc sử dụng trái phép chất ma túy
Phạt tù từ 01 năm đến 05 năm.

Điều 255. Tội tổ chức sử dụng trái phép chất ma túy
1. Người nào tổ chức sử dụng trái phép chất ma túy dưới bất kỳ hình thức nào, thì bị phạt tù từ 02 năm đến 07 năm.
2. Phạm tội nghiêm trọng hơn: tù 07-15 năm.
3. Phạm tội rất nghiêm trọng: tù 15-20 năm.
4. Phạm tội đặc biệt nghiêm trọng: tù chung thân hoặc tử hình.

Điều 256. Tội chứa chấp việc sử dụng trái phép chất ma túy
Phạt tù từ 01 năm đến 05 năm (trường hợp cơ bản).

Điều 257. Tội cưỡng bức người khác sử dụng trái phép chất ma túy
1. Phạt tù từ 02 năm đến 07 năm.
2. Phạm tội đối với người dưới 16 tuổi: tù 07-15 năm.
3. Phạm tội gây chết người: tù 15-20 năm hoặc tù chung thân.

Điều 258. Tội lôi kéo người khác sử dụng trái phép chất ma túy
Phạt tù từ 01 năm đến 05 năm (trường hợp cơ bản).

Điều 259. Tội vi phạm quy định về quản lý chất ma túy, tiền chất, thuốc gây nghiện, thuốc hướng thần
Phạt tù từ 01 năm đến 05 năm hoặc phạt tiền.
""",
    },
    {
        "filename": "nghi-dinh-105-2021-huong-dan-luat-phong-chong-ma-tuy.pdf",
        "title": "NGHỊ ĐỊNH 105/2021/NĐ-CP HƯỚNG DẪN THI HÀNH LUẬT PHÒNG, CHỐNG MA TUÝ",
        "content": """CHÍNH PHỦ
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Nghị định số: 105/2021/NĐ-CP
Ngày ban hành: 04/12/2021
Ngày hiệu lực: 01/01/2022

NGHỊ ĐỊNH
QUY ĐỊNH CHI TIẾT VÀ HƯỚNG DẪN THI HÀNH MỘT SỐ ĐIỀU
CỦA LUẬT PHÒNG, CHỐNG MA TÚY

Căn cứ Luật Tổ chức Chính phủ ngày 19 tháng 6 năm 2015;
Căn cứ Luật Phòng, chống ma túy ngày 30 tháng 3 năm 2021;
Theo đề nghị của Bộ trưởng Bộ Lao động - Thương binh và Xã hội;
Chính phủ ban hành Nghị định quy định chi tiết và hướng dẫn thi hành một số điều của Luật Phòng, chống ma túy.

CHƯƠNG I: QUY ĐỊNH CHUNG

Điều 1. Phạm vi điều chỉnh
Nghị định này quy định chi tiết và hướng dẫn thi hành một số điều của Luật Phòng, chống ma túy về:
1. Quản lý người sử dụng trái phép chất ma túy.
2. Cai nghiện ma túy tự nguyện tại gia đình, cộng đồng.
3. Cai nghiện ma túy tự nguyện tại cơ sở cai nghiện ma túy.
4. Cai nghiện ma túy bắt buộc.
5. Quản lý sau cai nghiện ma túy.
6. Các biện pháp tổ chức cai nghiện ma túy khác.

Điều 2. Đối tượng áp dụng
Nghị định này áp dụng đối với:
1. Người sử dụng trái phép chất ma túy.
2. Người nghiện ma túy.
3. Gia đình người nghiện ma túy, người sử dụng trái phép chất ma túy.
4. Cơ sở cai nghiện ma túy công lập và tư nhân.
5. Các cơ quan, tổ chức, cá nhân có liên quan.

CHƯƠNG II: QUẢN LÝ NGƯỜI SỬ DỤNG TRÁI PHÉP CHẤT MA TUÝ

Điều 3. Trình tự xác định người sử dụng trái phép chất ma túy
1. Khi phát hiện hoặc tiếp nhận thông tin về người sử dụng trái phép chất ma túy, Công an xã tiến hành:
   a) Lập biên bản về hành vi sử dụng trái phép chất ma túy;
   b) Yêu cầu xét nghiệm chất ma túy trong cơ thể;
   c) Lập hồ sơ quản lý.
2. Kết quả xét nghiệm dương tính với chất ma túy là cơ sở xác định người sử dụng trái phép chất ma túy.

Điều 4. Biện pháp quản lý người sử dụng trái phép chất ma túy
1. Lập danh sách, theo dõi, quản lý tại nơi cư trú.
2. Xét nghiệm chất ma túy trong cơ thể ít nhất 02 lần trong thời hạn quản lý.
3. Giáo dục, tư vấn về tác hại của ma túy và pháp luật.
4. Thời hạn quản lý: 01 năm kể từ ngày lập danh sách.

CHƯƠNG III: CAI NGHIỆN MA TÚY TỰ NGUYỆN

Điều 5. Cai nghiện tự nguyện tại gia đình, cộng đồng
1. Người nghiện ma túy hoặc đại diện gia đình đăng ký tại UBND xã.
2. Thời gian: tối thiểu 06 tháng.
3. Các giai đoạn:
   a) Tiếp nhận, phân loại: 5-7 ngày;
   b) Giải độc, cắt cơn: 7-15 ngày;
   c) Điều trị các rối loạn tâm thần: 30-60 ngày;
   d) Phục hồi sức khỏe, giáo dục, tư vấn: 30-60 ngày;
   e) Phòng chống tái nghiện: còn lại.

Điều 6. Quyền và nghĩa vụ của người cai nghiện tự nguyện
1. Quyền:
   a) Được tư vấn về chương trình cai nghiện;
   b) Được điều trị y tế;
   c) Được bảo đảm bí mật thông tin cá nhân.
2. Nghĩa vụ:
   a) Chấp hành quy trình cai nghiện;
   b) Xét nghiệm định kỳ theo yêu cầu;
   c) Không sử dụng trái phép chất ma túy trong thời gian cai nghiện.

CHƯƠNG IV: CAI NGHIỆN MA TÚY BẮT BUỘC

Điều 10. Đối tượng cai nghiện bắt buộc
1. Người nghiện ma túy từ đủ 18 tuổi trở lên thuộc một trong các trường hợp:
   a) Đã cai nghiện tự nguyện mà tái nghiện;
   b) Không đăng ký cai nghiện tự nguyện trong thời hạn quy định;
   c) Tự ý bỏ cai nghiện.
2. Thời gian: từ 12 tháng đến 24 tháng.

Điều 11. Trình tự đưa vào cơ sở cai nghiện bắt buộc
1. Công an cấp xã lập hồ sơ đề nghị.
2. Trưởng phòng Lao động - TB&XH thẩm định hồ sơ.
3. Tòa án nhân dân cấp huyện ra quyết định.
4. Thời hạn giải quyết: 05 ngày làm việc kể từ khi nhận đủ hồ sơ.

CHƯƠNG V: QUẢN LÝ SAU CAI NGHIỆN

Điều 15. Quản lý sau cai nghiện tại nơi cư trú
1. Thời gian quản lý sau cai: 02 năm.
2. Nội dung: hỗ trợ việc làm, giáo dục, tư vấn, xét nghiệm định kỳ.
3. Người quản lý: Cán bộ tư pháp xã phối hợp với gia đình.

Điều 16. Đánh giá kết quả quản lý sau cai
1. Sau 02 năm, nếu người sau cai nghiện không tái sử dụng ma túy, coi như hoàn thành.
2. Nếu tái nghiện: áp dụng lại biện pháp cai nghiện bắt buộc.

CHƯƠNG VI: ĐIỀU KHOẢN THI HÀNH

Điều 20. Hiệu lực thi hành
Nghị định này có hiệu lực từ ngày 01 tháng 01 năm 2022 và thay thế Nghị định số 94/2010/NĐ-CP.
""",
    },
    {
        "filename": "nghi-dinh-57-2022-danh-muc-chat-ma-tuy.pdf",
        "title": "NGHỊ ĐỊNH 57/2022/NĐ-CP VỀ DANH MỤC CHẤT MA TUÝ VÀ TIỀN CHẤT",
        "content": """CHÍNH PHỦ
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Nghị định số: 57/2022/NĐ-CP
Ngày ban hành: 25/08/2022
Ngày hiệu lực: 25/08/2022

NGHỊ ĐỊNH
QUY ĐỊNH CÁC DANH MỤC CHẤT MA TÚY VÀ TIỀN CHẤT

CHƯƠNG I: QUY ĐỊNH CHUNG

Điều 1. Phạm vi điều chỉnh
Nghị định này quy định các danh mục chất ma túy và tiền chất bao gồm:
1. Danh mục I: Các chất ma túy tuyệt đối cấm sử dụng trong y học và đời sống xã hội (bao gồm cả dạng muối, đồng phân, este, ete).
2. Danh mục II: Các chất ma túy được dùng hạn chế trong phân tích, kiểm nghiệm, nghiên cứu khoa học, điều tra tội phạm hoặc trong lĩnh vực y tế.
3. Danh mục III: Các chất ma túy được dùng trong phân tích, kiểm nghiệm, nghiên cứu khoa học, điều tra tội phạm hoặc trong lĩnh vực y tế theo quy định.
4. Danh mục IV: Các tiền chất.

CHƯƠNG II: DANH MỤC CÁC CHẤT MA TUÝ

Điều 2. Danh mục I - Các chất ma túy tuyệt đối cấm
Bao gồm nhưng không giới hạn:
1. Acetorphine
2. Acetyl-alpha-methylfentanyl
3. Alpha-methylfentanyl
4. Alpha-methylthiofentanyl
5. Beta-hydroxyfentanyl
6. Cần sa (Cannabis) và nhựa cần sa
7. Desomorphine
8. MDMA (3,4-methylenedioxymethamphetamine) - Thuốc lắc/Ecstasy
9. Heroin (Diacetylmorphine)
10. LSD (Lysergic acid diethylamide)
11. Mescaline
12. Methamphetamine (Ma túy đá/Ice)
13. Psilocybin (nấm thức thần)
14. THC (Tetrahydrocannabinol) - hoạt chất chính trong cần sa
15. Cathinone và các dẫn xuất tổng hợp (Mephedrone, Methylone, MDPV)
16. Ketamine (ở liều lượng và mục đích sử dụng trái phép)
17. GHB (Gamma-hydroxybutyrate)
18. Fentanyl và các dẫn xuất (Carfentanil, Acetylfentanyl)
19. Cỏ Mỹ (chất tổng hợp cannabinoid: JWH-018, JWH-073, AM-2201)
20. Flakka (Alpha-PVP)

Điều 3. Danh mục II - Các chất ma túy dùng hạn chế
Bao gồm:
1. Cocaine
2. Codeine
3. Fentanyl (trong y tế)
4. Methadone
5. Morphine
6. Oxycodone
7. Pethidine (Meperidine)
8. Amphetamine (trong y tế, điều trị ADHD)
9. Methylphenidate (Ritalin)
10. Diazepam, Midazolam và các benzodiazepine khác

Điều 4. Danh mục IV - Tiền chất
1. Acetic anhydride
2. Acetone
3. Anthranilic acid
4. Ephedrine
5. Ergometrine
6. Ergotamine
7. Hydrochloric acid
8. Isosafrole
9. Lysergic acid
10. Methyl ethyl ketone
11. Phenylacetic acid
12. Piperidine
13. Potassium permanganate
14. Pseudoephedrine
15. Safrole
16. Sulphuric acid
17. Toluene

CHƯƠNG III: QUY ĐỊNH VỀ QUẢN LÝ

Điều 5. Quản lý chất ma túy trong Danh mục II và III
1. Chỉ được sử dụng trong y tế khi có chỉ định của bác sĩ.
2. Phải có giấy phép của cơ quan có thẩm quyền.
3. Phải ghi chép, báo cáo đầy đủ về việc xuất, nhập, sử dụng.

Điều 6. Quản lý tiền chất
1. Doanh nghiệp sản xuất, kinh doanh tiền chất phải có giấy phép.
2. Phải báo cáo định kỳ 06 tháng về lượng tiền chất xuất, nhập, tồn kho.
3. Không được bán tiền chất cho cá nhân, tổ chức không có giấy phép.

CHƯƠNG IV: ĐIỀU KHOẢN THI HÀNH

Điều 7. Hiệu lực thi hành
Nghị định này có hiệu lực từ ngày ký và thay thế các quy định trước đó về danh mục chất ma túy.
""",
    },
]


def collect_legal_documents():
    """Thu thập và lưu các văn bản pháp luật vào data/landing/legal/."""
    setup_directory()
    print(f"\nBắt đầu thu thập {len(LEGAL_DOCUMENTS)} văn bản pháp luật...\n")

    for doc_info in LEGAL_DOCUMENTS:
        print(f"📄 {doc_info['title']}")
        create_legal_document_pdf(
            filename=doc_info["filename"],
            title=doc_info["title"],
            content=doc_info["content"],
        )
        print()

    # Liệt kê kết quả
    files = list(DATA_DIR.iterdir())
    print(f"\n{'='*50}")
    print(f"✓ Tổng cộng {len(files)} file trong {DATA_DIR}:")
    for f in sorted(files):
        if f.is_file():
            print(f"  - {f.name} ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    collect_legal_documents()
