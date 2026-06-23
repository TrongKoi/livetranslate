
#TEST 20
# import os
# import time
# import warnings
# import threading  # Thư viện đa luồng xử lý lag giao diện cực kỳ quan trọng
# import subprocess
# import sys
# import tkinter as tk
# from tkinter import ttk
# from tkinter import scrolledtext
# import cv2
# import easyocr
# import mss
# import numpy as np
# from deep_translator import GoogleTranslator

# # Gọi liên kết ngầm từ bộ thư viện lưu trữ đa kênh chúng ta đã hoàn thiện
# import storage
# from storage import central_database_router

# # Khóa toàn bộ các cảnh báo hệ thống không cần thiết từ thư viện bên thứ ba
# warnings.filterwarnings("ignore", category=UserWarning)  #


# class MangaLiveTranslatorGUI(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         # ==============================================================================
#         # CẤU HÌNH THUỘC TÍNH NỀN TẢNG CỦA CỬA SỔ
#         # ==============================================================================
#         self.title("Manga Live Translator Pro")  #
#         self.geometry("480x380")  # Kích thước tối ưu cho Menu ban đầu
        
#         # Cho phép người dùng tự do phóng to thu nhỏ cửa sổ lên tận 1920x1080
#         self.resizable(True, True)  #
        
#         # Áp dụng phong cách giao diện phẳng, hiện đại
#         self.style = ttk.Style()  #
#         self.style.theme_use("clam")  #

#         # Cấu hình danh mục ngôn ngữ đồng bộ với hệ thống OCR
#         self.supported_languages = {  #
#             "Tiếng Anh": {"ocr_code": ["en"], "trans_code": "en"},  #
#             "Tiếng Việt": {"ocr_code": ["vi"], "trans_code": "vi"},  #
#             "Tiếng Nhật": {"ocr_code": ["ja", "en"], "trans_code": "ja"},  #
#             "Tiếng Hàn": {"ocr_code": ["ko", "en"], "trans_code": "ko"},  #
#             "Tiếng Trung (Giản thể)": {"ocr_code": ["ch_sim", "en"], "trans_code": "zh-CN"},  #
#             "Tiếng Pháp": {"ocr_code": ["fr", "en"], "trans_code": "fr"},  #
#             "Tiếng Đức": {"ocr_code": ["de", "en"], "trans_code": "de"},  #
#         }  #

#         # Biến quản lý trạng thái và đa luồng ngầm
#         self.is_live_active = False  #
#         self.live_thread = None  # Biến lưu trữ tiến trình luồng dịch ngầm
#         self.last_raw_block = ""  # Bộ nhớ đệm chống trùng dữ liệu
#         self.monitor_coords = None # Lưu tọa độ vùng kéo chuột
#         self.reader = None  #
#         self.translator = None  #

#         # Khởi tạo toàn bộ các thành phần đồ họa của UI
#         self.create_widgets()  #

#     def create_widgets(self):  #
#         """Hàm dựng toàn bộ bố cục khung điều khiển của Menu Giao diện."""
#         # --- KHUNG CHỌN NGÔN NGỮ NGUỒN / ĐÍCH ---
#         lang_frame = ttk.LabelFrame(self, text=" Cấu Hình Ngôn Ngữ Dịch ", padding=10)  #
#         lang_frame.pack(fill="x", padx=15, pady=10)  #

#         ttk.Label(lang_frame, text="Ngôn ngữ gốc (Màn hình):").grid(row=0, column=0, sticky="w", pady=5)  #
#         self.cbo_source = ttk.Combobox(lang_frame, values=list(self.supported_languages.keys()), state="readonly", width=22)  #
#         self.cbo_source.grid(row=0, column=1, padx=10, pady=5)  #
#         self.cbo_source.set("Tiếng Anh")  #

#         ttk.Label(lang_frame, text="Ngôn ngữ đích (Bản dịch):").grid(row=1, column=0, sticky="w", pady=5)  #
#         self.cbo_target = ttk.Combobox(lang_frame, values=list(self.supported_languages.keys()), state="readonly", width=22)  #
#         self.cbo_target.grid(row=1, column=1, padx=10, pady=5)  #
#         self.cbo_target.set("Tiếng Việt")  #

#         # --- KHUNG CẤU HÌNH CƠ SỞ DỮ LIỆU ---
#         db_frame = ttk.LabelFrame(self, text=" Cấu Hình Kho Lưu Trữ (Database Backend) ", padding=10)  #
#         db_frame.pack(fill="x", padx=15, pady=5)  #

#         ttk.Label(db_frame, text="Chọn cổng Database:").grid(row=0, column=0, sticky="w", pady=5)  #
#         self.cbo_database = ttk.Combobox(db_frame, values=["LocalFile", "Discord", "Telegram", "None"], state="readonly", width=22)  #
#         self.cbo_database.grid(row=0, column=1, padx=10, pady=5)  #
#         self.cbo_database.set("LocalFile")  #
        
#         # Bắt sự kiện thay đổi lựa chọn combobox để ẩn/hiện trường động
#         self.cbo_database.bind("<<ComboboxSelected>>", self.on_database_change)  #

#         # Khung phụ động chứa các ô nhập token/webhook
#         self.dynamic_frame = ttk.Frame(db_frame)  #
#         self.dynamic_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)  #

#         # --- NÚT BẮT ĐẦU HÀNH TRÌNH TRANSLATE ---
#         self.btn_start = ttk.Button(self, text="🚀 BẮT ĐẦU TRANSLATE LIVE", command=self.initiate_capture_flow)  #
#         self.btn_start.pack(fill="x", padx=15, pady=12)  #

#         # --- KHUNG HIỂN THỊ ĐOẠN VĂN DỊCH TẠI CHỖ (THAY THẾ TERMINAL) ---
#         self.dashboard_frame = ttk.LabelFrame(self, text=" BẢNG ĐIỀU KHIỂN DỊCH LIVE NGUYÊN KHỐI ", padding=10)  #
        
#         # 🛠️ SỬA ĐỔI 1: Khởi tạo thanh Container chứa 2 nút Dừng lại và Quét lại song song nằm ngang
#         btn_container = ttk.Frame(self.dashboard_frame)
#         btn_container.pack(fill="x", pady=5)
        
#         # Nút Dừng lại nằm bên TAY TRÁI
#         self.btn_stop = ttk.Button(btn_container, text="🛑 DỪNG LẠI (STOP)", command=self.stop_live_monitoring)
#         self.btn_stop.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
#         # Nút Chọn lại nằm bên TAY PHẢI
#         self.btn_reselect = ttk.Button(btn_container, text="🔄 CHỌN LẠI VÙNG QUÉT (RE-SELECT)", command=self.reselect_roi)  #
#         self.btn_reselect.pack(side="right", fill="x", expand=True, padx=(5, 0))

