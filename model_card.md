# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Vibe-o-tron 1.0**  

---

## 2. Intended Use  

Vibe-o-tron 1.0 recommends songs from a small catalog by scoring each song against a user's genre, mood, and energy preferences, then returning the top five. Notably, the profiles themselves make assumptions about the user – specifically, that their taste can be summarized by a single favorite genre, a single favorite mood, and one target energy level, which is rarely true of real listeners. As a result, this system is intended for classroom exploration of how recommenders turn data into rankings, not for real users.

---

## 3. How the Model Works  

Each song is compared against the user's profile on four features: genre, mood, energy, and whether the user likes acoustic music. A matching genre earns 2.0 points and a matching mood earns 1.0 point. Energy is handled differently, since it is a number between 0 and 1 rather than a label; the closer a song's energy is to the user's target, the more points it earns, up to a maximum of 1.0. For example, a user targeting 0.8 energy would receive 0.98 points from a song at 0.82, but only 0.42 from a song at 0.22. Finally, if the user likes acoustic music and the song's acousticness is above 0.6, it earns an additional 0.5 points. These points are summed into a single score, and every song in the catalog is then sorted from highest to lowest so that the top five can be returned, each with a list of reasons explaining where its points came from.

### Changes from the starter logic

The starter code simply returned the first five songs in the catalog with a placeholder explanation, so the scoring and ranking were written from scratch. Additionally, the starter profile in `main.py` did not include a `likes_acoustic` preference, so the scoring treats that preference as optional rather than crashing when it is missing. I also tested halving the genre weight and doubling the energy weight (see Evaluation), but ultimately reverted to the original weights.

---

## 4. Data  

The catalog contains 16 songs: the 10 provided with the starter project and 6 that I added to cover genres and moods the original set was missing – hip-hop, metal, classical, country, R&B, and a sad indie track. Each song has a genre, mood, energy, tempo, valence, danceability, and acousticness value, although only genre, mood, energy, and acousticness are used for scoring. Despite the additions, the catalog is still uneven; lofi has three songs and the chill mood appears three times, while most other genres are represented by a single song. Thus, a lofi listener has more possible matches than, say, a country listener, who has exactly one. Arguably the largest gap is that the data contains nothing about listening history, lyrics, or language, which are central to how real platforms build a sense of taste.

---

## 5. Strengths  

The system performs best when a user's preferences agree with each other. The Chill Lofi and Deep Intense Rock profiles both returned top results that matched my intuition – Library Rain and Midnight Coding for lofi, Storm Runner for rock – since those songs matched on genre, mood, and energy simultaneously. Going into testing, I assumed some songs would overlap profiles despite differing genres, and this held up; Gym Hero, a pop song, ranked second for the rock profile because its intense mood and high energy carried it past the genre mismatch. That being said, I would consider this a reasonable result rather than a flaw, since a rock listener could plausibly enjoy a high-energy, intense pop track. Additionally, because every score comes with a list of reasons, it is straightforward to see exactly why each song was recommended.

---

## 6. Limitations and Bias 

The scoring does not use every feature available in `songs.csv`; tempo, valence, and danceability are loaded for each song but never factor into the score. As a result, the system cannot distinguish a sad song from a happy one unless their mood labels match exactly, even though valence is effectively a numeric measure of exactly that. Additionally, the catalog overrepresents lofi and chill music – three of the sixteen songs are lofi and three are chill, while most other genres appear only once. Thus, the Chill Lofi profile received a top three that matched on nearly every rule, whereas a country or classical listener has a single song that can ever earn the genre bonus, with the rest of their list filled by energy alone. This creates a filter bubble that favors users whose taste happens to match the most common music in the dataset, and arguably keeps those same users from discovering anything outside of it.

---

## 7. Evaluation  

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and a deliberately conflicting edge case that asks for classical music with a sad mood and 0.9 energy – a combination no song in the catalog satisfies. For each profile, I checked whether the top five matched my own intuition and verified several of the scores by hand against the recipe. I then ran one experiment, halving the genre weight and doubling the energy weight, to see how sensitive the rankings were.

What surprised me most was the variance in the scores of the best matches. The top Chill Lofi song scored 4.50, the maximum possible, while the top song for the edge case scored only 2.32, and the fifth-place songs for most profiles scored below 1.0. Notably, a score below 1.0 means the song matched on nothing but energy, so the bottom of each list is effectively filler rather than a real recommendation. The system has no way of saying "nothing here fits you well"; it simply returns the five least-bad options.

