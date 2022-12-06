import random
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Tuple

import numpy as np
from thefuzz import fuzz  # type: ignore

from .cw import str_to_weight

Affix = Tuple[str, int]


def load_words_and_freqs() -> Tuple[List[str], List[int]]:
    """
    Load the words and their frequencies from the data file.

    Returns
    -------
    List[str]
        A list of words.
    List[int]
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

    prefixes: DefaultDict[str, int] = defaultdict(int)
    suffixes: DefaultDict[str, int] = defaultdict(int)

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
    shuffle: bool,
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
    shuffle : bool
        Whether to shuffle the top 300 affixes, rather than return them all in order.
        We limit to the top 300 because rarer affixes won't have many example word matches.

    Returns
    -------
    List[Affix]
        A list of combined affixes and their frequencies.
    """

    if only_prefixes:
        all_affixes = prefixes
    elif only_suffixes:
        all_affixes = suffixes
    else:
        all_affixes = sorted(prefixes + suffixes, key=lambda x: -x[1])

    # Ensure affixes are unique; perform a group-by
    unique_affixes_dict: DefaultDict[str, int] = defaultdict(int)
    for affix, freq in all_affixes:
        unique_affixes_dict[affix] += freq
    unique_affixes = list(unique_affixes_dict.items())

    # If we're shuffling, keep only the most common 300 or we'll get lots of nonsense
    if shuffle:
        unique_affixes = random.sample(unique_affixes[:300], k=min(300, len(unique_affixes)))

    return unique_affixes


def weight_affixes(affixes: List[Affix], weighted: float) -> List[Affix]:

    if weighted == 0:
        return affixes

    for idx in range(len(affixes)):
        affix, freq = affixes[idx]
        affixes[idx] = (affix, freq / (str_to_weight(affix) ** weighted))

    affixes = sorted(affixes, key=lambda x: -x[1])
    return affixes


def _filter_examples(
    examples: Dict[str, List[str]],
    n_examples: int,
    similar: bool,
    dissimilar: bool,
) -> Dict[str, List[str]]:
    """
    Filter examples for similiar or dissimilar words.

    Parameters
    ----------
    examples : Dict[str, List[str]]
        A dict mapping affixes to their examples.
    n_examples : int
        The number of examples to return for each affix.
    similar : bool
        Whether to return example words that are similar to one another.
    dissimilar : bool
        Whether to return example words that are dissimilar to one another.

    Returns
    -------
    Dict[str, List[str]]
        A dict mapping affixes to their examples.
    """

    if similar and dissimilar:
        raise ValueError("Cannot keep both similar and dissimilar words.")

    if similar or dissimilar:
        for affix, affix_examples in examples.items():

            similarities = np.zeros((len(affix_examples), len(affix_examples)))
            for i, first_example in enumerate(affix_examples):
                for j, second_example in enumerate(affix_examples):
                    if i == j:
                        continue
                    similarities[i, j] = fuzz.ratio(first_example, second_example)

            if similar:
                idx = np.argsort(-similarities.sum(0))[:n_examples]
            else:
                idx = np.argsort(similarities.sum(0))[:n_examples]

            examples[affix] = [affix_examples[i] for i in idx]

    return examples


def find_examples(
    words: List[str],
    affixes: List[Affix],
    n_affixes: int,
    n_examples: int,
    only_prefixes: bool,
    only_suffixes: bool,
    min_example_length: Optional[int],
    max_example_length: Optional[int],
    similar: bool,
    dissimilar: bool,
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

    # Are we filtering any examples post-match ? If so, we need to find many more examples
    # so that we can filter them out for similarity or dissimilarity.
    filters = similar or dissimilar
    target_n_examples: int = n_examples * 5 if filters else n_examples

    # Generate examples for each affix
    all_examples = defaultdict(list)
    n_affixes_found = 0

    for affix in affixes:

        for word in words:

            # If a word is not strictly longer than the affix, throw it out
            if len(word) <= len(affix[0]):
                continue

            # If the word matches but is too long or too short, skip it
            if min_example_length and (len(word) < min_example_length):
                continue
            if max_example_length and (len(word) > max_example_length):
                continue

            # For words of the right length, check for a match
            if match(affix[0], word):

                # Add it to the list of examples
                all_examples[affix[0]].append(word)

                # We either stop when we have enough examples or we run out of words
                # If it's the former, we count this affix as having the target number of words
                # Otherwise, this affix won't show up in the output; it has too few examples
                if len(all_examples[affix[0]]) == target_n_examples:
                    n_affixes_found += 1
                    break

        # If we've found sufficient affixes, stop looking for more examples
        if n_affixes_found == n_affixes:
            break

    # Keep only affixes with sufficient examples
    examples = {
        key: value for key, value in all_examples.items() if len(value) == target_n_examples
    }

    # Filter out examples that are too similar or too dissimilar if requested
    examples = _filter_examples(examples, n_examples, similar, dissimilar)

    return examples
