from wordcount_core import tokenize, count_words, sort_counts


def test_tokenize_basic() -> None:
    text = "Hello hello, world! WORLD..."
    tokens = tokenize(text)
    assert tokens == ["hello", "hello", "world", "world"]


def test_count_words_basic() -> None:
    tokens = ["a", "b", "a", "c", "b", "a"]
    counts = count_words(tokens)
    assert counts["a"] == 3
    assert counts["b"] == 2
    assert counts["c"] == 1


def test_sort_counts() -> None:
    counts = {"b": 2, "a": 2, "c": 3}
    results = sort_counts(counts)

    # Desc count, then asc word
    assert results[0].word == "c"
    assert results[0].count == 3

    assert results[1].word == "a"
    assert results[1].count == 2

    assert results[2].word == "b"
    assert results[2].count == 2