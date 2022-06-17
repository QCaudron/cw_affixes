import random
from collections import defaultdict
from typing import Dict, List, Tuple

Affix = Tuple[str, int]


def load_words_and_freqs() -> Tuple[List[str], List[int]]:
    """
    Load the words and their frequencies from the data file.

    Returns
    -------
    List[str]
        A list of words.
    List[int]]
        The frequencies (counts) of the words.
    """

    with open("data/most_common_words.txt", "r") as f:
        lines = f.readlines()

    # Separate the words and their frequencies; clean line endings
    top_n_lines = [line.strip().split("\t") for line in lines]

    # Unzip the word and frequency lists into their own lists; cast frequencies to ints
    words = [line[0] for line in top_n_lines]
    freqs = [int(line[1]) for line in top_n_lines]

    return words, freqs


def construct_affixes(
    words: List[str], freqs: List[int], ngram_length: int
) -> Tuple[List[Affix], List[Affix]]:
    """
    Construct prefixes and suffixes.

    For each affix, aggregate the frequencies of their occurences.

    Parameters
    ----------
    words : List[str]
        A list of words.
    freqs : List[int]
        A list of word frequencies.
    ngram_length : int
        The length of the affixes to construct.

    Returns
    -------
    List[Affix]
        The prefixes and their frequencies.
    List[Affix]
        The suffixes and their frequencies.
    """

    prefixes: Dict[str, int] = defaultdict(int)
    suffixes: Dict[str, int] = defaultdict(int)

    for word, freq in zip(words, freqs):

        # Only extract n-grams from words of length n+1
        if len(word) > ngram_length:
            prefixes[word[:ngram_length]] += freq
            suffixes[word[-ngram_length:]] += freq

    # Sort by frequency
    prefixes_sorted = sorted(prefixes.items(), key=lambda x: -x[1])
    suffixes_sorted = sorted(suffixes.items(), key=lambda x: -x[1])

    return prefixes_sorted, suffixes_sorted


def merge_affixes(
    prefixes: List[Affix],
    suffixes: List[Affix],
    only_prefixes: bool,
    only_suffixes: bool,
) -> List[Affix]:
    """
    Combine prefixes and suffixes into a single ordered list.

    This can be a list of only prefixes, only suffixes, or both.

    Parameters
    ----------
    prefixes : List[Affix]
        The prefixes and their frequencies.
    suffixes : List[Affix]
        The suffixes and their frequencies.
    only_prefixes : bool
        Whether to only include prefixes in the combined list.
    only_suffixes : bool
        Whether to only include suffixes in the combined list.

    Returns
    -------
    List[Affix]
        A list of combined affixes and their frequencies.
    """

    if only_prefixes:
        return prefixes
    elif only_suffixes:
        return suffixes

    affixes = sorted(prefixes + suffixes, key=lambda x: -x[1])

    return affixes


def sample_affixes(affixes: List[Affix], n_affixes: int, shuffle: bool) -> List[Affix]:
    """
    Return the selected affixes from the list of all affixes.

    The selected affixes are either the most common, or a random subset.

    Parameters
    ----------
    affixes : List[Affix]
        The list of affixes and their frequencies.
    n_affixes : int
        The number of affixes to select.
    shuffle : bool
        Whether to return randomly-selected affixes.

    Returns
    -------
    List[Affix]
        The list of selected affixes.
    """
    if shuffle:
        return random.sample(affixes[:500], k=n_affixes)
    return affixes[:n_affixes]


def find_examples(
    words: List[str],
    affixes: List[Affix],
    n_examples: int,
    only_prefixes: bool,
    only_suffixes: bool,
) -> Dict[str, List[str]]:
    """
    Find a list of examples that match the affixes.

    Parameters
    ----------
    words : List[str]
        The words from which to find examples.
    affixes : List[Affix]
        The affixes and their frequencies.
    n_examples : int
        The number of examples to find for each affix.
    only_prefixes : bool
        Whether to only search for words that match prefixes.
    only_suffixes : bool
        Whether to only search for words that match suffixes.

    Returns
    -------
    Dict[str, List[str]]
        A dict mapping affixes to a list of examples that match them.
    """

    # Determine how to find matches
    if only_prefixes:
        match = lambda affix, word: word.startswith(affix)
    elif only_suffixes:
        match = lambda affix, word: word.endswith(affix)
    else:
        match = lambda affix, word: word.startswith(affix) or word.endswith(affix)

    examples = defaultdict(list)
    for affix in affixes:

        for word in words:

            # If a word is not strictly longer than the affix, throw it out
            if len(word) <= len(affix[0]):
                continue

            if match(affix[0], word):
                examples[affix[0]].append(word)

                # After finding enough examples, stop
                if len(examples[affix[0]]) == n_examples:
                    break

    return examples
