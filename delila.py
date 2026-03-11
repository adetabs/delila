"""delila -- an adjective finding program

This program uses the trankit toolkit for its parsing functions. Thanks!

Check README.md for more info.

Copyright (C) 2026 Adela Noponen & Emma Koskinen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from copy import deepcopy
import csv
from enum import Enum
import os
import sys
from trankit import Pipeline
from trankit.utils import CoNLL


class POS(str, Enum):
    """Enum describing possible values for Token.pos_.
    """
    ADJ = "ADJ"
    CCONJ = "CCONJ"
    ADP = "ADP"
    ADV = "ADV"
    AUX = "AUX"
    DET = "DET"
    INTJ = "INTJ"
    NOUN = "NOUN"
    NUM = "NUM"
    PART = "PART"
    PRON = "PRON"
    PROPN = "PROPN"
    PUNCT = "PUNCT"
    SCONJ = "SCONJ"
    SPACE = "SPACE"
    SYM = "SYM"
    VERB = "VERB"
    X = "X"


def find_adjectives(content) -> list[dict[str, str | list[str]]]:
    """Process tokenized content and find strings of two or more adjectives

    Args:
        content: Tokenized document data.

    Returns:
        AdjectiveData: A list where each item represents
            one result (one adjective sequence).
            Each item is a dictionary containing keys
            "sentence": str and "adjective_list": list[str]
    """

    result: list[dict[str, str | list[str]]] = []

    for sentence in content["sentences"]:

        one_result: dict[str, str | list[str]] = {}

        one_result["sentence"] = sentence["text"]

        # Remove filler
        sentence = [word for word in sentence["tokens"]
                    if "upos" in word
                    and word["upos"] not in (POS.CCONJ, POS.PUNCT, POS.SYM, POS.SPACE)]

        # Skip one-word sentences
        if len(sentence) == 1:
            continue

        # Dumb loop logic
        loop = list(range(0, len(sentence), 1))
        pointer = 0

        # Iterate over every word of the sentence allowing skips in the iteration using pointer += 1
        for _ in range(len(loop)):

            # Dumb loop logic
            if pointer >= len(loop):
                break

            one_result["adjective_list"] = []
            string_of_adjectives: list[str] = []

            # Is the current word an adjective?
            while sentence[pointer]["upos"] == POS.ADJ:

                # What is the conjugation of the current adjective?
                conjugation = get_conjugation(sentence[pointer])

                # Are we at the last word of the sentence?
                if pointer + 1 >= len(sentence):

                    # Was the previous word an adjective in the same conjugation?
                    if fills_conditions(sentence[pointer-1], conjugation):
                        string_of_adjectives.append(sentence[pointer]["lemma"])

                # Are either of the neighboring words adjectives in the same conjugation?
                # - elif because there is no following word in the previous case
                # - abs() is there so we don't wrap around
                elif fills_conditions(sentence[pointer+1], conjugation) or \
                        fills_conditions(sentence[abs(pointer-1)], conjugation):
                    string_of_adjectives.append(sentence[pointer]["lemma"])

                # Did we just handle the last word of the sentence?
                pointer += 1
                if pointer >= len(sentence):
                    break

            if len(string_of_adjectives) != 0:
                one_result["adjective_list"] = string_of_adjectives
                result.append(deepcopy(one_result))

            pointer += 1

    return result


def fills_conditions(checked_token, conj: str | None) -> bool:
    """Checks if word fills the conditions set for the parser.

    Args:
        checked_token (Token): A single word token.
        conj (str): Conjugation of the word to be checked against

    Returns:
        bool: True if conditions are fulfilled, else false.
    """
    if POS.ADJ not in checked_token["upos"]:
        return False
    if conj is None:
        return True
    checked_conj = get_conjugation(checked_token)
    return conj == checked_conj or checked_conj is None


def get_conjugation(token) -> str | None:
    """Get morphological feature tags of the token, then extract case information.

    Args:
        token (Token): A single word token.

    Returns:
        str: The case of the token.
    """
    try:
        return dict(pair.split("=") for pair in token["feats"].split("|"))["Case"]
    except KeyError:  # No case tagged
        return None


def parse_and_save(doc: str, parser: Pipeline, output: str):
    """For given document, use NLP to parse it, and save as a CoNLL-U formatted file.

    Args:
        doc (str): Document to parse
        parser (Pipeline): NLP to use
        output (str): Filename or path to save output to.
    """
    processed_doc = parser(doc)
    CoNLL.dict2conll(processed_doc, output)
    return processed_doc


def write_results_to_file(filename: str, output) -> None:
    """Write AdjectiveData results to a CSV file.

    Args:
        filename (str): Name of the file to write to.
        output (AdjectiveData): The AdjectiveData that will be written.
    """
    with open(filename, "w", encoding="UTF-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            for i, adjective in enumerate(row["adjective_list"]):
                row[f"adjective_{i+1}"] = adjective
            row.pop("adjective_list")
            writer.writerow(row.values())


if __name__ == "__main__":
    print("Copyright (c) 2026 Adela Noponen & Emma Koskinen")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it under certain "
          "conditions; See the GNU Affero General Public License for more details.")
    print("")

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} input [output]", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) >= 3:
        out_file = sys.argv[2]
    else:
        out_file = sys.argv[1].removesuffix('.txt') + ".conllu"

    nlp = Pipeline("finnish")

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="UTF-8") as file:
            data = file.read().replace("\n", " ")
        tokenized_doc = parse_and_save(data, nlp, out_file)
        results = find_adjectives(tokenized_doc)
        write_results_to_file(
            sys.argv[1].removesuffix('.txt') + ".csv", results)
    else:
        directory = sys.argv[1]
        for file in os.listdir(directory):
            if not file.lower().endswith(".txt"):
                continue
            with open(f"{directory}/{file}", "r", encoding="UTF-8") as document:
                data = document.read().replace("\n", " ")
            out_file = directory + "/" + file.removesuffix(".txt") + ".conllu"
            tokenized_doc = parse_and_save(data, nlp, out_file)
            results = find_adjectives(tokenized_doc)
            write_results_to_file(out_file.removesuffix(
                ".conllu") + ".csv", results)
