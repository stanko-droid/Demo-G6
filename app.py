from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    jokes = [
        "Varför var matematikboken ledsen? Den hade för många problem.",
        "Vad sa den ena väggen till den andra? Vi ses vid hörnet!",
        "Vilket djur är bäst på att smyga? Mysk-oxen.",
        "Hur vet man att en bil är från Tyskland? Det hörs på lacken!",
        "Det var en gång två bagare och en smet.",
        "Vilken ört läker sår bäst? Timjan.",
        "Vad kallas en överviktig hund? En rundgång.",
        "Varför har inte orienterare några barn? De springer bara runt i buskarna.",
        "Vad sa göteborgaren till den döda fisken? Det var ett jävla liv på dig.",
        "Hur ser man att en dykare är gift? Man ser det på ringarna på vattnet.",
        "Vilken hund är bäst på att trolla? Labra-dabra-dor.",
        "Vad gör en arbetslös skådespelare? Spelar ingen roll.",
        "Vilket land har de sämsta bilarna? Bak-u.",
        "Varför är det svårt att spela kort i djungeln? Det finns för många leoparder.",
        "Vad heter tysklands sämsta bärplockare? Han som hittar-inte.",
        "Vad kallas en kvinna som vet var hennes man är hela tiden? En änka.",
        "Vem är bäst på att tvätta i djungeln? Gor-illa.",
        "Vad sa kaffekoppen till den andra kaffekoppen? Är det bön-söndag idag?",
        "Vilket djur ser sämst? Allt-i-gatorn.",
        "Vad heter världens fattigaste kung? Kung-kurs."
    ]
    return render_template('index.html', version='G6-SLAY-ULTIMATE', jokes=jokes)

if __name__ == '__main__':
    app.run(debug=True)