#         ttk.Label(self.dashboard_frame, text="🔴 Văn Bản Gốc Đọc Được:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))  #
#         self.txt_original = scrolledtext.ScrolledText(self.dashboard_frame, height=5, font=("Consolas", 10), wrap=tk.WORD)  #
#         self.txt_original.pack(fill="both", expand=True, pady=2)  #

#         ttk.Label(self.dashboard_frame, text="🟢 Bản Dịch Hệ Thống Tại Chỗ:", font=("Arial", 10, "bold"), foreground="green").pack(anchor="w", pady=(5, 0))  #
#         self.txt_translated = scrolledtext.ScrolledText(self.dashboard_frame, height=6, font=("Arial", 10), wrap=tk.WORD)  #
#         self.txt_translated.pack(fill="both", expand=True, pady=2)  #

#     def on_database_change(self, event=None):  #
#         """Hàm tự động dọn dẹp và render ô cấu hình dữ liệu tương ứng khi đổi

#         option Database.
#         """
#         for widget in self.dynamic_frame.winfo_children():  #
#             widget.destroy()  #

#         selected_db = self.cbo_database.get()  #

#         if selected_db == "Discord":  #
#             ttk.Label(self.dynamic_frame, text="Discord Webhook URL:").pack(anchor="w", pady=2)  #
#             self.ent_webhook = ttk.Entry(self.dynamic_frame, width=54)  #
#             self.ent_webhook.pack(fill="x", pady=2)  #
#             self.ent_webhook.insert(0, storage.DISCORD_WEBHOOK_URL if "DÁN_LINK_WEBHOOK" not in storage.DISCORD_WEBHOOK_URL else "")  #

#         elif selected_db == "Telegram":  #
#             ttk.Label(self.dynamic_frame, text="Telegram Bot Token:").pack(anchor="w", pady=2)  #
#             self.ent_token = ttk.Entry(self.dynamic_frame, width=54)  #
#             self.ent_token.pack(fill="x", pady=2)  #
#             self.ent_token.insert(0, storage.TELEGRAM_BOT_TOKEN if "DÁN_TOKEN_BOT" not in storage.TELEGRAM_BOT_TOKEN else "")  #

#             ttk.Label(self.dynamic_frame, text="Telegram Chat ID:").pack(anchor="w", pady=2)  #
#             self.ent_chat_id = ttk.Entry(self.dynamic_frame, width=54)  #
#             self.ent_chat_id.pack(fill="x", pady=2)  #
#             self.ent_chat_id.insert(0, storage.TELEGRAM_CHAT_ID if "DÁN_CHAT_ID" not in storage.TELEGRAM_CHAT_ID else "")  #

#         elif selected_db == "LocalFile":  #
#             ttk.Label(self.dynamic_frame, text="📂 File lưu trữ offline: history_database.md").pack(anchor="w", pady=2)  #
#             btn_open_file = ttk.Button(self.dynamic_frame, text="📄 MỞ FILE LOG DATABASE (.MD)", command=self.open_local_database_file)  #
#             btn_open_file.pack(fill="x", pady=2)  #

#     def open_local_database_file(self):  #
#         """Hàm gọi trình soạn thảo hệ thống mở trực tiếp file Markdown Database."""
#         filepath = os.path.abspath(storage.LOCAL_DATABASE_PATH)  #
#         if not os.path.exists(filepath):  #
#             with open(filepath, "w", encoding="utf-8") as f:  #
#                 f.write("# 📚 LOCAL TRANSLATION AUDIT LOG DATABASE\n\n")  #

#         try:  #
#             if sys.platform == "win32":  #
#                 os.startfile(filepath)  #
#             elif sys.platform == "darwin":  #
#                 subprocess.call(["open", filepath])  #
#             else:  #
#                 subprocess.call(["xdg-open", filepath])  #
#         except Exception as e:  #
#             print(f"[GUI ERROR] Không thể mở file: {str(e)}")  #

#     def stop_live_monitoring(self):
#         """🛠️ SỬA ĐỒI 1: Hàm dừng hẳn luồng quét live, khôi phục lại trạng thái

#         giao diện Menu setup ban đầu.
#         """
#         self.is_live_active = False
#         self.monitor_coords = None
#         self.last_raw_block = ""
        
#         # Làm sạch nội dung các ô văn bản trên giao diện
#         self.txt_original.delete("1.0", tk.END)
#         self.txt_translated.delete("1.0", tk.END)
        
#         # Ẩn khung dashboard điều khiển dịch live khỏi màn hình
#         self.dashboard_frame.pack_forget()
        
#         # Co nhỏ kích thước cửa sổ về menu setup ban đầu
#         self.geometry("480x380")
        
#         # Khôi phục trạng thái hoạt động của nút Bắt đầu chính
#         self.btn_start.config(text="🚀 BẮT ĐẦU TRANSLATE LIVE")
#         self.btn_start.state(["!disabled"])

#     def reselect_roi(self):  #
#         """Hàm tạm dừng luồng quét ngầm, cho phép người dùng vẽ lại vùng quét mới

#         (ĐÃ SỬA LỖI 1: Cập nhật động cài đặt ngôn ngữ khi chọn lại).
#         """
#         self.is_live_active = False  #
#         self.withdraw()  #
#         time.sleep(0.3)  #

#         # Đọc lại giá trị từ combobox để cập nhật ngôn ngữ runtime ngay lập tức khi re-select
#         src_lang_name = self.cbo_source.get()  #
#         tgt_lang_name = self.cbo_target.get()  #
#         selected_db = self.cbo_database.get()  #

#         ocr_langs = self.supported_languages[src_lang_name]["ocr_code"]  #
#         trans_lang = self.supported_languages[tgt_lang_name]["trans_code"]  #

#         storage.DATABASE_BACKEND = selected_db  #
#         if selected_db == "Discord":  #
#             storage.DISCORD_WEBHOOK_URL = self.ent_webhook.get().strip()  #
#         elif selected_db == "Telegram":  #
#             storage.TELEGRAM_BOT_TOKEN = self.ent_token.get().strip()  #
#             storage.TELEGRAM_CHAT_ID = self.ent_chat_id.get().strip()  #

#         # Nạp lại bộ dịch thuật mới
#         self.reader = easyocr.Reader(ocr_langs, gpu=False)  #
#         self.translator = GoogleTranslator(source="auto", target=trans_lang)  #

