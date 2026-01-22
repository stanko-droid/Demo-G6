from flask import Flask, render_template  # <-- Viktigt: Glöm inte importera render_template!

app = Flask(__name__)

# --- HÄR ÄR DEN SAMMANSLAGNA LÖSNINGEN ---
@app.route('/')
def home():
    # Vi renderar HTML-filen OCH skickar med versionsnumret
    return render_template('index.html', version='1.0.0')

if __name__ == '__main__':
    app.run(debug=True)