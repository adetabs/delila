# pylint: disable=missing-module-docstring, missing-class-docstring
import os
import sys
from trankit import Pipeline
from trankit.utils import CoNLL


def parse_and_save(doc: str, parser: Pipeline, output: str) -> None:
    """For given document, use NLP to parse it, and save as a CoNLL-U formatted file.

    Args:
        doc (str): Document to parse
        parser (Pipeline): NLP to use
        output (str): Filename or path to save output to.
    """
    processed_doc = parser(doc)
    CoNLL.dict2conll(processed_doc, output)


if __name__ == "__main__":
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
            data = file.read()
        parse_and_save(data, nlp, out_file)
    else:
        directory = sys.argv[1]
        for file in os.listdir(directory):
            with open(f"{directory}/{file}", "r", encoding="UTF-8") as document:
                data = document.read()
            out_file = directory + "/" + file.removesuffix(".txt") + ".conllu"
            parse_and_save(data, nlp, out_file)