#         try:  #
#             roi = self.get_user_selected_roi_cv2()  #
#             x, y, w, h = roi  #
#             if w <= 10 or h <= 10:  #
#                 raise ValueError("Vùng chọn không hợp lệ.")  #
#             self.monitor_coords = {"top": y, "left": x, "width": w, "height": h}  #
#         except Exception as e:  #
#             print(f"[GUI WARNING] Hủy chọn lại: {str(e)}")  #

#         self.deiconify()  #
#         self.is_live_active = True  #
#         self.live_thread = threading.Thread(target=self.live_translation_loop, daemon=True)  #
#         self.live_thread.start()  #

#     def initiate_capture_flow(self):  #
#         """Đồng bộ tham số cấu hình -> Biến mất app -> Gọi OpenCV selectROI ->

#         Kích hoạt đa luồng.
#         """
#         src_lang_name = self.cbo_source.get()  #
#         tgt_lang_name = self.cbo_target.get()  #
#         selected_db = self.cbo_database.get()  #

#         ocr_langs = self.supported_languages[src_lang_name]["ocr_code"]  #
#         trans_lang = self.supported_languages[tgt_lang_name]["trans_code"]  #

#         storage.DATABASE_BACKEND = selected_db  #
#         if selected_db == "Discord":  #
#             storage.DISCORD_WEBHOOK_URL = self.ent_webhook.get().strip()  #
#         elif selected_db == "Telegram":  #
#             storage.TELEGRAM_BOT_TOKEN = self.ent_token.get().strip()  #
#             storage.TELEGRAM_CHAT_ID = self.ent_chat_id.get().strip()  #

#         self.btn_start.config(text="🔄 ĐANG NẠP THƯ VIỆN AI... VUI LÒNG CHỜ...")  #
#         self.update()  #
        
#         self.reader = easyocr.Reader(ocr_langs, gpu=False)  #
#         self.translator = GoogleTranslator(source="auto", target=trans_lang)  #

#         self.withdraw()  #
#         time.sleep(0.3)  #

#         try:  #
#             roi = self.get_user_selected_roi_cv2()  #
#             x, y, w, h = roi  #
#             if w <= 10 or h <= 10:  #
#                 raise ValueError("Vùng chọn không hợp lệ.")  #
#             self.monitor_coords = {"top": y, "left": x, "width": w, "height": h}  #
#         except Exception as e:  #
#             self.deiconify()  #
#             self.btn_start.config(text="🚀 BẮT ĐẦU TRANSLATE LIVE")  #
#             print(f"[GUI WARNING] Hủy tiến trình kéo chuột: {str(e)}")  #
#             return  #

#         self.deiconify()  #
#         self.geometry("480x680")  #
#         self.dashboard_frame.pack(fill="both", expand=True, padx=15, pady=5)  #
#         self.btn_start.config(text="🛑 ĐANG CHẠY LIVE MONITORING (MƯỢT MÀ - 60FPS)")  #
#         self.btn_start.state(["disabled"])  #

#         self.is_live_active = True  #
#         self.live_thread = threading.Thread(target=self.live_translation_loop, daemon=True)  #
#         self.live_thread.start()  #

#     def get_user_selected_roi_cv2(self):  #
#         """🛠️ SỬA ĐỔI 2: Thuật toán đóng băng làm mờ màn hình nguyên khối.

#         Tích hợp ma trận giải thuật vẽ ô vuông nét đứt màu trắng (Dashed White Line) chuẩn Snipping Tool.
#         """
#         with mss.MSS() as sct:  #
#             screen_dim = {"top": 0, "left": 0, "width": 1920, "height": 1080}  #
#             screenshot = sct.grab(screen_dim)  #
#             bg_image = np.array(screenshot)  #
#             bg_image = cv2.cvtColor(bg_image, cv2.COLOR_BGRA2BGR)  #

#         ix, iy, cx, cy = -1, -1, -1, -1
#         drawing = False
#         done = False

#         # --- PHÂN HỆ THUẬT TOÁN VẼ NÉT ĐỨT THỦ CÔNG (CUSTOM DASHED RENDERER) ---
#         def draw_dashed_line(img, p1, p2, color, thickness=1, dash_length=6):
#             x1, y1 = p1
#             x2, y2 = p2
#             dx, dy = x2 - x1, y2 - y1
#             dist = np.hypot(dx, dy)
#             if dist == 0:
#                 return
#             num_dashes = int(dist / dash_length)
#             for i in range(num_dashes):
#                 if i % 2 == 0:  # Chỉ vẽ phân đoạn chẵn, bỏ trống đoạn lẻ tạo hiệu ứng đứt nét
#                     start_ratio = i / num_dashes
#                     end_ratio = min(1.0, (i + 1) / num_dashes)
#                     st_x = int(x1 + dx * start_ratio)
#                     st_y = int(y1 + dy * start_ratio)
#                     end_x = int(x1 + dx * end_ratio)
#                     end_y = int(y1 + dy * end_ratio)
#                     cv2.line(img, (st_x, st_y), (end_x, end_y), color, thickness)

#         def draw_dashed_rectangle(img, top_left, bottom_right, color, thickness=1, dash_length=6):
#             x1, y1 = top_left
#             x2, y2 = bottom_right
#             # Vẽ phân rã 4 cạnh của hình vuông thấu kính
#             draw_dashed_line(img, (x1, y1), (x2, y1), color, thickness, dash_length)  # Cạnh trên
#             draw_dashed_line(img, (x2, y1), (x2, y2), color, thickness, dash_length)  # Cạnh phải
#             draw_dashed_line(img, (x2, y2), (x1, y2), color, thickness, dash_length)  # Cạnh dưới
#             draw_dashed_line(img, (x1, y2), (x1, y1), color, thickness, dash_length)  # Cạnh trái

#         def mouse_snipping_callback(event, x, y, flags, param):
#             nonlocal ix, iy, cx, cy, drawing, done
#             if event == cv2.EVENT_LBUTTONDOWN:
#                 drawing = True
#                 ix, iy = x, y
#                 cx, cy = x, y
#             elif event == cv2.EVENT_MOUSEMOVE:
#                 if drawing:
#                     cx, cy = x, y
#             elif event == cv2.EVENT_LBUTTONUP:
#                 if drawing:
#                     drawing = False
#                     cx, cy = x, y
#                     done = True  # Thả chuột ra là tự động chốt đơn vùng quét chuẩn Snipping Tool  #

#         window_name = "Snipping Zone - Keo chuot chon vung can xem Live"  #
#         cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  #
#         cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  #
#         cv2.setMouseCallback(window_name, mouse_snipping_callback)  #

#         # TỐI ƯU FPS: Tính toán trước màn hình mờ 50% báo hiệu chờ quét
#         dark_overlay = cv2.convertScaleAbs(bg_image, alpha=0.5, beta=0)  #

