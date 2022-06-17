import argparse


def validate_ngram_length(ngram_length_: str) -> int:
    """
    Validate that the ngram_length argument is valid : between 1 and 10.
    """
    ngram_length = int(ngram_length_)
    if ngram_length > 10:
        raise argparse.ArgumentTypeError("ngram_length must be <= 10.")
    if ngram_length < 1:
        raise argparse.ArgumentTypeError("ngram_length must be > 0.")
    return ngram_length


def validate_n_examples(n_examples_: str) -> int:
    """
    Validate that the n_examples argument is valid : greater than or equal to 0.
    """
    n_examples = int(n_examples_)
    if n_examples < 0:
        raise argparse.ArgumentTypeError("n_examples must be >= 0.")
    return n_examples


def validate_n_affixes(n_affixes_: str) -> int:
    """
    Validate that the n_affixes argument is valid : greater than 0.
    """
    n_affixes = int(n_affixes_)
    if n_affixes <= 0:
        raise argparse.ArgumentTypeError("n_affixes must be > 0.")
    return n_affixes


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser()

    # The number of affixes (lines), the number of examples per affix, and the n-gram length
    parser.add_argument(
        "--ngram_length",
        type=validate_ngram_length,
        default=3,
        help=("The number of characters in the affix n-grams; max 10, defaults to 3."),
    )
    parser.add_argument(
        "--n_affixes",
        type=validate_n_affixes,
        default=10,
        help="The number of affixes to return; defaults to 10.",
    )
    parser.add_argument(
        "--n_examples",
        type=validate_n_examples,
        default=5,
        help="The number of the examples containing each affix to return; defaults to 5.",
    )

    # Whether to return only prefixes, only suffixes, or both
    affix_type = parser.add_mutually_exclusive_group()
    affix_type.add_argument(
        "--prefixes",
        action="store_true",
        dest="only_prefixes",
        help="Only return prefixes and their examples.",
    )
    affix_type.add_argument(
        "--suffixes",
        action="store_true",
        dest="only_suffixes",
        help="Only return suffixes and their examples.",
    )

    # Whether to return the examples sorted by length
    parser.add_argument(
        "--sort",
        action="store_true",
        dest="sort_length",
        help="Sort the affixes and their examples by word length.",
    )

    # Whether to select random affixes, or in frequency order
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help=(
            "Randomly shuffle the affixes and their examples by word length. "
            "This will randomly select from the top 1,000 affixes."
        ),
    )

    args = parser.parse_args()
    return args
