
#TEST 3
# import os
# from datetime import datetime
# import requests

# # ==============================================================================
# # BÀN ĐIỀU KHIỂN CẤU HÌNH DATABASE (BẤM CHỌN CỔNG XUẤT DỮ LIỆU)
# # Lựa chọn bao gồm: "Discord", "Telegram", "LocalFile", hoặc "None"
# # ==============================================================================
# DATABASE_BACKEND = "LocalFile"

# # --- [1] CẤU HÌNH DISCORD ---
# DISCORD_WEBHOOK_URL = "DÁN_LINK_WEBHOOK_DISCORD_CỦA_ÔNG_VÀO_ĐÂY"

# # --- [2] CẤU HÌNH TELEGRAM ---
# TELEGRAM_BOT_TOKEN = "DÁN_TOKEN_BOT_TELEGRAM_CỦA_ÔNG_VÀO_ĐÂY"
# TELEGRAM_CHAT_ID = "DÁN_CHAT_ID_BOX_CỦA_ÔNG_VÀO_ĐÂY"

# # --- [3] CẤU HÌNH LOCAL FILE ---
# LOCAL_DATABASE_PATH = "history_database.md"


# def route_to_discord(original, translated):
#     """Phân hệ gửi dữ liệu lên Server Discord dưới dạng khung Embed đồ họa cao cấp.
#     Đã tối ưu hóa khối code block ```text để hiển thị xuống hàng tự nhiên 100%.
#     """
#     if not DISCORD_WEBHOOK_URL or "DÁN_LINK_WEBHOOK" in DISCORD_WEBHOOK_URL:
#         return
        
#     payload = {
#         "embeds": [
#             {
#                 "title": "🔄 AUTOMATED CLOUD DATABASE SYNCHRONIZED",
#                 "color": 3066993,  # Mã màu xanh lục bảo (Emerald Green) chuyên nghiệp
#                 "fields": [
#                     {
#                         "name": "🔴 NỘI DUNG GỐC ĐỌC ĐƯỢC:",
#                         "value": f"```text\n{original}\n```",
#                         "inline": False,
#                     },
#                     {
#                         "name": "🟢 BẢN DỊCH HỆ THỐNG NGUYÊN KHỐI:",
#                         "value": f"```text\n{translated}\n```",  # Đã tối ưu về hệ text thuần chuẩn
#                         "inline": False,
#                     },
#                 ],
#                 "footer": {
#                     "text": f"Manga Live Translator Engine • Logged at {datetime.now().strftime('%H:%M:%S')}"
#                 },
#             }
#         ]
#     }
#     try:
#         # Cài đặt timeout để tránh làm đứng hình tiến trình live mss nếu mạng lag
#         requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=2.0)
#     except Exception as e:
#         print(f"\n[DATABASE ERROR] Thất bại khi ghi dữ liệu vào Discord Cloud: {str(e)}")


# def route_to_telegram(original, translated):
#     """Phân hệ gửi dữ liệu lên Cloud Telegram siêu tốc.
#     Sử dụng định dạng HTML Rich Text và thẻ <code> để giữ nguyên định dạng xuống hàng.
#     """
#     if not TELEGRAM_BOT_TOKEN or "DÁN_TOKEN_BOT" in TELEGRAM_BOT_TOKEN:
#         return
        
#     # Chuỗi HTML định dạng chữ in đậm và khối code monospaced nguyên khối
#     message_html = (
#         f"<b>📥 DATABASE LIVE LOG RECORD</b>\n"
#         f"<i>Thời gian: {datetime.now().strftime('%H:%M:%S')}</i>\n\n"
#         f"🔴 <b>ORIGINAL TEXT:</b>\n<code>{original}</code>\n\n"
#         f"🟢 <b>TRANSLATED TEXT:</b>\n<code>{translated}</code>\n"
#         f"────────────────────"
#     )
    
#     # ĐÃ FIX: Sửa lại đường dẫn API URL chuẩn của Telegram (loại bỏ hyperlink Markdown lỗi)
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
#     payload = {
#         "chat_id": TELEGRAM_CHAT_ID,
#         "text": message_html,
#         "parse_mode": "HTML",
#     }
#     try:
#         requests.post(url, json=payload, timeout=2.0)
#     except Exception as e:
#         print(f"\n[DATABASE ERROR] Thất bại khi ghi dữ liệu vào Telegram Cloud: {str(e)}")