#         while not done:  #
#             if drawing:  #
#                 display_img = dark_overlay.copy()  #
#                 x1, x2 = min(ix, cx), max(ix, cx)  #
#                 y1, y2 = min(iy, cy), max(iy, cy)  #
                
#                 # Trả lại độ sáng rực rỡ 100% gốc cho vùng thấu kính được kéo chuột
#                 if x2 > x1 and y2 > y1:  #
#                     display_img[y1:y2, x1:x2] = bg_image[y1:y2, x1:x2]  #
#                     # 🛠️ SỬA ĐỒI 2: Gọi hàm vẽ nét đứt màu trắng tinh khiết (255, 255, 255)
#                     draw_dashed_rectangle(display_img, (x1, y1), (x2, y2), (255, 255, 255), 1, dash_length=6)
#             else:
#                 if ix == -1:  #
#                     display_img = dark_overlay  #
#                 else:  #
#                     display_img = dark_overlay.copy()  #

#             cv2.imshow(window_name, display_img)  #
#             key = cv2.waitKey(1) & 0xFF  #
#             if key == 27 or key == ord('c'):  #
#                 cv2.destroyWindow(window_name)  #
#                 return (0, 0, 0, 0)  #

#         cv2.destroyWindow(window_name)  #
        
#         x1, x2 = min(ix, cx), max(ix, cx)  #
#         y1, y2 = min(iy, cy), max(iy, cy)  #
#         w = x2 - x1  #
#         h = y2 - y1  #
#         return (x1, y1, w, h)  #

#     def live_translation_loop(self):  #
#         """VÒNG LẶP TIẾN TRÌNH LUỒNG NGẦM: Cô lập hoàn toàn việc gọi AI tính toán

#         nặng ra khỏi giao diện chính.
#         """
#         while self.is_live_active:  #
#             if not self.monitor_coords:  #
#                 time.sleep(0.1)  #
#                 continue  #
#             try:  #
#                 with mss.MSS() as sct:  #
#                     screenshot = sct.grab(self.monitor_coords)  #
#                     frame = np.array(screenshot)  #
#                     frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  #

#                 w, h = self.monitor_coords["width"], self.monitor_coords["height"]  #
#                 enhanced = cv2.resize(frame, (int(w * 1.5), int(h * 1.5)), interpolation=cv2.INTER_LINEAR)  #
#                 results = self.reader.readtext(enhanced)  #

#                 if results:  #
#                     sorted_results = sorted(results, key=lambda b: b[0][0][1])  #
#                     reconstructed_lines = []  #

#                     while sorted_results:  #
#                         first_item = sorted_results.pop(0)  #
#                         line_items = [first_item]  #
#                         first_y = first_item[0][0][1]  #
#                         first_h = first_item[0][3][1] - first_item[0][0][1]  #

#                         remnants = []  #
#                         for item in sorted_results:  #
#                             item_y = item[0][0][1]  #
#                             if abs(item_y - first_y) < (first_h * 0.5):  #
#                                 line_items.append(item)  #
#                             else:  #
#                                 remnants.append(item)  #

#                         line_items.sort(key=lambda b: b[0][0][0])  #
#                         reconstructed_lines.append(line_items)  #
#                         sorted_results = remnants  #

#                     # THUẬT TOÁN ĐOẠN VĂN HÌNH HỌC THÔNG MINH
#                     line_data = []  #
#                     for line in reconstructed_lines:  #
#                         line_text = " ".join([item[1] for item in line]).strip()  #
#                         if not line_text:  #
#                             continue  #
                        
#                         x_mins = [item[0][0][0] for item in line] + [item[0][3][0] for item in line]  #
#                         x_maxs = [item[0][1][0] for item in line] + [item[0][2][0] for item in line]  #
#                         y_mins = [item[0][0][1] for item in line] + [item[0][1][1] for item in line]  #
#                         y_maxs = [item[0][2][1] for item in line] + [item[0][3][1] for item in line]  #
                        
#                         x_min = min(x_mins)  #
#                         x_max = max(x_maxs)  #
#                         y_min = min(y_mins)  #
#                         y_max = max(y_maxs)  #
#                         height_line = y_max - y_min  #
                        
#                         line_data.append({  #
#                             "text": line_text,  #
#                             "x_min": x_min,  #
#                             "x_max": x_max,  #
#                             "y_min": y_min,  #
#                             "y_max": y_max,  #
#                             "height": height_line  #
#                         })  #
                    
#                     current_raw_block = ""  #
#                     if line_data:  #
#                         global_x_min = min(ld["x_min"] for ld in line_data)  #
#                         global_x_max = max(ld["x_max"] for ld in line_data)  #
#                         full_scanned_width = max(1, global_x_max - global_x_min)  #
                        
#                         for idx, current in enumerate(line_data):  #
#                             current_raw_block += current["text"]  #
                            
#                             if idx < len(line_data) - 1:  #
#                                 next_line = line_data[idx + 1]  #
#                                 vertical_gap = next_line["y_min"] - current["y_max"]  #
#                                 avg_height = (current["height"] + next_line["height"]) / 2  #
#                                 is_short_line = (current["x_max"] < global_x_min + full_scanned_width * 0.82)  #
                                
#                                 if vertical_gap > avg_height * 1.5:  #
#                                     current_raw_block += "\n\n"  #
#                                 elif is_short_line:  #
#                                     current_raw_block += "\n"  #
#                                 else:  #
#                                     current_raw_block += " "  #

#                     current_raw_block = current_raw_block.strip()  #

#                     if current_raw_block == self.last_raw_block:  #
#                         time.sleep(0.4)  #
#                         continue  #

#                     self.last_raw_block = current_raw_block  #

#                     full_translated_block = ""  #
#                     if current_raw_block:  #
#                         try:  #
#                             translated_bundle = self.translator.translate(current_raw_block)  #
#                             full_translated_block = translated_bundle  #
#                         except Exception as e:  #
#                             full_translated_block = f"[LỖI KẾT NỐI MẠNG]: {str(e)}"  #

#                     central_database_router(current_raw_block, full_translated_block)  #
#                     self.after(0, self.update_gui_dashboard, current_raw_block, full_translated_block)  #
#                 else:  #
#                     if self.last_raw_block != "":  #
#                         self.last_raw_block = ""  #
#                         self.after(0, self.update_gui_dashboard, "", "... Đang chờ chữ xuất hiện trong vùng quét ...")  #
#             except Exception as thread_err:  #
#                 print(f"[THREAD WORKER WARNING] Lỗi luồng quét: {str(thread_err)}")  #

#             time.sleep(0.4)  #

#     def update_gui_dashboard(self, original, translated):  #
#         """Hàm an toàn luồng cập nhật chữ trực tiếp lên hộp thoại giao diện

