import os
import time
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# Ekta busy thakle onnotay jabe
MODELS_TO_TRY = [
    "gemini-3.8-flash",
    "gemini-3.8-pro",
    "gemini-2.5-pro"
]

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    user_prompt = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")
        if client and user_prompt:
            success = False
            last_err = ""
            for m in MODELS_TO_TRY:
                for _ in range(2):
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=user_prompt
                        )
                        ai_response = response.text
                        success = True
                        break
                    except Exception as e:
                        last_err = str(e)
                        time.sleep(1)
                if success:
                    break
            if not success:
                ai_response = f"Models are temporarily overloaded. Please try again. Details: {last_err}"
        elif not client:
            ai_response = "API Key not configured properly."

    return render_template("index.html", response=ai_response, prompt=user_prompt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)