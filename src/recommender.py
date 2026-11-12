import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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
        """Return the top k Song objects ranked by score_song."""
        prefs = _profile_to_prefs(user)
        return sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable string of the reasons a song was scored the way it was."""
        score, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + ", ".join(reasons)


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the user_prefs dict format used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


NUMERIC_FIELDS = {"id": int, "energy": float, "tempo_bpm": float, "valence": float,
                  "danceability": float, "acousticness": float}


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV into a list of dicts, converting numeric columns."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        songs = []
        for row in csv.DictReader(f):
            for field, cast in NUMERIC_FIELDS.items():
                row[field] = cast(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    score = 0.0
    reasons = []
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("Matches favorite genre +2.0")
    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("Matches favorite mood +1.0")
    sim = 1 - abs(song["energy"] - user_prefs["energy"])
    score += sim
    reasons.append(f"Energy similarity +{sim:.2f}")
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("Likes acoustic +0.5")
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
