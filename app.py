import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def get_valid_models(client):
    models_to_try = []
    try:
        models_data = client.models.list()
        for m in models_data.data:
            mid = m.id.lower()
            # terms require kora, audio, vision ebong purono decommissioned bad
            if any(x in mid for x in ["orpheus", "canopy", "whisper", "vision", "mixtral", "llama3-8b"]):
                continue
            models_to_try.append(m.id)
    except Exception:
        pass
    return models_to_try

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    user_prompt = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")
        if client and user_prompt:
            valid_models = get_valid_models(client)
            success = False
            last_err = ""
            for m in valid_models:
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": user_prompt}],
                        model=m,
                    )
                    ai_response = chat_completion.choices[0].message.content
                    success = True
                    break
                except Exception as e:
                    last_err = str(e)
                    continue

            if not success:
                ai_response = f"Could not find an active model. Error: {last_err}"
        elif not client:
            ai_response = "API Key not configured properly."

    return render_template("index.html", response=ai_response, prompt=user_prompt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)