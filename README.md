# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Vibe-o-tron 1.0 scores 16 songs against a user's genre, mood, and energy preferences and returns the top 5 with their reasons for selection.

---

## How The System Works

**Real-world recommenders:** Collaborative filtering recommends songs based on what users with similar listening habits liked, using other users' information to shape recommendations. This project only uses content-based filtering on song attributes, prioritizing genre first, then mood, then energy closeness.

**Song features used:** `genre`, `mood`, `energy` (0–1), `acousticness` (0–1). The CSV also has `tempo_bpm`, `valence`, and `danceability`, but they are not scored yet.

**UserProfile fields:** `favorite_genre`, `favorite_mood`, `target_energy` (0–1), `likes_acoustic` (bool).

**Algorithm Recipe (scoring rule, one song):**

| Rule | Points |
|---|---|
| Genre matches `favorite_genre` | +2.0 |
| Mood matches `favorite_mood` | +1.0 |
| Energy closeness: `1 - abs(song.energy - target_energy)` | 0.0 – 1.0 |
| `likes_acoustic` is true and `acousticness > 0.6` | +0.5 |

Max possible score = 4.5. Each rule that fires adds a "reason" string so the result is explainable.

**Ranking rule (all songs):** score every song in the catalog, sort highest → lowest, return the top `k`.

**Data flow:** User prefs → loop: `score_song` on every row of `songs.csv` → sort by score → top K with reasons.

**Expected bias:** Genre (2.0) outweighs the maximum energy bonus (1.0), so a same-genre song with the wrong energy will beat a perfect-energy song from another genre. Exact string matching also means "indie pop" gets no credit for a "pop" fan. The catalog leans lofi/chill, so chill users get more choices than others.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Default profile: `{"genre": "pop", "mood": "happy", "energy": 0.8}`

```
Loaded songs: 16

Top recommendations:

Sunrise City - Score: 3.98
Because: Matches favorite genre +2.0, Matches favorite mood +1.0, Energy similarity +0.98

Gym Hero - Score: 2.87
Because: Matches favorite genre +2.0, Energy similarity +0.87

Rooftop Lights - Score: 1.96
Because: Matches favorite mood +1.0, Energy similarity +0.96

Concrete Crown - Score: 0.98
Because: Energy similarity +0.98

Night Drive Loop - Score: 0.95
Because: Energy similarity +0.95
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

When the genre weight was changed from 2.0 to 1.0 and the energy weight was doubled, the Conflicted profile's entire top three changed; Moonlit Sonata dropped out of the top 5 and high-energy songs took its place. For High-Energy Pop, Rooftop Lights nearly passed Gym Hero (2.82 vs. 2.84), while the Chill Lofi and Deep Intense Rock top threes did not change at all. The system is generally accurate, but some user profiles intrinsically have overlap between different genres, which stresses the algorithm. I reverted to the original weights afterward.

---

## Limitations and Risks

The catalog is small (16 songs) and uneven, with lofi and chill overrepresented, so users with common tastes get far more relevant matches than a country or classical listener, who has only one song that can earn the genre bonus. Additionally, tempo, valence, and danceability are loaded but never scored, so the system cannot tell a sad song from a happy one unless their mood labels match exactly.

---

## Reflection

[**Model Card**](model_card.md)

The most important thing I learned is that a recommender turns data into predictions through a scoring rule that is ultimately a design decision, and that decision has to be verified with evidence rather than trusted because the output looks reasonable. Vibe-o-tron weights a genre match at 2.0 points, a mood match at 1.0, and energy closeness at up to 1.0, and for the standard profiles, such as Chill Lofi and Deep Intense Rock, the top results matched my intuition almost exactly. However, when I halved the genre weight and doubled energy, the edge-case profile's entire top three changed while the others barely moved, which showed that these essentially arbitrary weights were quietly determining every result.

Bias showed up most clearly in the edge-case profile, which asked for classical music with a sad mood and 0.9 energy. Moonlit Sonata ranked first despite having an energy of 0.22 – nearly the opposite of what the user asked for – simply because it was the only classical song and the genre weight outweighed everything else. Thus, a system that ranks or scores data embeds assumptions that only surface under testing, and users whose tastes fall outside the most common or most heavily weighted categories are the ones most likely to receive poor recommendations.