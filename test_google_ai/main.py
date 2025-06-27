import os
import sys
import traceback

from google import genai
from google.genai import types


try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        contents=sys.argv[1],
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0))
    )
    print(response.text)

except Exception:
    traceback.print_exc()
    sys.exit(1)
