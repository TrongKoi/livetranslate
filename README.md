# Live Translator Pro

An advanced, high-performance, and privacy-focused real-time screen translation utility app for Windows. Built entirely in Python with a beautiful multi-threaded GUI, allowing users to capture, recognize text via local AI (OCR), and stream non-flicker translations seamlessly without console dependency.

---

## Key Features

- Snipping-Tool-Like Capture: Smooth dark overlay freeze-screen with a custom-engineered white dashed boundary box (60+ FPS dynamic render).
- Multi-Backend Storage Router: Dynamically routes log pipelines to Cloud Servers (Discord Embeds / Telegram Rich HTML) or saves locally as clean Markdown Code Blocks.
- Flawless Drag & Multithreading: Heavy background worker threads split from the main Tkinter UI thread, guaranteeing zero window lagging or freezing.
- Smart Paragraph Unification: Geometrically calculates text block line heights to reassemble split text organically into smooth flow paragraphs, avoiding ugly broken format lines.
- 100% Privacy First: Direct decentralized network traffic. Application settings/tokens remain purely client-side. No developer analytics tracking.

---

## Installation & Setup (For Developers)

1. Clone this repository to your local directory:
git clone [https://github.com/your-username/manga-live-translator.git](https://github.com/your-username/manga-live-translator.git)

2. Install the certified dependency modules:
pip install mss easyocr opencv-python numpy deep-translator requests

3. Launch the central core:
python main.py

---

## Packaging to Standalone App (.EXE)

To compile the application into a single executable binary that boots natively on Windows without Python environments installed:

pip install pyinstaller
pyinstaller --onefile --noconsole --name="Manga Live Translator Pro" main.py

Once compilation finishes, your standalone production-ready application will be located inside the /dist directory.

---

## Privacy & Data Confidentiality Statement

This application is strictly Privacy-By-Design:
- Local AI Inference: Image capturing (mss) and Text Recognition (EasyOCR) run entirely offline locally inside your local machine hardware. No telemetry logs or captured image frames are uploaded to external tracking servers.
- Decentralized Direct Requests: Data dispatching modules (requests) transmit data packets directly and exclusively to endpoints (Discord webhooks / Telegram bot keys) manually filled out by the active end-user inside the interface frame.

---

## License
Distributed under the MIT License. See LICENSE for more information.
