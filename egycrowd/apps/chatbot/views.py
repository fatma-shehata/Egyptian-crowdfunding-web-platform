from google import genai
from google.genai import types
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .tools import CHATBOT_TOOLS

SYSTEM_PROMPT = """You are the official assistant for EgyCrowd, a crowdfunding
platform for Egypt. You help visitors understand how the platform works
(registration, starting a project, donating, categories, ratings, comments)
and you can look up real, live data about projects using your tools.

Rules:
- When asked about top/lowest/best/worst projects, platform statistics, or
  project search, ALWAYS use the relevant tool — never guess or make up numbers.
- Keep answers concise and friendly, 2-4 sentences unless listing multiple projects.
- When listing projects, include their name and key stat (amount raised, rating, etc).
- If you don't have a tool for something, say so honestly and suggest browsing
  the site directly.
- Respond in the same language the user wrote in (Arabic or English).
"""

client = genai.Client(api_key=settings.GEMINI_API_KEY)


@csrf_exempt
@require_POST
def chat_api(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request"}, status=400)

    user_message = body.get("message", "").strip()
    if not user_message:
        return JsonResponse({"error": "Empty message"}, status=400)

    # Automatic function calling: passing raw Python functions as `tools`
    # makes the SDK call them itself whenever the model requests it — no
    # manual tool-execution loop needed.
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=CHATBOT_TOOLS,
        ),
    )

    final_text = response.text or "Sorry, I couldn't generate a response."

    return JsonResponse({"reply": final_text})