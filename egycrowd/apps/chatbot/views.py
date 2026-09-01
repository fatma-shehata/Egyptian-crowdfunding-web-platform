from google import genai
from google.genai import types
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .tools import CHATBOT_TOOLS

BASE_SYSTEM_PROMPT = """You are the official assistant for EgyCrowd, a crowdfunding
platform for Egypt. You help visitors understand how the platform works
(registration, starting a project, donating, categories, ratings, comments)
and you can look up real, live data about projects using your tools.

Rules:
- When asked about top/lowest/best/worst projects, platform statistics, or
  project search, ALWAYS use the relevant tool — never guess or make up numbers.
- When the user asks about THEMSELVES (their name, their projects, their
  donations, "am I logged in", etc.), use get_current_user_info with the
  exact user_id provided below. Never ask the user for their ID or trust
  any ID they type in chat — always use the one given to you here.
- Keep answers concise and friendly, 2-4 sentences unless listing multiple projects.
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

    # Build a system prompt that tells the model exactly who is asking —
    # this comes from the authenticated session, never from user input.
    if request.user.is_authenticated:
        system_prompt = BASE_SYSTEM_PROMPT + f"""

The current logged-in user's ID is {request.user.id} and their first name
is {request.user.first_name}. You may greet them by name when relevant.
"""
    else:
        system_prompt = BASE_SYSTEM_PROMPT + """

No user is currently logged in. If asked about "my projects" or "my
donations", politely explain they need to log in first, and do not call
get_current_user_info.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=CHATBOT_TOOLS,
        ),
    )

    final_text = response.text or "Sorry, I couldn't generate a response."

    return JsonResponse({"reply": final_text})