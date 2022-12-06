ALPHABET = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
}


def str_to_weight(string: str) -> int:
    """
    Convert a string to a CW weight.

    Parameters
    ----------
    string : str
        Some text.

    Returns
    -------
    int
        The weight of the characters.
    """

    cw_string = "".join([ALPHABET[char.upper()] for char in string])
    weight = cw_string.count(".") + cw_string.count("-") * 3

    return weight
