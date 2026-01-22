from flask import Flask, render_template
import random  # <--- Vi behöver denna för skämten

app = Flask(__name__)

@app.route('/')
def home():
    # 1. Lista med skämt
    jokes = [
        "Varför var matematikboken ledsen? Den hade för många problem.",
        "Vad sa den ena väggen till den andra? Vi ses vid hörnet!",
        "Vilket djur är bäst på att smyga? Mysk-oxen.",
        "Hur vet man att en bil är från Tyskland? Det hörs på lacken!",
        "Det var en gång två bagare och en smet."
    ]
    
    # 2. Välj ett slumpmässigt skämt
    selected_joke = random.choice(jokes)

    # 3. Skicka skämtet OCH versionen till HTML
    return render_template('index.html', version='1.0.0', joke=selected_joke)

if __name__ == '__main__':
    app.run(debug=True)