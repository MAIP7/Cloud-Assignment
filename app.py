import os
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    user_prompt = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")
        if client and user_prompt:
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": user_prompt,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                ai_response = chat_completion.choices[0].message.content
            except Exception as e:
                ai_response = f"Error: {str(e)}"
        elif not client:
            ai_response = "API Key not configured properly."

    return render_template("index.html", response=ai_response, prompt=user_prompt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)