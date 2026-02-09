from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class WordCountResult:
    """Represents a word and its frequency."""
    word: str
    count: int


def _is_word_char(ch: str) -> bool:
    """
    Decide whether a character belongs to a word token.

    Basic approach (no regex):
    - Accept letters and digits.
    - Treat everything else as separator.
    """
    if len(ch) != 1:
        return False
    return ch.isalnum()


def tokenize(text: str) -> List[str]:
    """
    Tokenize input text into words using basic algorithms (no regex).

    - Lowercases tokens for case-insensitive counting.
    - Splits using any non-alphanumeric as separator.
    """
    tokens: List[str] = []
    current_chars: List[str] = []

    for ch in text:
        if _is_word_char(ch):
            current_chars.append(ch.lower())
        else:
            if current_chars:
                tokens.append("".join(current_chars))
                current_chars = []

    if current_chars:
        tokens.append("".join(current_chars))

    return tokens


def count_words(tokens: List[str]) -> Dict[str, int]:
    """
    Count frequency of each distinct word.

    Uses a plain dict and loops (basic algorithm).
    """
    counts: Dict[str, int] = {}
    for token in tokens:
        if token == "":
            continue
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1
    return counts


def sort_counts(counts: Dict[str, int]) -> List[WordCountResult]:
    """
    Convert counts dict to a sorted list.

    Sort rules:
    - Descending by count
    - Ascending by word (for stable output)
    """
    items: List[Tuple[str, int]] = []
    for word, cnt in counts.items():
        items.append((word, cnt))

    items.sort(key=lambda x: (-x[1], x[0]))

    results: List[WordCountResult] = []
    for word, cnt in items:
        results.append(WordCountResult(word=word, count=cnt))

    return results