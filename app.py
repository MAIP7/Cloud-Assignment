import os
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Environment variable theke API Key nibe
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    user_prompt = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")
        if client and user_prompt:
            try:
                response = client.models.generate_content(
                  model="gemini-2.0-flash",
                    contents=user_prompt
                )
                ai_response = response.text
            except Exception as e:
                ai_response = f"Error: {str(e)}"
        elif not client:
            ai_response = "API Key not configured properly."

    return render_template("index.html", response=ai_response, prompt=user_prompt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)