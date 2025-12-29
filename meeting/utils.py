import subprocess
import tempfile
import os
import wave
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Whisper LOCAL for transcription
import whisper
# Offline summarization & NLP extraction
from transformers import pipeline

# Keyword extraction
from sklearn.feature_extraction.text import TfidfVectorizer

# Load Whisper model
WHISPER_MODEL = whisper.load_model("base")  # small/medium/large for accuracy

# Summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Optional simple action item extractor
action_item_extractor = pipeline("text2text-generation", model="google/flan-t5-small")


def convert_to_wav(input_path):
    """Convert audio/video file to WAV (16kHz mono)"""
    output_path = input_path + ".wav"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(output_path):
        raise Exception("Audio conversion failed")

    # Check duration
    with wave.open(output_path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)

    if duration < 1:
        raise Exception("Audio is empty or too short")

    return output_path, round(duration, 2)


def transcribe_audio(wav_path):
    """Transcribe audio using Whisper and return transcript + speaker timeline"""
    if os.path.getsize(wav_path) < 5000:
        raise Exception("Invalid or empty audio file")

    result = WHISPER_MODEL.transcribe(wav_path, word_timestamps=True)
    transcript = result.get("text", "").strip()

    timeline = []
    speakers = {}
    for idx, segment in enumerate(result.get("segments", [])):
        speaker_name = f"Speaker {segment.get('speaker', idx % 2 + 1)}"
        timeline.append({
            "start": segment["start"],
            "end": segment["end"],
            "speaker": speaker_name,
            "text": segment["text"]
        })
        speakers[speaker_name] = speakers.get(speaker_name, 0) + 1

    return transcript, timeline, speakers


def summarize_text(text):
    """Summarize text and extract decisions/action items"""
    if len(text.split()) < 50:
        summary_text = f"Meeting Summary:\n{text}"
    else:
        summary_list = summarizer(text, max_length=150, min_length=50, do_sample=False)
        summary_text = summary_list[0]["summary_text"]

    # Extract decisions & action items
    extraction_prompt = f"Extract decisions and action items from the following text:\n{text}"
    extracted = action_item_extractor(extraction_prompt)[0]["generated_text"]
    decisions = "\n".join([line.strip() for line in extracted.split("Decision:") if line.strip()][:5])
    action_items = "\n".join([line.strip() for line in extracted.split("Action:") if line.strip()][:5])

    return summary_text, decisions, action_items


def extract_keywords(text, top_n=10):
    """Extract top N keywords from text using TF-IDF"""
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    X = vectorizer.fit_transform([text])
    return list(vectorizer.get_feature_names_out())


def generate_pdf(user, content, duration, keywords=None):
    """Generate PDF from content and include keywords"""
    output_path = tempfile.mktemp(suffix=".pdf")
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)
    elements = []

    # Header
    elements.append(Paragraph(
        f"<b>AI Meeting Note Generator</b><br/>"
        f"Name: {user.full_name}<br/>"
        f"Email: {user.email}<br/>"
        f"Duration: {duration} seconds<br/><br/>",
        styles["Normal"]
    ))

    # Meeting content
    for line in content.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 10))

    # Keywords section
    if keywords:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("<b>Keywords:</b> " + ", ".join(keywords), styles["Normal"]))

    doc.build(elements)
    return output_path


def save_txt_docx(user, content):
    """Save TXT and DOCX locally"""
    txt_path = tempfile.mktemp(suffix=".txt")
    docx_path = tempfile.mktemp(suffix=".docx")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        from docx import Document
        doc = Document()
        for line in content.split("\n"):
            doc.add_paragraph(line)
        doc.save(docx_path)
    except ImportError:
        docx_path = None

    return txt_path, docx_path
