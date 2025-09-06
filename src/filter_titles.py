import pandas as pd
import re

# --- Small, hand-made lists ---

POP_TERMS = [
    "Avengers", "Pokemon", "Barbie", "Taylor Swift", "Sherlock",
    "Hobbit", "Batman", "Spiderman", "Harry Potter", "Star Wars", "Marvel",
    "Hitchhiker", "Mario", "Yoda", "Shrek", "Simpsons", "Seinfeld",
    "Lord of the Rings", "Game of Thrones",
]

# Common playful title templates
TEMPLATES = [re.compile(rx, re.I) for rx in [
    r"\bAll You Need\b",
    r"\bTo .* or Not to .*\b",
    r"\bHitchhiker'?s Guide\b",
    r"\bMuch Ado About .*\b",
]]

# Very small set of pun patterns (just a starting point)
PUN_PATTERNS = [re.compile(rx, re.I) for rx in [
    r"\bknow-who\b",
    r"\bjust another [a-z]+\b",
    r"\b[a-z]+-ing it in\b",
    r"\bwhat do you meme\b",
]]

# Words that are usually serious/non-playful
NEGATIVE_TERMS = [
    "dataset", "data set", "benchmark", "survey",
    "hate speech", "racist", "toxicity", "adversarial",
]

# A few acronyms that are also real words
REAL_WORD_ACROS = {"DAMN", "HERO", "PANIC", "ELVIS", "HYPE"}

MODEL_TOKEN = re.compile(r"^[A-Z0-9\-]{3,12}$")
MODEL_SUFFIX = re.compile(r"(-?Net|-?Former|Trans|CNN|RNN|GNN|MLP|ViT|NLP|DL|AI|GPU|3D|2D)$", re.I)


def generic_model_colon(title: str) -> bool:
    m = re.match(r"^([^:]+):", title)
    if not m:
        return False
    head = m.group(1).replace("–", "-").replace("—", "-").strip()
    if " " in head:
        return False
    return bool(MODEL_TOKEN.match(head) or MODEL_SUFFIX.search(head))


def real_word_acronym(title: str) -> bool:
    m = re.match(r"^([A-Z]{3,6}):", title)
    return bool(m and m.group(1) in REAL_WORD_ACROS)


def has_any_regex(patterns, text: str) -> bool:
    return any(rx.search(text) for rx in patterns)


def is_playful(title: str) -> bool:
    if not isinstance(title, str):
        return False
    t = title.strip()
    if not t:
        return False

    low = t.lower()

    # quick outs
    if any(term in low for term in NEGATIVE_TERMS):
        return False
    if generic_model_colon(t) and not real_word_acronym(t):
        return False

    # strong cues
    if any(term.lower() in low for term in POP_TERMS):
        return True
    if has_any_regex(TEMPLATES, t):
        return True
    if has_any_regex(PUN_PATTERNS, t):
        return True
    if real_word_acronym(t):
        return True

    return False


if __name__ == "__main__":
    df = pd.read_csv("data/processed/papers.csv")

    # avoid NaNs crashing apply
    df["title"] = df["title"].fillna("")

    df["playful"] = df["title"].apply(is_playful)
    df.to_csv("data/processed/papers_with_playfulness.csv", index=False)
    df[df["playful"]].to_csv("data/processed/playful_titles_only.csv", index=False)

    print(df["playful"].value_counts())
    print("Saved papers_with_playfulness.csv and playful_titles_only.csv")
