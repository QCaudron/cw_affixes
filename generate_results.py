from pathlib import Path
from subprocess import Popen


# Set up some base scenarios for both top affixes and random affixes
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
readme = "# Results\n\n"

# Create various scenarios
for base_scenario in [top_scenario, random_scenario]:
    for ngram_length in range(2, 5):
        for prefixes in [True, False]:
            for suffixes in [True, False]:

                # Prefixes only and suffixes only are mutually exclusive
                if prefixes and suffixes:
                    continue

                # We don't want randomly-selected 2-grams, they're nonsensical
                if (ngram_length == 2) and (base_scenario["name"] == "random"):
                    continue

                scenario = base_scenario.copy()
                scenario["ngram_length"] = ngram_length
                scenario["prefixes"] = prefixes
                scenario["suffixes"] = suffixes
                scenarios.append(scenario)

# Run each scenario, saving output to a file
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
        f"{ngram_length}-gram"
        f"_{name}"
        f"_{n_affixes}"
        f"_{affix_type}"
        f"{'_sorted' if sort else ''}"
        f"{'_shuffled' if shuffle else ''}"
        ".txt"
    )

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

    # Clean up missing pieces from the command
    command = [piece for piece in command if piece is not None]
    print(command)
    p = Popen(
        command,
        stdout=open("results" / filename, "w"),
    )
    p.wait()

    # Add a link to this scenario in the results README
    list_name = f"{ngram_length}-letter {name} {affix_type}"
    if sort:
        list_name += " sorted"
    if shuffle:
        list_name += " shuffled"
    readme += f"""- [{list_name}]({filename.as_posix()})\n"""

# Save the README after running all scenarios
with open("results/README.md", "w") as f:
    f.write(readme)
