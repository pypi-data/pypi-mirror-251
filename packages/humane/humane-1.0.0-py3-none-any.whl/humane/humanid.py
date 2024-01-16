from enum import Enum
from pathlib import Path
import random


def read_wordlist(name: str) -> list[str]:
    current_file = Path(__file__).resolve()
    parent_dir = current_file.parent
    wordlist_path = parent_dir / f"{name}"
    return wordlist_path.read_text().splitlines()


class Wordlist(str, Enum):
    ADJECTIVES = "adjectives"
    COLOURS = "colours"
    ANIMALS = "animals"
    VERBS = "verbs"
    ADVERBS = "adverbs"


WORDLISTS = {
    Wordlist.ADJECTIVES: read_wordlist("./253-adjectives.txt"),
    Wordlist.COLOURS: read_wordlist("./162-colours.txt"),
    Wordlist.ANIMALS: read_wordlist("./200-animal-plurals.txt"),
    Wordlist.VERBS: read_wordlist("./281-verbs.txt"),
    Wordlist.ADVERBS: read_wordlist("./321-adverbs.txt"),
}

MAX_N = 10


def total_possibilities(wordlists: list[Wordlist], start: int = 1) -> int:
    total = start
    for wordlist in wordlists:
        total *= len(WORDLISTS.get(wordlist, []))
    return total


# Expected entropy: 30 * 253 * 200 = 1,518,000
def short_human_id(seed: str | None = None) -> str:
    rng = random.Random(seed)

    # <n> <adjective> <animal>
    parts = [
        str(rng.randint(2, MAX_N + 2)),
        rng.choice(WORDLISTS[Wordlist.ADJECTIVES]),
        rng.choice(WORDLISTS[Wordlist.ANIMALS]),
    ]
    return "-".join(parts)


def human_id(seed: str | None = None) -> str:
    rng = random.Random(seed)

    # <n> <adjective> <animal> <verb> <adverb>
    parts = [
        str(rng.randint(2, MAX_N + 2)),
        rng.choice(WORDLISTS[Wordlist.ADJECTIVES]),
        rng.choice(WORDLISTS[Wordlist.ANIMALS]),
        rng.choice(WORDLISTS[Wordlist.VERBS]),
        rng.choice(WORDLISTS[Wordlist.ADVERBS]),
    ]

    return "-".join(parts)
