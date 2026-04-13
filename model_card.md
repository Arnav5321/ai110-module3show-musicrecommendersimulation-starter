# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Bard

---

## 2. Intended Use  

Bard suggests up to 5 songs from an 18-track catalog based on a user's preferred genre, mood, and energy level. It assumes the user can describe their taste with a single genre label, a mood word, and a target energy value between 0 and 1. Built for classroom exploration only — not intended for real users or production use.

---

## 3. How the Model Works  

Every song gets a score based on how well it matches what the user asked for. If the genre matches, the song earns 2 points. If the mood matches, it earns another 2 points. Then the system looks at energy — a number between 0 (very calm) and 1 (very intense) — and awards up to 1 extra point based on how close the song's energy is to the user's target. Songs are ranked by their total score and the top 5 are returned, each with a plain-English explanation of why it was chosen.

---

## 4. Data  

The catalog contains 18 songs across 13 genres (pop, lofi, rock, ambient, jazz, folk, blues, metal, world, cinematic, reggae, house, hip hop) and 11 moods. No songs were added or removed from the starter CSV. The dataset skews toward calm, introspective styles — lofi has 3 entries while genres like rock, metal, and reggae have only one each. High-energy dance or Latin genres are entirely absent, meaning users with those tastes will only ever see energy-proximity results with no genre match.

---

## 5. Strengths  

- Works well when a user's taste aligns with a well-represented catalog segment (e.g. Chill Lofi scored a perfect 5.00).
- Every recommendation comes with a plain-English reason, making the logic fully transparent and easy to audit.
- Simple enough that unexpected results are easy to diagnose — there are no hidden layers or learned weights.

---

## 6. Limitations and Bias 

- **Genre filter bubble:** matching is exact, so "indie pop" never counts as "pop," even if it sounds identical.
- **Catalog coverage bias:** genres with only one or two entries (rock, pop) give thin results compared to well-represented ones (lofi).
- **Energy always scores something:** even a poor energy match contributes points, making it an invisible tiebreaker that can override mood or genre signals.
- **No diversity penalty:** the system can return multiple songs by the same artist if their numbers align.

---

## 7. Evaluation  

5 profiles were tested: two standard (High-Energy Pop, Chill Lofi) and three adversarial (Conflicting Vibes, Unknown Genre, Mid-Point Energy).

Standard profiles mostly matched expectations. Chill Lofi was the clearest win — Library Rain scored a perfect 5.00 on all three signals. The biggest surprise was the **Conflicting Vibes** profile: `Gym Hero` ranked #1 for a user who wanted melancholic pop, because its genre and energy scores outweighed the mood mismatch. The system has no way to know a gym-workout song is the wrong emotional fit.

The **Unknown Genre** (classical) profile showed how fragile the rankings become with no genre bonus — the #2 through #5 slots were separated by fractions of a point and felt nearly arbitrary.

---

## 8. Future Work  

- Add a diversity penalty so the same artist cannot appear more than once in the top 5.
- Include valence and tempo proximity as additional scoring signals to better capture emotional fit.
- Use fuzzy genre matching (e.g. "indie pop" counts partially as "pop") to reduce the filter bubble.
- Support multiple mood preferences so a user can say "happy or chill" instead of just one word.

---

## 9. Personal Reflection  

The most surprising thing was how much the catalog's genre tags controlled the output, not the scoring math. A song tagged "indie pop" is permanently invisible to a "pop" user no matter how good a fit it is. That made me realize that in real apps like Spotify, the people who decide how to label a song are quietly shaping every recommendation downstream, even if no engineer ever intended that. 
