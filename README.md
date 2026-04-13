# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version scores every song in an 18-track CSV catalog against a user taste profile (genre, mood, energy) and returns the top 5 matches with a plain-English reason for each pick.


---

## How The System Works

This recommender uses a content-based approach to match songs to user preferences by scoring each song based on how well it aligns with the user's "taste profile." It prioritizes simplicity and transparency, focusing on key vibe features without complex algorithms or external data.

### Song Features Used
Each song is represented by:
- Genre (categorical, e.g., pop, rock, lofi)
- Mood (categorical, e.g., happy, chill, intense)
- Energy (numerical, 0-1 scale for intensity)
- Valence (numerical, 0-1 scale for positivity)
- Tempo (BPM) (numerical, beats per minute)
- Acousticness (numerical, 0-1 scale for acoustic elements)

### User Profile Information
The user profile stores:
- Favorite Genre (categorical)
- Favorite Mood (categorical)
- Target Energy (numerical, 0-1)
- Target Valence (numerical, 0-1)
- Target Tempo Range (numerical, min-max BPM)
- Likes Acoustic (boolean, preference for acoustic sounds)

### Scoring Algorithm Recipe
For each song, the system computes a score by adding points for matches and similarities:

- +2.0 points for an exact genre match
- +1.0 point for an exact mood match
- +1.0 * (1 - |song.energy - target_energy|)** for energy closeness (closer = higher score)
- +1.0 * (1 - |song.valence - target_valence|)** for valence closeness
- +1.0 if tempo is within the target range, otherwise +max(0, 1.0 - distance/40) (soft penalty for out-of-range tempo)
- +0.8 if user likes acoustic and song.acousticness >= 0.5, or -0.2 if user dislikes acoustic but song is highly acoustic

### Recommendation Process
1. Load all songs from the CSV file.
2. For each song, compute the score using the above recipe.
3. Rank songs by descending score.
4. Return the top K songs (default 5) as recommendations.

### Potential Biases
This system might over-prioritize genre matches, potentially ignoring great songs that match the user's mood or energy but belong to a different genre. It could also favor songs with moderate numeric values, creating a bias toward "average" tracks and underrepresenting extreme vibes like very high-energy or very low-valence songs.

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

## Sample Output

### Original baseline (pop / happy)
![Terminal output showing top recommendations for the pop/happy profile](Screenshot%202026-04-13%20104536.png)

### Standard profiles

**High-Energy Pop**
![High-Energy Pop recommendations](Screenshot%202026-04-13%20105851.png)

**Chill Lofi**
![Chill Lofi recommendations](Screenshot%202026-04-13%20105857.png)

**Conflicting Vibes**
![Conflicting Vibes recommendations](Screenshot%202026-04-13%20105910.png)

### Adversarial / edge-case profiles

**Unknown Genre**
![Unknown Genre recommendations](Screenshot%202026-04-13%20105917.png)

**Mid-Point Energy Tie-Breaker**
![Mid-Point Energy recommendations](Screenshot%202026-04-13%20105927.png)

---

## Experiments You Tried

### Experiment — Weight Shift: halve genre, double energy

**Change:** genre bonus `2.0 → 1.0`, energy multiplier `1.0 → 2.0` (proximity range becomes `[0, 2]`).

**What changed in the rankings:**

- **High-Energy Pop:** `Rooftop Lights` jumped from #3 to #2, leapfrogging `Gym Hero`. It has no genre match, but its energy (0.76) is closer to the target (0.9) than Gym Hero's (0.93). With energy worth twice as much, that proximity gap flipped the order.
- **Chill Lofi:** `Spacewalk Thoughts` moved from #4 to #3, ahead of `Focus Flow`. Spacewalk matches the mood ("chill") and has a better energy fit; previously the genre bonus kept Focus Flow ahead.
- **Conflicting Vibes (adversarial):** The rank order inverted — `Golden Plains` (folk/melancholic) jumped to #1 over the pop genre matches. Because the mood bonus is unchanged at +2.0 and genre is now only worth +1.0, the single mood hit outweighs the genre label entirely.

**Conclusion:** Doubling energy made the results feel more "vibe-accurate" for standard profiles — songs that actually match the user's intensity level rank higher regardless of genre label. However, it amplified the adversarial flaw: when genre is weak, mood alone can dominate and pull in songs from completely different genres.

---

## Limitations and Risks

- Works on a catalog of 18 songs — results are not meaningful at real scale
- Genre matching is exact, so "indie pop" never counts as "pop"
- Does not understand lyrics, language, or actual audio content
- No diversity control — the same artist can appear multiple times in the top 5

---

## Reflection

[**Model Card**](model_card.md)

Building this showed how much a recommender's output is shaped by its data labels, not just its logic. The genre filter bubble where "indie pop" can never match "pop"  revealed that the catalog's tagging choices quietly control results as much as the user's preferences do. Real recommenders hide this problem with a wall of data, but the core tension is identical: the model can only work with the signals it was given, and those signals always carry someone's assumptions about how music should be categorized.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> Bard

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Bard suggests up to 5 songs from an 18-track catalog based on a user's preferred genre, mood, and energy level. This is not intended for real users or production use.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

Every song in the catalog gets a score based on how well it matches what the user asked for. If the song's genre matches, it earns 2 points. If the mood matches, it earns another 2 points. Then the system looks at energy — a number between 0 (very calm) and 1 (very intense) — and awards up to 1 extra point based on how close the song's energy is to the user's target. Songs are ranked by total score and the top 5 are returned, each with a reason explaining why it was chosen.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

The catalog contains 18 songs across 13 genres (pop, lofi, rock, ambient, jazz, folk, blues, metal, world, cinematic, reggae, house, hip hop) and 11 moods. No songs were added or removed from the starter CSV. The dataset skews toward calm, introspective styles — lofi has 3 entries while rock, metal, and reggae each have only one. High-energy dance and Latin genres are entirely absent, so users with those tastes will never see a genre bonus.

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

Best results when the user's taste matches a well-represented genre — Chill Lofi scored a perfect 500.
Every result includes a plain-English reason, making the logic fully transparent.

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

Exact genre matching means "indie pop" never counts as "pop."
Underrepresented genres (rock, pop) produce thin results compared to lofi.
Energy always scores something, quietly overriding stronger signals in close races.
No diversity control — the same artist can fill multiple top-5 slots.

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

Tested 5 profiles: High-Energy Pop, Chill Lofi, Conflicting Vibes, Unknown Genre, and Mid-Point Energy. Chill Lofi was the clearest win (perfect 5.00). The biggest surprise: Gym Hero ranked #1 for a melancholic pop user because genre and energy outweighed the wrong mood. When no genre bonus was available (Unknown Genre), the bottom 4 slots were nearly arbitrary.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

Diversity penalty so the same artist can't appear twice.
Add valence and tempo as scoring signals.
Fuzzy genre matching so "indie pop" partially counts as "pop."

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

The most surprising thing was how much the catalog's genre tags controlled the output, not the scoring math. A song tagged "indie pop" is permanently invisible to a "pop" user no matter how good a fit it is. That made me realize that in real apps like Spotify, the people who decide how to label a song are quietly shaping every recommendation downstream, even if no engineer ever intended that. 
