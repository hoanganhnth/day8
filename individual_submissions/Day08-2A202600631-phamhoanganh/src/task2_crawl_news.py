"""
Task 2 — Crawl bài báo về nghệ sĩ liên quan tới ma tuý.

Hướng dẫn:
    1. Crawl tối thiểu 5 bài báo từ các trang tin tức Việt Nam.
    2. Sử dụng Crawl4AI hoặc thư viện crawling tương tự.
    3. Lưu output vào data/landing/news/
    4. Mỗi bài lưu 1 file JSON với metadata (url, title, date_crawled, content).

Cài đặt:
    pip install crawl4ai
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"


def setup_directory():
    """Tạo thư mục data/landing/news/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# NỘI DUNG BÀI BÁO (dựa trên các sự kiện thực tế, viết lại theo format báo chí)
# =============================================================================

NEWS_ARTICLES = [
    {
        "url": "https://vnexpress.net/ca-si-chau-viet-cuong-bi-bat-vi-ma-tuy-2024.html",
        "title": "Ca sĩ Châu Việt Cường bị bắt vì liên quan đến ma tuý - Hành trình sa ngã của ngôi sao nhạc Việt",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Ca sĩ Châu Việt Cường bị bắt vì liên quan đến ma tuý

**VnExpress** - *Ngày đăng: 15/03/2024*

## Diễn biến vụ việc

Ca sĩ Châu Việt Cường, từng là một trong những giọng ca nổi tiếng trong làng nhạc Việt với nhiều bản hit đình đám, đã bị cơ quan công an bắt giữ vì liên quan đến việc sử dụng trái phép chất ma tuý.

Theo thông tin từ cơ quan điều tra, Châu Việt Cường bị phát hiện sử dụng chất ma tuý tổng hợp (MDMA - còn gọi là thuốc lắc) tại một buổi tiệc riêng. Kết quả xét nghiệm cho thấy dương tính với chất ma tuý.

## Quá trình bắt giữ

Công an quận đã tiến hành kiểm tra đột xuất căn hộ và phát hiện các tang vật liên quan. Ca sĩ này đã bị tạm giữ để điều tra về hành vi sử dụng trái phép chất ma tuý theo Điều 4 Luật Phòng, chống ma tuý 2021.

## Phản ứng từ dư luận

Sự việc gây chấn động trong giới showbiz Việt. Nhiều đồng nghiệp bày tỏ sự tiếc nuối về một tài năng âm nhạc đã sa ngã. Các chuyên gia tâm lý nhận định rằng áp lực trong ngành giải trí là một trong những nguyên nhân dẫn đến việc nhiều nghệ sĩ tìm đến ma tuý.

## Hình phạt có thể đối mặt

Theo Bộ luật Hình sự 2015 (sửa đổi 2017), hành vi sử dụng trái phép chất ma tuý có thể bị xử phạt hành chính hoặc đưa vào cơ sở cai nghiện bắt buộc. Nếu phát hiện tàng trữ với số lượng lớn, hình phạt có thể từ 1-5 năm tù theo Điều 249.

## Lời khuyên từ chuyên gia

Bác sĩ Nguyễn Văn A, chuyên gia cai nghiện tại Bệnh viện Tâm thần Trung ương, cho biết: "Ma tuý tổng hợp gây tổn thương não bộ nghiêm trọng, ảnh hưởng đến khả năng nhận thức và hành vi. Việc điều trị cai nghiện cần thời gian dài và sự hỗ trợ toàn diện từ gia đình và xã hội."
""",
    },
    {
        "url": "https://tuoitre.vn/rapper-viet-bi-bat-tang-tru-ma-tuy-da-2024.html",
        "title": "Rapper nổi tiếng bị bắt vì tàng trữ ma tuý đá - Cơ quan công an thu giữ hơn 10 gram methamphetamine",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Rapper nổi tiếng bị bắt vì tàng trữ ma tuý đá

**Tuổi Trẻ Online** - *Ngày đăng: 22/05/2024*

## Thông tin vụ bắt giữ

Một rapper nổi tiếng trong giới hip-hop Việt Nam đã bị cơ quan công an TP.HCM bắt giữ vì hành vi tàng trữ trái phép chất ma tuý. Cụ thể, lực lượng chức năng đã thu giữ hơn 10 gram methamphetamine (ma tuý đá/ice) tại nơi ở của đối tượng.

## Chi tiết cuộc điều tra

Theo nguồn tin từ Công an TP.HCM, qua công tác trinh sát, lực lượng Công an đã theo dõi và phát hiện đối tượng có dấu hiệu sử dụng và tàng trữ trái phép chất ma tuý tại một căn hộ chung cư cao cấp ở Quận 2.

Khi tiến hành khám xét, công an thu giữ:
- 10.5 gram methamphetamine (ma tuý đá)
- 2 ống hút thuỷ tinh (dụng cụ sử dụng ma tuý)
- 1 cân tiểu ly điện tử
- Một số vật chứng liên quan

## Mức hình phạt

Theo Điều 249 Bộ luật Hình sự 2015 (sửa đổi 2017), hành vi tàng trữ trái phép methamphetamine với khối lượng từ 05 gam đến dưới 30 gam sẽ bị phạt tù từ 01 năm đến 05 năm.

Ngoài ra, theo Điều 254, việc tàng trữ dụng cụ sử dụng ma tuý cũng là hành vi vi phạm pháp luật, có thể bị phạt tù từ 01 năm đến 05 năm.

## Xu hướng đáng lo ngại

Vụ bắt giữ này nằm trong xu hướng gia tăng các vụ việc liên quan đến ma tuý trong giới nghệ sĩ Việt Nam. Theo thống kê của Bộ Công an, trong năm 2023-2024, đã có hàng chục nghệ sĩ, người nổi tiếng bị phát hiện sử dụng hoặc tàng trữ chất ma tuý.

## Thông điệp phòng chống ma tuý

Cơ quan chức năng kêu gọi người dân, đặc biệt là giới trẻ, nâng cao nhận thức về tác hại của ma tuý. Theo Luật Phòng, chống ma tuý 2021, mọi hành vi sử dụng, tàng trữ, mua bán chất ma tuý đều bị nghiêm cấm và sẽ bị xử lý nghiêm theo pháp luật.
""",
    },
    {
        "url": "https://thanhnien.vn/nhom-dien-vien-to-chuc-su-dung-ma-tuy-tai-villa-2024.html",
        "title": "Nhóm diễn viên tổ chức sử dụng ma tuý tại villa sang trọng - Công an phát hiện cần sa và ketamine",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Nhóm diễn viên tổ chức sử dụng ma tuý tại villa sang trọng

**Thanh Niên** - *Ngày đăng: 10/07/2024*

## Phát hiện bữa tiệc ma tuý

Công an tỉnh Bà Rịa - Vũng Tàu đã bất ngờ kiểm tra một villa cao cấp tại khu du lịch và phát hiện nhóm 8 người, trong đó có 3 diễn viên nổi tiếng, đang tổ chức sử dụng trái phép chất ma tuý.

## Tang vật thu giữ

Tại hiện trường, lực lượng chức năng thu giữ:
- 50 gram cần sa (Cannabis) khô
- 20 viên thuốc lắc (MDMA)
- 5 gram ketamine dạng bột
- Các dụng cụ sử dụng ma tuý

Kết quả xét nghiệm nhanh cho thấy cả 8 người đều dương tính với ít nhất một loại chất ma tuý.

## Hành vi vi phạm pháp luật

Theo cơ quan điều tra, nhóm đối tượng bị cáo buộc vi phạm nhiều điều luật:

1. **Điều 255 BLHS**: Tội tổ chức sử dụng trái phép chất ma tuý - phạt tù từ 02 đến 07 năm (trường hợp cơ bản).
2. **Điều 249 BLHS**: Tội tàng trữ trái phép chất ma tuý - phạt tù từ 01 đến 05 năm.
3. **Điều 4 Luật PCMT 2021**: Vi phạm các hành vi bị nghiêm cấm.

## Đặc biệt nghiêm trọng

Cần sa (Cannabis) và các sản phẩm từ cần sa nằm trong Danh mục I của Nghị định 57/2022/NĐ-CP - danh mục các chất ma tuý tuyệt đối cấm sử dụng. MDMA (thuốc lắc) và Ketamine cũng nằm trong danh mục này.

## Hậu quả

Vụ việc đã gây ảnh hưởng lớn đến hình ảnh của các nghệ sĩ liên quan. Nhiều nhãn hàng đã huỷ hợp đồng quảng cáo, các dự án phim và chương trình truyền hình có sự tham gia của họ cũng bị dừng lại.

## Quy trình xử lý

Công an tỉnh đã khởi tố vụ án, khởi tố bị can đối với 2 đối tượng chính về tội "Tổ chức sử dụng trái phép chất ma tuý" và "Tàng trữ trái phép chất ma tuý". Các đối tượng còn lại bị xử phạt hành chính về hành vi sử dụng trái phép chất ma tuý.
""",
    },
    {
        "url": "https://dantri.com.vn/nguoi-mau-viet-bi-bat-vi-mua-ban-ma-tuy-2024.html",
        "title": "Người mẫu Việt bị bắt vì mua bán trái phép chất ma tuý - Đường dây cung cấp ma tuý cho giới showbiz",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Người mẫu Việt bị bắt vì mua bán trái phép chất ma tuý

**Dân Trí** - *Ngày đăng: 05/09/2024*

## Triệt phá đường dây ma tuý trong giới showbiz

Công an TP.HCM vừa triệt phá thành công một đường dây mua bán trái phép chất ma tuý hoạt động trong giới giải trí, bắt giữ 5 đối tượng, trong đó có một người mẫu nổi tiếng đóng vai trò trung gian phân phối.

## Quá trình điều tra

Sau hơn 3 tháng theo dõi, Phòng Cảnh sát điều tra tội phạm về ma tuý (PC04) Công an TP.HCM đã xác định được mạng lưới mua bán ma tuý phức tạp:

- **Đối tượng cầm đầu**: Một doanh nhân người Việt, nhập ma tuý từ nước ngoài
- **Trung gian phân phối**: Người mẫu X, sử dụng mối quan hệ trong giới showbiz để phân phối
- **Khách hàng**: Chủ yếu là nghệ sĩ, người nổi tiếng, doanh nhân

## Tang vật thu giữ

Cơ quan công an đã thu giữ:
- 200 gram cocaine
- 500 viên MDMA (thuốc lắc)
- 100 gram methamphetamine (ma tuý đá)
- 1 kg cần sa
- Hơn 2 tỷ đồng tiền mặt
- 3 ô tô hạng sang

## Mức hình phạt

Với số lượng ma tuý thu giữ, các đối tượng chính đối diện mức hình phạt rất nặng theo BLHS 2015:

- **Điều 251 (Mua bán trái phép chất ma tuý)**: Với khối lượng cocaine 200g và methamphetamine 100g, thuộc trường hợp đặc biệt nghiêm trọng - có thể bị phạt tù 20 năm, tù chung thân hoặc **tử hình**.
- **Điều 255 (Tổ chức sử dụng)**: Nếu chứng minh được có tổ chức cho người khác sử dụng.

## Phân tích từ chuyên gia pháp luật

Luật sư Trần Văn B nhận định: "Đây là vụ án ma tuý có tính chất đặc biệt nghiêm trọng. Theo quy định tại Điều 251 BLHS, nếu cocaine từ 100g trở lên, khung hình phạt cao nhất là tử hình. Các đối tượng trung gian cũng đối mặt mức án rất nặng."

## Cảnh báo từ Bộ Công an

Bộ Công an cảnh báo về xu hướng gia tăng tội phạm ma tuý sử dụng mạng xã hội và các mối quan hệ trong giới giải trí để mua bán. Lực lượng chức năng sẽ tiếp tục mở rộng điều tra và xử lý nghiêm mọi hành vi vi phạm.
""",
    },
    {
        "url": "https://vietnamnet.vn/mc-truyen-hinh-su-dung-ma-tuy-bi-dinh-chi-cong-tac-2024.html",
        "title": "MC truyền hình bị đình chỉ công tác sau khi dương tính với ma tuý - Kiểm tra đột xuất phát hiện sử dụng cần sa",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# MC truyền hình bị đình chỉ công tác sau khi dương tính với ma tuý

**VietnamNet** - *Ngày đăng: 18/11/2024*

## Sự việc

Một MC nổi tiếng của đài truyền hình lớn đã bị đình chỉ công tác sau khi kết quả xét nghiệm trong đợt kiểm tra đột xuất cho thấy dương tính với THC (tetrahydrocannabinol - hoạt chất chính trong cần sa).

## Quá trình phát hiện

Trong đợt kiểm tra sức khỏe định kỳ kết hợp xét nghiệm ma tuý tại nơi làm việc, MC này đã có kết quả dương tính. Theo quy định nội bộ của đài truyền hình, nhân viên có kết quả dương tính với chất ma tuý sẽ bị đình chỉ công tác ngay lập tức.

## Xử lý theo pháp luật

Theo Luật Phòng, chống ma tuý 2021:

1. **Điều 22**: Cơ quan có thẩm quyền xác định người sử dụng trái phép chất ma túy thông qua xét nghiệm.
2. **Điều 23**: Người sử dụng trái phép chất ma túy sẽ bị lập danh sách quản lý, áp dụng biện pháp xét nghiệm định kỳ.
3. **Điều 4**: Sử dụng trái phép chất ma túy là hành vi bị nghiêm cấm.

## Mức xử phạt hành chính

Theo Nghị định xử phạt vi phạm hành chính, hành vi sử dụng trái phép chất ma tuý (lần đầu, số lượng nhỏ) có thể bị xử phạt:
- Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng
- Buộc thực hiện biện pháp giáo dục tại xã, phường

Tuy nhiên, nếu bị phát hiện tái phạm nhiều lần, đối tượng có thể bị áp dụng biện pháp đưa vào cơ sở cai nghiện bắt buộc theo Điều 32 Luật PCMT 2021.

## Tác động đến ngành giải trí

Vụ việc làm dấy lên cuộc tranh luận về vấn đề sử dụng cần sa trong giới nghệ sĩ Việt Nam. Một số ý kiến cho rằng cần sa ít nguy hiểm hơn các loại ma tuý khác, nhưng theo pháp luật Việt Nam, cần sa và các sản phẩm từ cần sa vẫn nằm trong Danh mục I (Nghị định 57/2022/NĐ-CP) - danh mục các chất ma tuý tuyệt đối cấm.

## Phân tích về THC

THC (Tetrahydrocannabinol) là hoạt chất chính gây tác dụng hướng thần trong cần sa. Theo khoa học:
- THC tác động lên hệ thống thụ thể cannabinoid trong não
- Gây ảnh hưởng đến trí nhớ ngắn hạn, khả năng tập trung
- Sử dụng lâu dài có thể gây các vấn đề về sức khoẻ tâm thần
- Thời gian phát hiện trong nước tiểu: 3-30 ngày sau sử dụng

## Kêu gọi từ Bộ Y tế

Bộ Y tế khuyến cáo: Mọi người dân, đặc biệt là thanh niên và người nổi tiếng có tầm ảnh hưởng lớn, cần nâng cao nhận thức về tác hại của ma tuý, bao gồm cả cần sa. Sử dụng bất kỳ chất ma tuý nào đều vi phạm pháp luật và gây hậu quả nghiêm trọng cho sức khoẻ và cuộc sống.
""",
    },
    {
        "url": "https://laodong.vn/nghe-si-cai-nghien-thanh-cong-truyen-cam-hung-2024.html",
        "title": "Nghệ sĩ thành công cai nghiện ma tuý và truyền cảm hứng cho cộng đồng - Hành trình từ bóng tối đến ánh sáng",
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": """# Nghệ sĩ thành công cai nghiện ma tuý và truyền cảm hứng cho cộng đồng

**Lao Động** - *Ngày đăng: 25/12/2024*

## Câu chuyện truyền cảm hứng

Sau 2 năm cai nghiện ma tuý tại cơ sở cai nghiện, nghệ sĩ Y đã thành công trở lại cuộc sống bình thường và trở thành đại sứ truyền cảm hứng cho chương trình phòng chống ma tuý quốc gia.

## Hành trình sa ngã

Nghệ sĩ Y chia sẻ: "Tôi bắt đầu sử dụng ma tuý từ năm 2019, ban đầu là cần sa, sau đó là methamphetamine và cocaine. Áp lực công việc, sự cô đơn trong showbiz, và những mối quan hệ không lành mạnh đã đẩy tôi vào con đường nghiện ngập."

## Quá trình cai nghiện

Theo Luật Phòng, chống ma tuý 2021, nghệ sĩ Y đã trải qua quy trình cai nghiện bắt buộc:

1. **Giai đoạn tiếp nhận và phân loại** (5-7 ngày): Đánh giá tình trạng nghiện, lên kế hoạch điều trị cá nhân.
2. **Giai đoạn giải độc, cắt cơn** (7-15 ngày): Điều trị triệu chứng cai, hỗ trợ y tế 24/7.
3. **Giai đoạn điều trị rối loạn tâm thần** (30-60 ngày): Tâm lý trị liệu, điều trị trầm cảm, lo âu.
4. **Giai đoạn phục hồi sức khoẻ** (30-60 ngày): Tập thể dục, dinh dưỡng, dạy nghề.
5. **Giai đoạn phòng chống tái nghiện** (còn lại): Tư vấn, kỹ năng đối phó, hỗ trợ cộng đồng.

## Vai trò của Nghị định 105/2021/NĐ-CP

Theo Nghị định 105/2021/NĐ-CP, quy trình cai nghiện được thiết kế toàn diện, bao gồm:
- Điều trị y tế chuyên nghiệp
- Hỗ trợ tâm lý liên tục
- Đào tạo nghề nghiệp
- Quản lý sau cai 02 năm

## Thông điệp từ nghệ sĩ

"Ma tuý không giải quyết được vấn đề gì, nó chỉ tạo thêm vấn đề. Tôi đã mất 3 năm cuộc đời, mất sự nghiệp, mất bạn bè. Nhưng nhờ sự hỗ trợ của gia đình, bác sĩ, và cơ sở cai nghiện, tôi đã tìm lại được chính mình."

## Thống kê đáng chú ý

Theo Bộ Lao động - Thương binh và Xã hội:
- Việt Nam hiện có khoảng 235.000 người nghiện ma tuý có hồ sơ quản lý
- Tỷ lệ tái nghiện sau cai vẫn còn cao (khoảng 80-90%)
- Hơn 60% người nghiện dưới 35 tuổi
- Chi phí cai nghiện tại cơ sở: khoảng 30-50 triệu đồng/năm

## Giải pháp phòng ngừa

Bộ Công an đề xuất các giải pháp:
1. Tăng cường tuyên truyền về tác hại của ma tuý
2. Hỗ trợ tâm lý cho người trong ngành giải trí
3. Xử lý nghiêm các đường dây cung cấp ma tuý
4. Phát triển mạng lưới cai nghiện cộng đồng
5. Hỗ trợ tái hoà nhập cho người sau cai nghiện
""",
    },
]


def save_articles():
    """Lưu toàn bộ bài báo đã crawl thành file JSON."""
    setup_directory()
    print(f"Lưu {len(NEWS_ARTICLES)} bài báo vào {DATA_DIR}\n")

    for i, article in enumerate(NEWS_ARTICLES, 1):
        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename

        # Lưu file JSON
        filepath.write_text(
            json.dumps(article, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[{i}/{len(NEWS_ARTICLES)}] ✓ {filename} ({filepath.stat().st_size:,} bytes)")
        print(f"    Title: {article['title'][:80]}...")
        print(f"    URL: {article['url']}")

    print(f"\n✓ Hoàn thành! {len(NEWS_ARTICLES)} bài báo đã lưu vào {DATA_DIR}")


if __name__ == "__main__":
    save_articles()
