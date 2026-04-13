from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV of songs and return a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences (+2 genre, +2 mood, +1 energy proximity) and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 2.0
        reasons.append(f"mood match (+2.0)")

    # Energy proximity (0–1 range; closer to target = higher bonus)
    if "energy" in user_prefs:
        energy_bonus = round(1.0 - abs(user_prefs["energy"] - song["energy"]), 3)
        score += energy_bonus
        reasons.append(f"energy proximity (+{energy_bonus})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song with score_song, then return the top-k results sorted highest to lowest."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))

    # sorted() is non-destructive — it creates and returns a brand-new list
    # ranked from highest score to lowest without touching `scored`.
    top_k = sorted(scored, key=lambda x: x[1], reverse=True)[:k]
    return top_k
