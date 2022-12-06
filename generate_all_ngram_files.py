from pathlib import Path
from subprocess import Popen
from typing import Dict, List

PREAMBLES = {
    "exercises": "Head-copy exercise :",
    "generic": "Generic results :",
}

# Base scenarios
BASE_SCENARIO = {
    "name": "top",
    "ngram_length": 3,
    "n_affixes": 300,
    "n_examples": 10,
    "sort": False,
    "shuffle": False,
    "prefixes": False,
    "suffixes": False,
    "similar": False,
    "dissimilar": False,
    "weighted": 0,
    "section": "generic",
}

RANDOM_SCENARIO = BASE_SCENARIO.copy()
RANDOM_SCENARIO.update({"name": "random", "sort": True, "shuffle": True})


def generate_scenarios() -> List[Dict]:

    scenarios = []

    # Create scenarios from the exercise base scenario
    for affix in ["prefixes", "suffixes"]:
        for sim in ["similar", "dissimilar"]:
            for weighted in [0, 5]:
                scenario = BASE_SCENARIO.copy()
                scenario["name"] = sim
                scenario["section"] = "exercises"
                scenario[affix] = True
                scenario[sim] = True
                scenario["weighted"] = weighted
                scenario["n_examples"] = 7  # 10 is too hard to find with similar / dissimilar
                scenario["min_word_length"] = 5
                scenario["max_word_length"] = 12
                scenarios.append(scenario)

    # Create various scenarios for more generic results
    for scenario_type in [BASE_SCENARIO, RANDOM_SCENARIO]:
        for ngram_length in range(2, 5):
            for prefixes in [True, False]:
                for suffixes in [True, False]:

                    # Prefixes only and suffixes only are mutually exclusive
                    if prefixes and suffixes:
                        continue

                    # We don't want randomly-selected 2-grams, they're nonsensical
                    if (ngram_length == 2) and (scenario_type["name"] == "random"):
                        continue

                    scenario = scenario_type.copy()
                    scenario["ngram_length"] = ngram_length
                    scenario["prefixes"] = prefixes
                    scenario["suffixes"] = suffixes
                    scenarios.append(scenario)

    return scenarios


def generate_command_from_scenario(scenario: Dict) -> List[str]:

    ngram_length = scenario["ngram_length"]
    n_affixes = scenario["n_affixes"]
    n_examples = scenario["n_examples"]
    sort = scenario["sort"]
    shuffle = scenario["shuffle"]
    prefixes = scenario["prefixes"]
    suffixes = scenario["suffixes"]
    similar = scenario["similar"]
    dissimilar = scenario["dissimilar"]
    weighted = scenario["weighted"]
    min_word_length = scenario.get("min_word_length")
    max_word_length = scenario.get("max_word_length")

    command = [
        "poetry",
        "run",
        "python",
        "generate_ngrams_from_scenario.py",
        "--ngram_length",
        str(ngram_length),
        "--n_affixes",
        str(n_affixes),
        "--n_examples",
        str(n_examples),
        "--weighted",
        str(weighted),
    ]

    if prefixes:
        command.append("--prefixes")
    if suffixes:
        command.append("--suffixes")
    if sort:
        command.append("--sort")
    if shuffle:
        command.append("--shuffle")
    if similar:
        command.append("--similar")
    if dissimilar:
        command.append("--dissimilar")
    if min_word_length is not None:
        command += ["--min_example_length", str(min_word_length)]
    if max_word_length is not None:
        command += ["--max_example_length", str(max_word_length)]

    return command


def generate_filename_from_scenario(scenario: Dict) -> Path:
    name = scenario["name"]
    ngram_length = scenario["ngram_length"]
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
        f"{'_weighted' if scenario['weighted'] > 0 else ''}"
        f"_{affix_type}"
        f"{'_sorted' if sort else ''}"
        f"{'_shuffled' if shuffle else ''}"
        ".txt"
    )

    return filename


def generate_link_from_scenario(scenario: Dict, filename: Path) -> str:

    name = scenario["name"]
    ngram_length = scenario["ngram_length"]
    sort = scenario["sort"]
    shuffle = scenario["shuffle"]
    prefixes = scenario["prefixes"]
    suffixes = scenario["suffixes"]
    preamble = PREAMBLES[scenario["section"]]

    if scenario["weighted"] > 0:
        weighted = "weighted"
    else:
        weighted = "unweighted"

    if prefixes:
        affix_type = "prefixes"
    elif suffixes:
        affix_type = "suffixes"
    else:
        affix_type = "affixes"

    # Add a link to this scenario in the results README
    link_name = f"{preamble} {name.title()} {weighted} {ngram_length}-gram {affix_type}"

    if sort:
        link_name += ", sorted"
    if shuffle:
        link_name += ", shuffled"

    readme_line = f"- [{link_name}]({filename.as_posix()})\n"
    return readme_line


def run_command(command: List[str], filename: Path) -> None:
    print(f"Generating {filename}; calling {' '.join(command)}")
    process = Popen(command, stdout=open("results" / filename, "w"))
    process.wait()


def main():

    readme = "# Results\n\n"

    # Create scenarios and their commands, their results filenames, and a link to those results
    scenarios = generate_scenarios()
    commands = [generate_command_from_scenario(scenario) for scenario in scenarios]
    filenames = [generate_filename_from_scenario(scenario) for scenario in scenarios]
    links = [
        generate_link_from_scenario(scenario, filename)
        for scenario, filename in zip(scenarios, filenames)
    ]

    # Run each scenario, saving output to a file and updating the README
    for command, filename, link in zip(commands, filenames, links):
        run_command(command, filename)
        readme += link

    # Save the README after running all scenarios
    with open("results/README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    main()
