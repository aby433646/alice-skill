from flask import Flask, request, jsonify
import random

app = Flask(__name__)

PHRASES = [
    "Ну это, конечно, капец полный",
    "Ага, очень смешно, брат",
    "Вот это поворот",
    "Ну ты даёшь, конечно"
]

@app.route("/", methods=["POST"])
def main():
    phrase = random.choice(PHRASES)

    return jsonify({
        "response": {
            "text": phrase,
            "end_session": False
        },
        "version": "1.0"
    })

if __name__ == "__main__":
    app.run()
