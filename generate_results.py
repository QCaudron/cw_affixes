from pathlib import Path
from subprocess import call, Popen


top_scenario = {
    "name": "top",
    "n_affixes": 100,
    "n_examples": 10,
    "sort": False,
    "shuffle": False,
}

random_scenario = {
    "name": "random",
    "n_affixes": 200,
    "n_examples": 10,
    "sort": True,
    "shuffle": True,
}

scenarios = []

for base_scenario in [top_scenario, random_scenario]:
    for ngram_length in range(2, 5):
        for prefixes in [True, False]:
            for suffixes in [True, False]:

                if prefixes and suffixes:
                    continue

                scenario = base_scenario.copy()
                scenario["ngram_length"] = ngram_length
                scenario["prefixes"] = prefixes
                scenario["suffixes"] = suffixes
                scenarios.append(scenario)

readme = "# Results\n\n"

for scenario in scenarios:

    name = scenario["name"]
    ngram_length = scenario["ngram_length"]
    n_affixes = scenario["n_affixes"]
    n_examples = scenario["n_examples"]
    sort = scenario["sort"]
    shuffle = scenario["shuffle"]
    prefixes = scenario["prefixes"]
    suffixes = scenario["suffixes"]

    if prefixes:
        affix_type = "prefixes"
    elif suffixes:
        affix_type = "suffixes"
    else:
        affix_type = "affixes"

    filename = Path(
        "results/"
        f"{ngram_length}-gram"
        f"_{name}"
        f"_{n_affixes}"
        f"_{affix_type}"
        f"{'_sorted' if sort else ''}"
        f"{'_shuffled' if shuffle else ''}"
        ".txt"
    ).as_posix()

    command = [
        "poetry",
        "run",
        "python",
        "cw_ngrams.py",
        "--ngram_length",
        str(ngram_length),
        "--n_affixes",
        str(n_affixes),
        "--n_examples",
        str(n_examples),
        "--prefixes" if prefixes else None,
        "--suffixes" if suffixes else None,
        "--sort" if sort else None,
        "--shuffle" if shuffle else None,
    ]

    command = [piece for piece in command if piece is not None]
    print(command)
    p = Popen(
        command,
        stdout=open(filename, "w"),
    )
    p.wait()

    list_name = f"{ngram_length}-letter {name} {affix_type}"
    if sort:
        list_name += " sorted"
    if shuffle:
        list_name += " shuffled"

    readme += f"""- [{list_name}]({filename})\n"""

with open("results/README.md", "w") as f:
    f.write(readme)
