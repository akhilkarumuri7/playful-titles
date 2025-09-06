# Playful Paper Title Generation Tryout Project

This is a tryout project for Professor Jordan Boyd-Graber, where I tried to figure out which paper titles are “playful” vs normal.

---

## Data
I got the data from the provided CS-PaperSum dataset on arxiv.  
The raw csv is huge (like 3GB) so it’s not here. Instead I cleaned it with a script and then used the smaller processed version.  

Files in `data/processed/`:
- `papers.csv.gz`: cleaned paperID, title, abstract  
- `papers_with_playfulness.csv.gz`: same, but added a column for if it’s playful  
- `playful_titles_only.csv`: just the playful ones  

---

## How it works
Wrote some rules to check if a title looks playful. Stuff like:
- if it has pop culture words (Harry Potter, Star Wars, Mario, etc)  
- if it looks like a template (All You Need…, To ___ or Not To ___, Hitchhiker’s Guide…)  
- some pun regex (like “Phone-ing it in”, “know-who”, “what do you meme”)  
- acronyms that are actual words (like DAMN, HERO)  

Also tried to make sure it doesn’t mark boring model names (`XYZ-Net: Subtitle`) or very serious things (dataset, benchmark, hate speech).  

---

## How to run
1. first preprocess the big file (if you actually have it):
`python src/prep_data.py --input data/raw/All_capped_keywords.csv --out data/processed/papers.csv`
2. then run the filter:
`python src/filter_titles.py`


This makes the outputs in `data/processed/`.

---

## Results
Some titles that came out as playful:
- MarioNETte: Few-shot Face Reenactment …  
- Epistemic Logic of Know-Who  
- The Hitchhiker’s Guide to Testing Statistical Significance in NLP  
- Phone-ing it in: Towards Flexible Multi-Modal LLM Training  
- DAMN: Defeasible Reasoning Tool …  
- What do you MEME? Generating Explanations for Visual Semantic Role Labelling in Memes  

It only flagged about .1% of the papers

---

## Notes
This is all just heuristics, not a real ML model. It works alright, but misses many jokes and still has some false positives. If I had more time I’d probably label data and fine-tune a model instead.