### Profile comparisons

- **High-Energy Pop vs. Chill Lofi:** The pop profile favors upbeat, high-energy songs, while the lofi profile shifts toward quiet, acoustic tracks, and the two lists share no songs at all. This makes sense, since the profiles sit on opposite ends of the energy scale and only the lofi profile earns the acoustic bonus.
- **High-Energy Pop vs. Deep Intense Rock:** Gym Hero ranks second in both lists, but for different reasons – for pop it wins on genre, and for rock it wins on mood. To put it plainly for a non-programmer, Gym Hero shows up for "Happy Pop" listeners because it is labeled pop and is high energy, even though its mood is intense rather than happy; the genre label alone is worth more points than a happy mood and a close energy level combined.
- **High-Energy Pop vs. Conflicted:** Every song in the pop top three earns at least one label match and a strong energy score, whereas the conflicted profile's winner, Moonlit Sonata, scores only 0.32 on energy. It ranks first purely because it is the only classical song, which shows that the genre label can outweigh everything else.
- **Chill Lofi vs. Deep Intense Rock:** These lists are effectively mirror images; the lofi list is entirely low-energy and acoustic, while the rock list is entirely high-energy. This is coincident with the energy targets of 0.35 and 0.90, which pull each profile toward opposite halves of the catalog.
- **Chill Lofi vs. Conflicted:** Both profiles ask for a quieter genre or mood, but the conflicted profile also asks for high energy. As a result, the lofi list is consistent from top to bottom, while the conflicted list contradicts itself – its top two are slow and quiet, and its bottom three are rock, pop, and metal.
- **Deep Intense Rock vs. Conflicted:** Ranks three through five of the conflicted profile (Storm Runner, Gym Hero, Iron Cathedral) are essentially the rock profile's high-energy songs. Since both profiles target roughly 0.9 energy, once the label matches run out, the two profiles converge on the same songs.

### Weight experiment

Halving the genre weight and doubling the energy weight had the largest effect on the edge case, where Moonlit Sonata dropped out of the top five entirely and high-energy songs took the top three spots. For High-Energy Pop, Rooftop Lights (happy, indie pop) nearly caught Gym Hero, closing the gap from 0.96 to 0.02. However, the Chill Lofi and Rock top threes did not change at all, since their preferences already agreed with each other. Therefore, the change made the results more accurate for conflicting profiles but not universally better – energy then dominated the bottom of every list, filling it with songs from any genre that happened to share an energy level. I reverted to the original weights afterward.

### Test output: baseline weights (genre +2.0, mood +1.0, energy 0–1, acoustic +0.5)

```
Top recommendations for profile 'High-Energy Pop':

Sunrise City - Score: 3.97
Because: Matches favorite genre +2.0, Matches favorite mood +1.0, Energy similarity +0.97

Gym Hero - Score: 2.92
Because: Matches favorite genre +2.0, Energy similarity +0.92

Rooftop Lights - Score: 1.91
Because: Matches favorite mood +1.0, Energy similarity +0.91

Storm Runner - Score: 0.94
Because: Energy similarity +0.94

Concrete Crown - Score: 0.93
Because: Energy similarity +0.93


Top recommendations for profile 'Chill Lofi':

Library Rain - Score: 4.50
Because: Matches favorite genre +2.0, Matches favorite mood +1.0, Energy similarity +1.00, Likes acoustic +0.5

Midnight Coding - Score: 4.43
Because: Matches favorite genre +2.0, Matches favorite mood +1.0, Energy similarity +0.93, Likes acoustic +0.5

Focus Flow - Score: 3.45
Because: Matches favorite genre +2.0, Energy similarity +0.95, Likes acoustic +0.5

Spacewalk Thoughts - Score: 2.43
Because: Matches favorite mood +1.0, Energy similarity +0.93, Likes acoustic +0.5

Coffee Shop Stories - Score: 1.48
Because: Energy similarity +0.98, Likes acoustic +0.5


Top recommendations for profile 'Deep Intense Rock':

Storm Runner - Score: 3.99
Because: Matches favorite genre +2.0, Matches favorite mood +1.0, Energy similarity +0.99

Gym Hero - Score: 1.97
Because: Matches favorite mood +1.0, Energy similarity +0.97

Iron Cathedral - Score: 0.93
Because: Energy similarity +0.93

Sunrise City - Score: 0.92
Because: Energy similarity +0.92

Concrete Crown - Score: 0.88
Because: Energy similarity +0.88


Top recommendations for profile 'Conflicted (edge)':

Moonlit Sonata No. 3 - Score: 2.32
Because: Matches favorite genre +2.0, Energy similarity +0.32

Empty Platform - Score: 1.43
Because: Matches favorite mood +1.0, Energy similarity +0.43

Storm Runner - Score: 0.99
Because: Energy similarity +0.99

Gym Hero - Score: 0.97
Because: Energy similarity +0.97

Iron Cathedral - Score: 0.93
Because: Energy similarity +0.93
```

