from typing import Dict, List


def make_output(examples: Dict[str, List[str]], sort_length: bool) -> List[str]:
    """
    Make the output user-friendly, and sort if requested.

    Parameters
    ----------
    examples : Dict[str, List[str]]
        A dict mapping affixes to a list of examples that match them.
    sort_length : bool
        Whether to sort the output by length.
    shuffle : bool
        Wheter the randomly shuffle the output

    Returns
    -------
    List[str]
        A list of affixes and examples.
    """

    output = []
    for affix, affix_examples in examples.items():

        # Sort examples by length
        if sort_length:
            affix_examples = sorted(affix_examples, key=lambda x: len(x))

        # Construct output lines
        output.append(f"{affix.upper()} - {', '.join(affix_examples).upper()}")

        # Sort output lines by length
        if sort_length:
            output = sorted(output, key=lambda x: len(x))

    return output