# def route_to_local_file(original, translated):
#     """Phân hệ ghi log ngoại tuyến trực tiếp vào ổ cứng máy tính dạng Markdown.
#     Bảo toàn cấu trúc xuống dòng nguyên khối y chang màn hình Terminal.
#     """
#     try:
#         # Tự khởi tạo tiêu đề file nếu chưa tồn tại
#         if not os.path.exists(LOCAL_DATABASE_PATH):
#             with open(LOCAL_DATABASE_PATH, "w", encoding="utf-8") as f:
#                 f.write("# 📚 LOCAL TRANSLATION AUDIT LOG DATABASE\n")
#                 f.write(
#                     f"Khởi tạo hệ thống vào lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
#                 )
#                 f.write(
#                     "================================================================\n\n"
#                 )

#         current_time = datetime.now().strftime("%H:%M:%S")

#         # Ghi trực tiếp theo khối văn bản tự nhiên, bọc trong khối code block (```text) của Markdown
#         with open(LOCAL_DATABASE_PATH, "a", encoding="utf-8") as f:
#             f.write(
#                 f"## ⏱️ HỆ THỐNG GHI LOG LÚC: [{current_time}]\n\n"
#             )
#             f.write("### 🔴 NỘI DUNG GỐC TRÊN MÀN HÌNH:\n")
#             f.write(f"```text\n{original}\n```\n\n")
#             f.write("### 🟢 NỘI DUNG DỊCH HỆ THỐNG:\n")
#             f.write(f"```text\n{translated}\n```\n")
#             f.write(
#                 "\n----------------------------------------------------------------\n\n"
#             )

#     except Exception as e:
#         print(f"\n[DATABASE ERROR] Lỗi ghi file Local: {str(e)}")


# def central_database_router(original, translated):
#     """Hàm tổng đài phân phối luồng dữ liệu dựa vào cấu hình người dùng."""
#     if DATABASE_BACKEND == "Discord":
#         route_to_discord(original, translated)
#     elif DATABASE_BACKEND == "Telegram":
#         route_to_telegram(original, translated)
#     elif DATABASE_BACKEND == "LocalFile":
#         route_to_local_file(original, translated)
#     else:
#         pass





#TEST 5
import os
from datetime import datetime
import requests

# ==============================================================================
# BÀN ĐIỀU KHIỂN CẤU HÌNH DATABASE (BẤM CHỌN CỔNG XUẤT DỮ LIỆU)
# Lựa chọn bao gồm: "LocalFile", "Discord", "Telegram", hoặc "None"
# ==============================================================================
DATABASE_BACKEND = "LocalFile"

# --- [1] CẤU HÌNH KẾT NỐI DISCORD CLOUD ---
DISCORD_WEBHOOK_URL = "DÁN_LINK_WEBHOOK_DISCORD_CỦA_ÔNG_VÀO_ĐÂY"

# --- [2] CẤU HÌNH KẾT NỐI TELEGRAM CLOUD ---
TELEGRAM_BOT_TOKEN = "DÁN_TOKEN_BOT_TELEGRAM_CỦA_ÔNG_VÀO_ĐÂY"
TELEGRAM_CHAT_ID = "DÁN_CHAT_ID_BOX_CỦA_ÔNG_VÀO_ĐÂY"

# --- [3] CẤU HÌNH KHO LƯU TRỮ LOCAL FILE (LƯU TRỮ OFFLINE) ---
LOCAL_DATABASE_PATH = "history_database.md"


def route_to_discord(original, translated):
    """Phân hệ gửi dữ liệu lên Server Discord dưới dạng khung Embed đồ họa cao cấp.
    Bảo toàn cấu trúc xuống dòng tự nhiên 100% trong khối code block.
    """
    if not DISCORD_WEBHOOK_URL or "DÁN_LINK_WEBHOOK" in DISCORD_WEBHOOK_URL:
        return
        
    payload = {
        "embeds": [
            {
                "title": "🔄 AUTOMATED CLOUD DATABASE SYNCHRONIZED",
                "color": 3066993,  # Mã màu xanh lục bảo (Emerald Green) chuyên nghiệp
                "fields": [
                    {
                        "name": "🔴 NỘI DUNG GỐC ĐỌC ĐƯỢC:",
                        "value": f"```text\n{original}\n```",
                        "inline": False,
                    },
                    {
                        "name": "🟢 BẢN DỊCH HỆ THỐNG NGUYÊN KHỐI:",
                        "value": f"```text\n{translated}\n```",
                        "inline": False,
                    },
                ],
                "footer": {
                    "text": f"Manga Live Translator Engine • Logged at {datetime.now().strftime('%H:%M:%S')}"
                },
            }
        ]
    }
    try:
        # Giới hạn timeout 2.0 giây để tránh nghẽn luồng live capture nếu mạng lag
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=2.0)
    except Exception as e:
        print(f"\n[DATABASE ERROR] Thất bại khi ghi dữ liệu vào Discord Cloud: {str(e)}")