### Experiment: weight shift (genre 2.0 → 1.0, energy similarity ×2)

```
Top recommendations for profile 'High-Energy Pop':

Sunrise City - Score: 3.94
Because: Matches favorite genre +1.0, Matches favorite mood +1.0, Energy similarity +1.94

Gym Hero - Score: 2.84
Because: Matches favorite genre +1.0, Energy similarity +1.84

Rooftop Lights - Score: 2.82
Because: Matches favorite mood +1.0, Energy similarity +1.82

Storm Runner - Score: 1.88
Because: Energy similarity +1.88

Concrete Crown - Score: 1.86
Because: Energy similarity +1.86


Top recommendations for profile 'Chill Lofi':

Library Rain - Score: 4.50
Because: Matches favorite genre +1.0, Matches favorite mood +1.0, Energy similarity +2.00, Likes acoustic +0.5

Midnight Coding - Score: 4.36
Because: Matches favorite genre +1.0, Matches favorite mood +1.0, Energy similarity +1.86, Likes acoustic +0.5

Focus Flow - Score: 3.40
Because: Matches favorite genre +1.0, Energy similarity +1.90, Likes acoustic +0.5

Spacewalk Thoughts - Score: 3.36
Because: Matches favorite mood +1.0, Energy similarity +1.86, Likes acoustic +0.5

Coffee Shop Stories - Score: 2.46
Because: Energy similarity +1.96, Likes acoustic +0.5


Top recommendations for profile 'Deep Intense Rock':

Storm Runner - Score: 3.98
Because: Matches favorite genre +1.0, Matches favorite mood +1.0, Energy similarity +1.98

Gym Hero - Score: 2.94
Because: Matches favorite mood +1.0, Energy similarity +1.94

Iron Cathedral - Score: 1.86
Because: Energy similarity +1.86

Sunrise City - Score: 1.84
Because: Energy similarity +1.84

Concrete Crown - Score: 1.76
Because: Energy similarity +1.76


Top recommendations for profile 'Conflicted (edge)':

Storm Runner - Score: 1.98
Because: Energy similarity +1.98

Gym Hero - Score: 1.94
Because: Energy similarity +1.94

Iron Cathedral - Score: 1.86
Because: Energy similarity +1.86

Empty Platform - Score: 1.86
Because: Matches favorite mood +1.0, Energy similarity +0.86

Sunrise City - Score: 1.84
Because: Energy similarity +1.84
```

---

## 8. Future Work  

The most immediate improvement would be to use the features already present in `songs.csv` that the scoring ignores – tempo, valence, and danceability. Valence in particular could help separate a sad song from a happy one even when their mood labels do not match exactly. Next, genre matching could award partial credit for related genres, so that a pop fan receives some credit for an indie pop song rather than none. Finally, a diversity penalty that lowers a song's score if its genre or artist already appears in the top results would reduce the filter-bubble effect, where a lofi listener only ever sees lofi.

---

## 9. Personal Reflection  

My biggest takeaway is that the scoring is perhaps a bit arbitrary. The weights of 2.0 for genre and 1.0 for mood were a reasonable starting point, but nothing about them is inherently correct, and the weight experiment showed that a small change can reorder an entire list. Thus, a scoring rule needs testing to verify that the results act as expected, rather than being trusted simply because the top result looks right. The edge-case profile made this particularly clear, since a song with nearly the opposite energy of what the user asked for still ranked first.

AI tools were helpful for drafting the loading and ranking functions and for checking scores, but they still required verification on my end. For example, after I wrote the scoring function, the AI pointed out that reading `likes_acoustic` directly would crash on the default profile in `main.py`, since that profile never defines it; switching to `.get()` resolved this. That being said, I still had to decide which features to use and how to weight them, and to confirm by hand that each score matched the recipe. It was also interesting that such a simple sum of points still produces lists that feel like real recommendations – essentially, a few matching labels and one number are enough to make the output seem intentional, which makes me more skeptical of how much real apps actually "know" about a listener.