#         Tkinter.
#         """
#         self.txt_original.delete("1.0", tk.END)  #
#         self.txt_original.insert(tk.END, original)  #
#         self.txt_translated.delete("1.0", tk.END)  #
#         self.txt_translated.insert(tk.END, translated)  #


# if __name__ == "__main__":  #
#     try:  #
#         app = MangaLiveTranslatorGUI()  #
#         app.on_database_change()  #
#         app.mainloop()  #
#     except KeyboardInterrupt:  #
#         print("\n[HỆ THỐNG] Đã tắt ứng dụng.")  #




#TEST 21
import os
import time
import warnings
import threading  # Thư viện đa luồng xử lý lag giao diện cực kỳ quan trọng
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import cv2
import easyocr
import mss
import numpy as np
from deep_translator import GoogleTranslator

# Gọi liên kết ngầm từ bộ thư viện lưu trữ đa kênh chúng ta đã hoàn thiện
import storage
from storage import central_database_router

# Khóa toàn bộ các cảnh báo hệ thống không cần thiết từ thư viện bên thứ ba
warnings.filterwarnings("ignore", category=UserWarning)


class MangaLiveTranslatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # ==============================================================================
        # CẤU HÌNH THUỘC TÍNH NỀN TẢNG CỦA CỬA SỔ
        # ==============================================================================
        self.title("Dịch ngôn ngữ Trực Tiếp")
        self.geometry("480x380")  # Kích thước tối ưu cho Menu ban đầu
        
        # Cho phép người dùng tự do phóng to thu nhỏ cửa sổ lên tận 1920x1080
        self.resizable(True, True)
        
        # Áp dụng phong cách giao diện phẳng, hiện đại
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Cấu hình danh mục ngôn ngữ đồng bộ với hệ thống OCR
        self.supported_languages = {
            "Tiếng Anh": {"ocr_code": ["en"], "trans_code": "en"},
            "Tiếng Việt": {"ocr_code": ["vi"], "trans_code": "vi"},
            "Tiếng Nhật": {"ocr_code": ["ja", "en"], "trans_code": "ja"},
            "Tiếng Hàn": {"ocr_code": ["ko", "en"], "trans_code": "ko"},
            "Tiếng Trung (Giản thể)": {"ocr_code": ["ch_sim", "en"], "trans_code": "zh-CN"},
            "Tiếng Pháp": {"ocr_code": ["fr", "en"], "trans_code": "fr"},
            "Tiếng Đức": {"ocr_code": ["de", "en"], "trans_code": "de"},
        }

        # Từ điển bản địa hóa thông báo "Không tìm thấy văn bản" (Yêu cầu bổ sung)
        self.no_text_messages = {
            "Tiếng Anh": "No text found in selected area",
            "Tiếng Việt": "Không tìm thấy văn bản trong vùng chọn",
            "Tiếng Nhật": "選択された範囲にテキストが見つかりません",
            "Tiếng Hàn": "선택한 영역에서 텍스트를 찾을 수 없습니다",
            "Tiếng Trung (Giản thể)": "在选择区域未找到文本",
            "Tiếng Pháp": "Aucun texte trouvé dans la zone sélectionnée",
            "Tiếng Đức": "Kein Text im ausgewählten Bereich gefunden"
        }

        # Biến quản lý trạng thái và đa luồng ngầm
        self.is_live_active = False
        self.is_paused = False  # Cờ lưu trữ trạng thái Tạm dừng / Tiếp tục
        self.live_thread = None  # Biến lưu trữ tiến trình luồng dịch ngầm
        self.last_raw_block = ""  # Bộ nhớ đệm chống trùng dữ liệu
        self.monitor_coords = None # Lưu tọa độ vùng kéo chuột
        self.reader = None
        self.translator = None

        # Khởi tạo toàn bộ các thành phần đồ họa của UI
        self.create_widgets()

    def create_widgets(self):
        """Hàm dựng toàn bộ bố cục khung điều khiển của Menu Giao diện."""
        # --- KHUNG CHỌN NGÔN NGỮ NGUỒN / ĐÍCH ---
        lang_frame = ttk.LabelFrame(self, text=" Cấu Hình Ngôn Ngữ Dịch ", padding=10)
        lang_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(lang_frame, text="Ngôn ngữ gốc (Màn hình):").grid(row=0, column=0, sticky="w", pady=5)
        self.cbo_source = ttk.Combobox(lang_frame, values=list(self.supported_languages.keys()), state="readonly", width=22)
        self.cbo_source.grid(row=0, column=1, padx=10, pady=5)
        self.cbo_source.set("Tiếng Anh")

        ttk.Label(lang_frame, text="Ngôn ngữ đích (Bản dịch):").grid(row=1, column=0, sticky="w", pady=5)
        self.cbo_target = ttk.Combobox(lang_frame, values=list(self.supported_languages.keys()), state="readonly", width=22)
        self.cbo_target.grid(row=1, column=1, padx=10, pady=5)
        self.cbo_target.set("Tiếng Việt")

        # --- KHUNG CẤU HÌNH CƠ SỞ DỮ LIỆU ---
        db_frame = ttk.LabelFrame(self, text=" Cấu Hình Kho Lưu Trữ (Database Backend) ", padding=10)
        db_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(db_frame, text="Chọn cổng Database:").grid(row=0, column=0, sticky="w", pady=5)
        self.cbo_database = ttk.Combobox(db_frame, values=["LocalFile", "Discord", "Telegram", "None"], state="readonly", width=22)
        self.cbo_database.grid(row=0, column=1, padx=10, pady=5)
        self.cbo_database.set("LocalFile")
        
        # Bắt sự kiện thay đổi lựa chọn combobox để ẩn/hiện trường động
        self.cbo_database.bind("<<ComboboxSelected>>", self.on_database_change)

        # Khung phụ động chứa các ô nhập token/webhook
        self.dynamic_frame = ttk.Frame(db_frame)
        self.dynamic_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        # --- NÚT BẮT ĐẦU HÀNH TRÌNH TRANSLATE ---
        self.btn_start = ttk.Button(self, text="🚀 BẮT ĐẦU TRANSLATE LIVE", command=self.initiate_capture_flow)
        self.btn_start.pack(fill="x", padx=15, pady=12)

        # --- KHUNG HIỂN THỊ ĐOẠN VĂN DỊCH TẠI CHỖ (THAY THẾ TERMINAL) ---
        self.dashboard_frame = ttk.LabelFrame(self, text=" BẢNG ĐIỀU KHIỂN DỊCH LIVE NGUYÊN KHỐI ", padding=10)
        
        # Container chứa thanh 3 nút điều hướng hàng ngang mượt mà (Tạm dừng, Chọn lại, Menu chính)
        btn_container = ttk.Frame(self.dashboard_frame)
        btn_container.pack(fill="x", pady=5)
        
        # 1. Nút Tạm dừng / Tiếp tục (Toggle State)
        self.btn_stop = ttk.Button(btn_container, text="🛑 TẠM DỪNG (PAUSE)", command=self.toggle_pause_resume)
        self.btn_stop.pack(side="left", fill="x", expand=True, padx=(0, 2))
        
        # 2. Nút Chọn lại vùng quét
        self.btn_reselect = ttk.Button(btn_container, text="🔄 CHỌN LẠI (RE-SELECT)", command=self.reselect_roi)
        self.btn_reselect.pack(side="left", fill="x", expand=True, padx=(2, 2))

        # 3. Nút Quay trở lại Menu cài đặt gốc
        self.btn_menu = ttk.Button(btn_container, text="🏠 MENU CHÍNH", command=self.go_back_to_menu)
        self.btn_menu.pack(side="left", fill="x", expand=True, padx=(2, 0))

        ttk.Label(self.dashboard_frame, text="🔴 Văn Bản Gốc Đọc Được:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
        self.txt_original = scrolledtext.ScrolledText(self.dashboard_frame, height=5, font=("Consolas", 10), wrap=tk.WORD)
        self.txt_original.pack(fill="both", expand=True, pady=2)

        ttk.Label(self.dashboard_frame, text="🟢 Bản Dịch Hệ Thống Tại Chỗ:", font=("Arial", 10, "bold"), foreground="green").pack(anchor="w", pady=(5, 0))
        self.txt_translated = scrolledtext.ScrolledText(self.dashboard_frame, height=6, font=("Arial", 10), wrap=tk.WORD)
        self.txt_translated.pack(fill="both", expand=True, pady=2)

    def on_database_change(self, event=None):
        """Hàm tự động dọn dẹp và render ô cấu hình dữ liệu tương ứng khi đổi

        option Database.
        """
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        selected_db = self.cbo_database.get()

        if selected_db == "Discord":
            ttk.Label(self.dynamic_frame, text="Discord Webhook URL:").pack(anchor="w", pady=2)
            self.ent_webhook = ttk.Entry(self.dynamic_frame, width=54)
            self.ent_webhook.pack(fill="x", pady=2)
            self.ent_webhook.insert(0, storage.DISCORD_WEBHOOK_URL if "DÁN_LINK_WEBHOOK" not in storage.DISCORD_WEBHOOK_URL else "")

        elif selected_db == "Telegram":
            ttk.Label(self.dynamic_frame, text="Telegram Bot Token:").pack(anchor="w", pady=2)
            self.ent_token = ttk.Entry(self.dynamic_frame, width=54)
            self.ent_token.pack(fill="x", pady=2)
            self.ent_token.insert(0, storage.TELEGRAM_BOT_TOKEN if "DÁN_TOKEN_BOT" not in storage.TELEGRAM_BOT_TOKEN else "")

            ttk.Label(self.dynamic_frame, text="Telegram Chat ID:").pack(anchor="w", pady=2)
            self.ent_chat_id = ttk.Entry(self.dynamic_frame, width=54)
            self.ent_chat_id.pack(fill="x", pady=2)
            self.ent_chat_id.insert(0, storage.TELEGRAM_CHAT_ID if "DÁN_CHAT_ID" not in storage.TELEGRAM_CHAT_ID else "")

        elif selected_db == "LocalFile":
            ttk.Label(self.dynamic_frame, text="📂 File lưu trữ offline: history_database.md").pack(anchor="w", pady=2)
            btn_open_file = ttk.Button(self.dynamic_frame, text="📄 MỞ FILE LOG DATABASE (.MD)", command=self.open_local_database_file)
            btn_open_file.pack(fill="x", pady=2)

    def open_local_database_file(self):
        """Hàm gọi trình soạn thảo hệ thống mở trực tiếp file Markdown Database."""
        filepath = os.path.abspath(storage.LOCAL_DATABASE_PATH)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("# 📚 LOCAL TRANSLATION AUDIT LOG DATABASE\n\n")

        try:
            if sys.platform == "win32":
                os.startfile(filepath)
            elif sys.platform == "darwin":
                subprocess.call(["open", filepath])
            else:
                subprocess.call(["xdg-open", filepath])
        except Exception as e:
            print(f"[GUI ERROR] Không thể mở file: {str(e)}")

    def toggle_pause_resume(self):
        """Hàm điều khiển Tạm dừng (Pause) / Tiếp tục (Resume) luồng quét mà không

        làm mất vùng tọa độ đã chọn.
        """
        if not self.is_paused:
            # Chuyển đổi sang trạng thái Tạm dừng
            self.is_live_active = False
            self.is_paused = True
            self.btn_stop.config(text="▶️ TIẾP TỤC (RESUME)")
            self.dashboard_frame.config(text=" BẢNG ĐIỀU KHIỂN DỊCH LIVE NGUYÊN KHỐI (ĐANG TẠM DỪNG) ")
        else:
            # Chuyển đổi ngược về trạng thái Tiếp tục dịch
            self.is_paused = False
            self.btn_stop.config(text="🛑 TẠM DỪNG (PAUSE)")
            self.dashboard_frame.config(text=" BẢNG ĐIỀU KHIỂN DỊCH LIVE NGUYÊN KHỐI ")
            self.is_live_active = True
            # Hồi sinh lại luồng quét ngầm với tọa độ cũ
            self.live_thread = threading.Thread(target=self.live_translation_loop, daemon=True)
            self.live_thread.start()

    def go_back_to_menu(self):
        """Hàm dừng hẳn luồng dịch và dọn dẹp để thu nhỏ cửa sổ về Menu setup ban

        đầu.
        """
        self.is_live_active = False
        self.is_paused = False
        self.monitor_coords = None
        self.last_raw_block = ""
        
        # Làm sạch văn bản trên các hộp thoại
        self.txt_original.delete("1.0", tk.END)
        self.txt_translated.delete("1.0", tk.END)
        
        # Ẩn khung dashboard điều khiển live
        self.dashboard_frame.pack_forget()
        
        # Thu nhỏ cửa sổ về menu setup
        self.geometry("480x380")
        
        # Khôi phục trạng thái nút setup ban đầu
        self.btn_stop.config(text="🛑 TẠM DỪNG (PAUSE)")
        self.dashboard_frame.config(text=" BẢNG ĐIỀU KHIỂN DỊCH LIVE NGUYÊN KHỐI ")
        self.btn_start.config(text="🚀 BẮT ĐẦU TRANSLATE LIVE")
        self.btn_start.state(["!disabled"])

    def reselect_roi(self):
        """Hàm tạm dừng luồng quét ngầm, cho phép người dùng vẽ lại vùng quét mới."""
        self.is_live_active = False
        self.withdraw()
        time.sleep(0.3)

        # Đọc lại giá trị từ combobox để cập nhật ngôn ngữ runtime ngay lập tức khi re-select
        src_lang_name = self.cbo_source.get()
        tgt_lang_name = self.cbo_target.get()
        selected_db = self.cbo_database.get()

        ocr_langs = self.supported_languages[src_lang_name]["ocr_code"]
        trans_lang = self.supported_languages[tgt_lang_name]["trans_code"]

        storage.DATABASE_BACKEND = selected_db
        if selected_db == "Discord":
            storage.DISCORD_WEBHOOK_URL = self.ent_webhook.get().strip()
        elif selected_db == "Telegram":
            storage.TELEGRAM_BOT_TOKEN = self.ent_token.get().strip()
            storage.TELEGRAM_CHAT_ID = self.ent_chat_id.get().strip()

        # Nạp lại bộ dịch thuật mới phù hợp cấu hình mới thay đổi
        self.reader = easyocr.Reader(ocr_langs, gpu=False)
        self.translator = GoogleTranslator(source="auto", target=trans_lang)

        try:
            roi = self.get_user_selected_roi_cv2()
            x, y, w, h = roi
            if w <= 10 or h <= 10:
                raise ValueError("Vùng chọn không hợp lệ.")
            self.monitor_coords = {"top": y, "left": x, "width": w, "height": h}
        except Exception as e:
            print(f"[GUI WARNING] Hủy chọn lại: {str(e)}")

        self.deiconify()
        
        # Khôi phục trạng thái nút bấm Tạm dừng
        self.is_paused = False
        self.btn_stop.config(text="🛑 TẠM DỪNG (PAUSE)")
        self.dashboard_frame.config(text=" BẢNG ĐIỀU KHIỂN DỊCH LIVE NGUYÊN KHỐI ")

        self.is_live_active = True
        self.live_thread = threading.Thread(target=self.live_translation_loop, daemon=True)
        self.live_thread.start()

    def initiate_capture_flow(self):
        """Đồng bộ tham số cấu hình -> Biến mất app -> Gọi OpenCV selectROI ->

        Kích hoạt đa luồng.
        """
        src_lang_name = self.cbo_source.get()
        tgt_lang_name = self.cbo_target.get()
        selected_db = self.cbo_database.get()

        ocr_langs = self.supported_languages[src_lang_name]["ocr_code"]
        trans_lang = self.supported_languages[tgt_lang_name]["trans_code"]

        storage.DATABASE_BACKEND = selected_db
        if selected_db == "Discord":
            storage.DISCORD_WEBHOOK_URL = self.ent_webhook.get().strip()
        elif selected_db == "Telegram":
            storage.TELEGRAM_BOT_TOKEN = self.ent_token.get().strip()
            storage.TELEGRAM_CHAT_ID = self.ent_chat_id.get().strip()

        self.btn_start.config(text="🔄 ĐANG NẠP THƯ VIỆN AI... VUI LÒNG CHỜ...")
        self.update()
        
        self.reader = easyocr.Reader(ocr_langs, gpu=False)
        self.translator = GoogleTranslator(source="auto", target=trans_lang)

        self.withdraw()
        time.sleep(0.3)

        try:
            roi = self.get_user_selected_roi_cv2()
            x, y, w, h = roi
            if w <= 10 or h <= 10:
                raise ValueError("Vùng chọn không hợp lệ.")
            self.monitor_coords = {"top": y, "left": x, "width": w, "height": h}
        except Exception as e:
            self.deiconify()
            self.btn_start.config(text="🚀 BẮT ĐẦU TRANSLATE LIVE")
            print(f"[GUI WARNING] Hủy tiến trình kéo chuột: {str(e)}")
            return

        self.deiconify()
        self.geometry("480x680")
        self.dashboard_frame.pack(fill="both", expand=True, padx=15, pady=5)
        self.btn_start.config(text="🛑 ĐANG CHẠY LIVE MONITORING (MƯỢT MÀ - 60FPS)")
        self.btn_start.state(["disabled"])

        self.is_live_active = True
        self.live_thread = threading.Thread(target=self.live_translation_loop, daemon=True)
        self.live_thread.start()

    def get_user_selected_roi_cv2(self):
        """Thuật toán đóng băng làm mờ màn hình nguyên khối.

        Vẽ ô vuông nét đứt màu trắng (Dashed White Line) chuẩn Snipping Tool.
        """
        with mss.MSS() as sct:
            screen_dim = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            screenshot = sct.grab(screen_dim)
            bg_image = np.array(screenshot)
            bg_image = cv2.cvtColor(bg_image, cv2.COLOR_BGRA2BGR)

        ix, iy, cx, cy = -1, -1, -1, -1
        drawing = False
        done = False

        # --- THUẬT TOÁN VẼ NÉT ĐỨT THỦ CÔNG (CUSTOM DASHED RENDERER) ---
        def draw_dashed_line(img, p1, p2, color, thickness=1, dash_length=6):
            x1, y1 = p1
            x2, y2 = p2
            dx, dy = x2 - x1, y2 - y1
            dist = np.hypot(dx, dy)
            if dist == 0:
                return
            num_dashes = int(dist / dash_length)
            for i in range(num_dashes):
                if i % 2 == 0:  # Chỉ vẽ phân đoạn chẵn, bỏ trống đoạn lẻ tạo hiệu ứng đứt nét
                    start_ratio = i / num_dashes
                    end_ratio = min(1.0, (i + 1) / num_dashes)
                    st_x = int(x1 + dx * start_ratio)
                    st_y = int(y1 + dy * start_ratio)
                    end_x = int(x1 + dx * end_ratio)
                    end_y = int(y1 + dy * end_ratio)
                    cv2.line(img, (st_x, st_y), (end_x, end_y), color, thickness)

        def draw_dashed_rectangle(img, top_left, bottom_right, color, thickness=1, dash_length=6):
            x1, y1 = top_left
            x2, y2 = bottom_right
            # Vẽ phân rã 4 cạnh của hình vuông thấu kính
            draw_dashed_line(img, (x1, y1), (x2, y1), color, thickness, dash_length)  # Cạnh trên
            draw_dashed_line(img, (x2, y1), (x2, y2), color, thickness, dash_length)  # Cạnh phải
            draw_dashed_line(img, (x2, y2), (x1, y2), color, thickness, dash_length)  # Cạnh dưới
            draw_dashed_line(img, (x1, y2), (x1, y1), color, thickness, dash_length)  # Cạnh trái

        def mouse_snipping_callback(event, x, y, flags, param):
            nonlocal ix, iy, cx, cy, drawing, done
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                ix, iy = x, y
                cx, cy = x, y
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    cx, cy = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                if drawing:
                    drawing = False
                    cx, cy = x, y
                    done = True  # Thả chuột ra là tự động chốt đơn vùng quét chuẩn Snipping Tool

        window_name = "Snipping Zone - Keo chuot chon vung can xem Live"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback(window_name, mouse_snipping_callback)

        # TỐI ƯU FPS: Tính toán trước màn hình mờ 50% báo hiệu chờ quét
        dark_overlay = cv2.convertScaleAbs(bg_image, alpha=0.5, beta=0)

        while not done:
            if drawing:
                display_img = dark_overlay.copy()
                x1, x2 = min(ix, cx), max(ix, cx)
                y1, y2 = min(iy, cy), max(iy, cy)
                
                # Trả lại độ sáng rực rỡ 100% gốc cho vùng thấu kính được kéo chuột
                if x2 > x1 and y2 > y1:
                    display_img[y1:y2, x1:x2] = bg_image[y1:y2, x1:x2]
                    # Vẽ nét đứt màu trắng tinh khiết (255, 255, 255)
                    draw_dashed_rectangle(display_img, (x1, y1), (x2, y2), (255, 255, 255), 1, dash_length=6)
            else:
                if ix == -1:
                    display_img = dark_overlay
                else:
                    display_img = dark_overlay.copy()

            cv2.imshow(window_name, display_img)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('c'):
                cv2.destroyWindow(window_name)
                return (0, 0, 0, 0)

        cv2.destroyWindow(window_name)
        
        x1, x2 = min(ix, cx), max(ix, cx)
        y1, y2 = min(iy, cy), max(iy, cy)
        w = x2 - x1
        h = y2 - y1
        return (x1, y1, w, h)

    def live_translation_loop(self):
        """VÒNG LẶP TIẾN TRÌNH LUỒNG NGẦM: Cô lập hoàn toàn việc gọi AI tính toán

        nặng ra khỏi giao diện chính.
        """
        while self.is_live_active:
            if not self.monitor_coords:
                time.sleep(0.1)
                continue
            try:
                with mss.MSS() as sct:
                    screenshot = sct.grab(self.monitor_coords)
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                w, h = self.monitor_coords["width"], self.monitor_coords["height"]
                enhanced = cv2.resize(frame, (int(w * 1.5), int(h * 1.5)), interpolation=cv2.INTER_LINEAR)
                results = self.reader.readtext(enhanced)

                if results:
                    sorted_results = sorted(results, key=lambda b: b[0][0][1])
                    reconstructed_lines = []

                    while sorted_results:
                        first_item = sorted_results.pop(0)
                        line_items = [first_item]
                        first_y = first_item[0][0][1]
                        first_h = first_item[0][3][1] - first_item[0][0][1]

                        remnants = []
                        for item in sorted_results:
                            item_y = item[0][0][1]
                            if abs(item_y - first_y) < (first_h * 0.5):
                                line_items.append(item)
                            else:
                                remnants.append(item)

                        line_items.sort(key=lambda b: b[0][0][0])
                        reconstructed_lines.append(line_items)
                        sorted_results = remnants

                    # Thuật toán tính toán khoảng cách dọc để tự động bo tròn gộp đoạn văn bản
                    paragraphs = []
                    current_para = []
                    last_y = None
                    last_h = None

                    for line in reconstructed_lines:
                        avg_y = sum([item[0][0][1] for item in line]) / len(line)
                        avg_h = sum([item[0][3][1] - item[0][0][1] for item in line]) / len(line)
                        line_text = " ".join([item[1] for item in line]).strip()
                        
                        if not line_text:
                            continue

                        if last_y is None:
                            current_para.append(line_text)
                        else:
                            vertical_gap = avg_y - (last_y + last_h)
                            if vertical_gap < (last_h * 1.3):
                                current_para.append(line_text)
                            else:
                                paragraphs.append(" ".join(current_para))
                                current_para = [line_text]

                        last_y = avg_y
                        last_h = avg_h

                    if current_para:
                        paragraphs.append(" ".join(current_para))

                    current_raw_block = "\n\n".join(paragraphs)

                    if current_raw_block == self.last_raw_block:
                        time.sleep(0.4)
                        continue

                    self.last_raw_block = current_raw_block

                    full_translated_block = ""
                    if paragraphs:
                        try:
                            translated_bundle = self.translator.translate(current_raw_block)
                            full_translated_block = translated_bundle
                        except Exception as e:
                            full_translated_block = f"[LỖI KẾT NỐI MẠNG]: {str(e)}"

                    central_database_router(current_raw_block, full_translated_block)
                    
                    # Gọi cập nhật đồ họa lên luồng chính GUI (Thread-safe Call)
                    self.after(0, self.update_gui_dashboard, current_raw_block, full_translated_block)
                else:
                    # 🛠️ NÂNG CẤP ĐỘT PHÁ: Hiển thị thông báo "Không tìm thấy văn bản" được bản địa hóa
                    if self.last_raw_block != "no_text_found_state":
                        self.last_raw_block = "no_text_found_state"
                        
                        # Lấy cấu hình ngôn ngữ hiện tại để dịch thông báo tương ứng
                        src_lang_name = self.cbo_source.get()
                        tgt_lang_name = self.cbo_target.get()
                        
                        # Lấy thông điệp tương ứng từ từ điển
                        msg_original = self.no_text_messages.get(src_lang_name, "No text found in selected area")
                        msg_translated = self.no_text_messages.get(tgt_lang_name, "Không tìm thấy văn bản trong vùng chọn")
                        
                        # Cập nhật an toàn lên cả 2 ô Textbox
                        self.after(0, self.update_gui_dashboard, msg_original, msg_translated)
                        
            except Exception as thread_err:
                print(f"[THREAD WORKER WARNING] Lỗi luồng quét: {str(thread_err)}")

            time.sleep(0.4)  # Tần suất quét live mượt mà

    def update_gui_dashboard(self, original, translated):
        """Hàm an toàn luồng cập nhật chữ trực tiếp lên hộp thoại giao diện

        Tkinter.
        """
        self.txt_original.delete("1.0", tk.END)
        self.txt_original.insert(tk.END, original)
        self.txt_translated.delete("1.0", tk.END)
        self.txt_translated.insert(tk.END, translated)


if __name__ == "__main__":
    try:
        app = MangaLiveTranslatorGUI()
        app.on_database_change()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n[HỆ THỐNG] Đã tắt ứng dụng.")