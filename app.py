import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PHRASES = {
    "привет": ["Йо, братуха! 😎", "Здарова, кореш! 💀"],
    "погода": ["На улице +2, одевай шапку 💀", "Дождь льёт, не залипай 😏"],
    "шутка": ["Два пацана заходят в бар... 💀", "Смешно или нет, мне всё равно 🤯"]
}

EXTRAS = ["💀","😳","😏","🤯","🫵","🤬","💪","😎"]

def detect_category(text):
    text = text.lower()
    if any(w in text for w in ["привет","йо"]): return "привет"
    if any(w in text for w in ["погода","солнце","дождь"]): return "погода"
    if any(w in text for w in ["шутка","анекдот"]): return "шутка"
    return "привет"

def generate_ai_response(text):
    # Пример с OpenAI API
    API_KEY = "ТВОЙ_API_KEY"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    prompt = f"Алиса-гопник, отвечает на текст: {text}. Шутки, мат, сарказм, эмодзи."
    data = {"model":"gpt-3.5-turbo","messages":[{"role":"user","content":prompt}], "max_tokens":50}
    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    else:
        return random.choice(PHRASES["привет"])

@app.route("/", methods=["POST"])
def main():
    user_text = request.json.get("request", {}).get("original_utterance", "")
    category = detect_category(user_text)

    if random.random() < 0.5:
        phrase = random.choice(PHRASES[category])
    else:
        phrase = generate_ai_response(user_text)

    if random.random() < 0.3:
        phrase += " " + random.choice(EXTRAS)

    return jsonify({"response":{"text":phrase,"end_session":False},"version":"1.0"})

if __name__ == "__main__":
    app.run()
