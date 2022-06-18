from typing import Optional

from cw_ngrams import (
    construct_affixes,
    find_examples,
    load_words_and_freqs,
    make_output,
    merge_affixes,
    parse_args,
)


def main(
    ngram_length: int,
    n_affixes: int,
    n_examples: int,
    only_prefixes: bool,
    only_suffixes: bool,
    sort_length: bool,
    shuffle: bool,
    min_example_length: Optional[int],
    max_example_length: Optional[int],
    similar: bool,
    dissimilar: bool,
):

    # Load words and their frequencies from the data file
    words, freqs = load_words_and_freqs()

    # Construct prefix and suffix lists; aggregate frequencies
    prefixes, suffixes = construct_affixes(words, freqs, ngram_length)

    # Combine prefix and suffix lists, or keep only the desired affix type
    affixes = merge_affixes(prefixes, suffixes, only_prefixes, only_suffixes, shuffle)

    # Find examples of words that match the affixes, potentially filtered by criteria
    examples = find_examples(
        words,
        affixes,
        n_affixes,
        n_examples,
        only_prefixes,
        only_suffixes,
        min_example_length,
        max_example_length,
        similar,
        dissimilar,
    )

    # Make the output friendly, and sort if requested
    output = make_output(examples, sort_length)

    for line in output:
        print(line)


if __name__ == "__main__":

    args = parse_args()
    main(
        ngram_length=args.ngram_length,
        n_affixes=args.n_affixes,
        n_examples=args.n_examples,
        only_prefixes=args.only_prefixes,
        only_suffixes=args.only_suffixes,
        sort_length=args.sort_length,
        shuffle=args.shuffle,
        min_example_length=args.min_example_length,
        max_example_length=args.max_example_length,
        similar=args.similar,
        dissimilar=args.dissimilar,
    )