def route_to_telegram(original, translated):
    """Phân hệ gửi dữ liệu lên Cloud Telegram siêu tốc.
    Sử dụng định dạng HTML Rich Text và thẻ <code> để giữ nguyên định dạng phân dòng.
    """
    if not TELEGRAM_BOT_TOKEN or "DÁN_TOKEN_BOT" in TELEGRAM_BOT_TOKEN:
        return
        
    # Tạo cấu trúc tin nhắn HTML Monospaced chuyên nghiệp đổ về điện thoại
    message_html = (
        f"<b>📥 DATABASE LIVE LOG RECORD</b>\n"
        f"<i>Thời gian: {datetime.now().strftime('%H:%M:%S')}</i>\n\n"
        f"🔴 <b>ORIGINAL TEXT:</b>\n<code>{original}</code>\n\n"
        f"🟢 <b>TRANSLATED TEXT:</b>\n<code>{translated}</code>\n"
        f"────────────────────"
    )
    
    # URL thuần túy, sạch sẽ không dính bẫy ký tự lạ Markdown
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_html,
        "parse_mode": "HTML",
    }
    try:
        requests.post(url, json=payload, timeout=2.0)
    except Exception as e:
        print(f"\n[DATABASE ERROR] Thất bại khi ghi dữ liệu vào Telegram Cloud: {str(e)}")


def route_to_local_file(original, translated):
    """Phân hệ ghi log ngoại tuyến trực tiếp vào ổ cứng dạng Code Block Markdown.
    Khắc phục triệt để lỗi vỡ dòng của cấu hình bảng biểu cũ.
    """
    try:
        # Tự động dựng tiêu đề cấu trúc ban đầu nếu tệp tin chưa tồn tại trên ổ đĩa
        if not os.path.exists(LOCAL_DATABASE_PATH):
            with open(LOCAL_DATABASE_PATH, "w", encoding="utf-8") as f:
                f.write("# 📚 LOCAL TRANSLATION AUDIT LOG DATABASE\n")
                f.write(
                    f"Khởi tạo hệ thống vào lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                f.write(
                    "================================================================\n\n"
                )

        current_time = datetime.now().strftime("%H:%M:%S")

        # Tiến hành ghi nối đuôi (Append) khối văn bản tự nhiên vào file log (.md)
        with open(LOCAL_DATABASE_PATH, "a", encoding="utf-8") as f:
            f.write(f"## ⏱️ HỆ THỐNG GHI LOG LÚC: [{current_time}]\n\n")
            f.write("### 🔴 NỘI DUNG GỐC TRÊN MÀN HÌNH:\n")
            f.write(f"```text\n{original}\n```\n\n")
            f.write("### 🟢 NỘI DUNG DỊCH HỆ THỐNG:\n")
            f.write(f"```text\n{translated}\n```\n")
            f.write("\n----------------------------------------------------------------\n\n")

    except Exception as e:
        print(f"\n[DATABASE ERROR] Lỗi ghi file Local: {str(e)}")


def central_database_router(original, translated):
    """HÀM PHỄU TRUNG TÂM (DATABASE ROUTER FACTORY):
    Điều hướng dòng chảy dữ liệu dựa trên lựa chọn trực quan của người dùng từ GUI.
    """
    if DATABASE_BACKEND == "Discord":
        route_to_discord(original, translated)
    elif DATABASE_BACKEND == "Telegram":
        route_to_telegram(original, translated)
    elif DATABASE_BACKEND == "LocalFile":
        route_to_local_file(original, translated)
    else:
        # Nếu chọn "None", hệ thống tự hiểu chỉ hiển thị kết quả trên App, hoàn toàn chạy Offline ngầm
        pass
