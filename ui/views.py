import os
import whisper
from pydub import AudioSegment
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import time
# Load Whisper model
model = whisper.load_model("small")
# model = whisper.load_model("small.pt")
# model = whisper.load_model("base")

@method_decorator(csrf_exempt, name='dispatch')
class voice_form_english(View):
    template = 'voice_form_english.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        if "audio" not in request.FILES:
            return JsonResponse({"error": "No audio file provided"})

        currentField = request.POST.get("currentField")
        path = 'static/audios/'
        uid= str(time.time())
        os.makedirs(path, exist_ok=True)  # Ensure directory exists
        audio_file_name = f"{uid}_{currentField}_audio.wav"
        audio_path = os.path.join(path, audio_file_name)

        # Save uploaded audio file
        with open(audio_path, "wb") as vid:
            vid.write(request.FILES['audio'].read())

        try:

            # Transcribe with Whisper
            options = dict(language='english')
            transcribe_options = dict(task="transcribe", **options)
            result = model.transcribe(audio_path,**transcribe_options)

            # os.remove(audio_path)  # Remove original file
            text_file_name = f"{uid}_{currentField}_audio.txt"
            text_path = os.path.join(path, text_file_name)
            with open(text_path, "w") as text_file:
                text_file.write(result["text"])

            return JsonResponse({"text": result["text"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
