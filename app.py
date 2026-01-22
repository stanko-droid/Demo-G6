from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def home():
    jokes = [
        "Varför var matematikboken ledsen? Den hade för många problem.",
        "Vad sa den ena väggen till den andra? Vi ses vid hörnet!",
        "Vilket djur är bäst på att smyga? Mysk-oxen.",
        "Hur vet man att en bil är från Tyskland? Det hörs på lacken!",
        "Det var en gång två bagare och en smet."
    ]
    selected_joke = random.choice(jokes)
    return render_template('index.html', version='1.0.0', joke=selected_joke)

if __name__ == '__main__':
    app.run(debug=True)