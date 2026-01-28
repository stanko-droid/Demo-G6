"""
Joke repository - handles data access for jokes.
"""


class JokeRepository:
    """Repository for joke data access."""

    def __init__(self):
        """Initialize the joke repository with default jokes."""
        self._jokes = [
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

    def get_all_jokes(self) -> list[str]:
        """Get all jokes."""
        return self._jokes

    def get_random_joke(self):
        """Get a random joke."""
        import random
        return random.choice(self._jokes) if self._jokes else "Inga skämt tillgängliga"

    def get_joke_by_index(self, index: int) -> str | None:
        """Get a specific joke by index."""
        if 0 <= index < len(self._jokes):
            return self._jokes[index]
        return None

    def get_joke_count(self) -> int:
        """Get the total number of jokes."""
        return len(self._jokes)
