from cw_ngrams import (
    construct_affixes,
    find_examples,
    load_words_and_freqs,
    make_output,
    merge_affixes,
    parse_args,
    sample_affixes,
)


def main(
    ngram_length: int,
    n_affixes: int,
    n_examples: int,
    only_prefixes: bool,
    only_suffixes: bool,
    sort_length: bool,
    shuffle: bool,
):

    # Load words and their frequencies from the data file
    words, freqs = load_words_and_freqs()

    # Construct prefix and suffix lists; aggregate frequencies
    prefixes, suffixes = construct_affixes(words, freqs, ngram_length)

    # Combine prefix and suffix lists, or keep only the desired affix type
    all_affixes = merge_affixes(prefixes, suffixes, only_prefixes, only_suffixes)

    # Grab the most common affixes, or a random subset
    affixes = sample_affixes(all_affixes, n_affixes, shuffle)

    # Find examples of words that match the affixes
    examples = find_examples(words, affixes, n_examples, only_prefixes, only_suffixes)

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
    )
