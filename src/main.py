"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def run_profile(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top-k recommendations for a named user profile."""
    print(f"\n{'=' * 52}")
    print(f"  Profile: {label}")
    print(f"  Prefs  : {user_prefs}")
    print(f"{'=' * 52}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{i}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # ── Standard profiles ────────────────────────────────────────────────────
    profiles = [
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.9},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.35},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.95},
        ),
    ]

    # ── Adversarial / edge-case profiles ─────────────────────────────────────
    # These are designed to expose blind spots in the scoring logic:
    #
    # 1. Conflicting vibes
    #
    # 2. Unknown genre
    #
    # 3. Extreme low energy
    #
    # 4. Exact mid-point energy
    adversarial_profiles = [
        (
            "Conflicting Vibes (high-energy + melancholic mood)",
            {"genre": "pop", "mood": "melancholic", "energy": 0.9},
        ),
        (
            "Unknown Genre (classical — not in catalog)",
            {"genre": "classical", "mood": "relaxed", "energy": 0.5},
        ),
        (
            "Extreme Low Energy (energy=0.0, upbeat mood)",
            {"genre": "ambient", "mood": "upbeat", "energy": 0.0},
        ),
        (
            "Mid-Point Energy Tie-Breaker (energy=0.5)",
            {"genre": "jazz", "mood": "soulful", "energy": 0.5},
        ),
    ]

    for label, prefs in profiles + adversarial_profiles:
        run_profile(label, prefs, songs)


if __name__ == "__main__":
    main()
