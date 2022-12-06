from cw_ngrams.cli import parse_args
from cw_ngrams.data import (
    construct_affixes,
    find_examples,
    load_words_and_freqs,
    merge_affixes,
    weight_affixes,
)
from cw_ngrams.output import make_output
