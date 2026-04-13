# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.


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

![Terminal output showing top recommendations for the pop/happy profile](Screenshot%202026-04-13%20104536.png)

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

