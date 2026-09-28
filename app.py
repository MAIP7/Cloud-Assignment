import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# Terms chhara standard free models
MODELS_TO_TRY = [
    "gemma2-9b-it",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768"
]

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    user_prompt = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")
        if client and user_prompt:
            success = False
            last_error = ""
            for m in MODELS_TO_TRY:
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": user_prompt,
                            }
                        ],
                        model=m,
                    )
                    ai_response = chat_completion.choices[0].message.content
                    success = True
                    break
                except Exception as e:
                    last_error = str(e)
                    continue

            if not success:
                ai_response = f"Error: {last_error}"
        elif not client:
            ai_response = "API Key not configured properly."

    return render_template("index.html", response=ai_response, prompt=user_prompt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)