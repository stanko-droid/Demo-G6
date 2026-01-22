from flask import Flask

app = Flask(__name__)


# --- USER STORY 1 LÖSNING ---
@app.route("/")
def hello():
    # Här är ändringen som User Storyn krävde:
    return "<h1>Welcome to G6! 🚀</h1>"


if __name__ == '__main__':
    app.run(debug=True)
