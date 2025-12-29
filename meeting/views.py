import tempfile
import os

from django.core.files import File
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Meeting
from .forms import UploadMeetingForm
from .utils import (
    convert_to_wav,
    transcribe_audio,
    summarize_text,
    generate_pdf,
    save_txt_docx,
    extract_keywords
)


@login_required
def dashboard(request):
    form = UploadMeetingForm()

    if request.method == "POST":
        form = UploadMeetingForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data["file"]

            meeting = Meeting.objects.create(
                user=request.user,
                original_file=uploaded_file
            )

            suffix = os.path.splitext(uploaded_file.name)[1]
            temp_input_path = None
            wav_path = None
            pdf_path = None
            txt_path = None
            docx_path = None

            try:
                # Save temporary uploaded file
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
                    for chunk in uploaded_file.chunks():
                        temp_input.write(chunk)
                    temp_input_path = temp_input.name

                # 1️⃣ Convert to WAV
                wav_path, duration = convert_to_wav(temp_input_path)

                # 2️⃣ Transcribe
                transcript, timeline, speakers = transcribe_audio(wav_path)

                # 3️⃣ Summarize & extract decisions/action items
                summary, decisions, action_items = summarize_text(transcript)

                # 4️⃣ Extract keywords
                keywords = extract_keywords(summary)

                # 5️⃣ Generate PDF with keywords
                pdf_path = generate_pdf(request.user, summary, duration, keywords=keywords)

                # 6️⃣ Save TXT & DOCX
                txt_path, docx_path = save_txt_docx(request.user, summary)

                # Save all to DB
                meeting.transcript = transcript
                meeting.summary = summary
                meeting.decisions = decisions
                meeting.action_items = action_items
                meeting.timeline = timeline
                meeting.speakers = speakers

                with open(pdf_path, "rb") as pdf_file:
                    meeting.pdf.save(os.path.basename(pdf_path), File(pdf_file), save=False)
                if txt_path:
                    with open(txt_path, "rb") as f:
                        meeting.txt.save(os.path.basename(txt_path), File(f), save=False)
                if docx_path:
                    with open(docx_path, "rb") as f:
                        meeting.docx.save(os.path.basename(docx_path), File(f), save=False)

                meeting.keywords = ", ".join(keywords)
                meeting.save()

                messages.success(request, "✅ Meeting processed successfully!")
                return redirect("history")

            except Exception as e:
                meeting.delete()
                messages.error(request, f"❌ Processing failed: {str(e)}")

            finally:
                for path in [temp_input_path, wav_path, pdf_path, txt_path, docx_path]:
                    if path and os.path.exists(path):
                        try:
                            os.remove(path)
                        except Exception:
                            pass

    return render(request, "dashboard.html", {"form": form})


@login_required
def history(request):
    query = request.GET.get("q")
    meetings = Meeting.objects.filter(user=request.user)
    if query:
        meetings = meetings.filter(summary__icontains=query)
    meetings = meetings.order_by("-created_at")
    return render(request, "history.html", {"history": meetings})


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def summary_avatar(request, meeting_id):
    """Render animated AI avatar summary page"""
    meeting = Meeting.objects.get(id=meeting_id, user=request.user)
    return render(request, "summary_avatar.html", {"meeting": meeting})
