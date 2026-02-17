🚀 AI Meeting Note Generator
📌 Overview

AI Meeting Note Generator is a Django-based AI application that automatically converts meeting audio/video into structured meeting notes. It uses local AI models for speech-to-text transcription, summarization, and information extraction.

The system generates:

Full Transcript

Meeting Summary

Decisions

Action Items

Speaker Timeline

Downloadable Reports (PDF, TXT, DOCX)

✨ Features

✅ Upload audio or video meeting files
✅ Offline Speech-to-Text using Whisper
✅ AI Meeting Summarization (BART Transformer)
✅ Decision & Action Item Extraction
✅ Speaker Timeline Generation
✅ PDF, TXT, DOCX Export
✅ Secure Django Authentication
✅ Local Processing (No Cloud API Cost)

🧠 AI Models Used
Task	Model
Speech Recognition	OpenAI Whisper (Local)
Summarization	facebook/bart-large-cnn
NLP Extraction	google/flan-t5-small
🏗️ Tech Stack

Backend: Django

AI/ML: PyTorch, Transformers, Whisper

Audio Processing: FFmpeg

PDF Generation: ReportLab

Database: SQLite / PostgreSQL

Frontend: HTML, CSS, Bootstrap

📂 Project Structure
project/
│
├ meeting/
│ ├ utils.py
│ ├ views.py
│ ├ models.py
│
├ templates/
├ static/
├ media/
├ manage.py

⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/yourusername/ai-meeting-note-generator.git
cd ai-meeting-note-generator

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install Requirements
pip install -r requirements.txt

4️⃣ Install FFmpeg

Linux:

sudo apt install ffmpeg


Windows:
Download from ffmpeg official website.

5️⃣ Run Migrations
python manage.py migrate

6️⃣ Run Server
python manage.py runserver

📤 Usage

Login / Register

Upload Meeting Audio or Video

AI Processes Meeting

Download Generated Notes

📊 Output Example

Transcript

Summary

Decisions

Action Items

Speaker Timeline

🔐 Privacy

✔ Runs fully offline
✔ No third-party API required
✔ Secure local processing

🚀 Future Improvements

Real-time meeting processing

Multi-language support

Cloud deployment

Team collaboration dashboard

Meeting sentiment analysis

👨‍💻 Author

Bappa Saha
AI Researcher | Software Developer

📜 License

MIT License
