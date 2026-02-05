# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring

from trankit import Pipeline
from trankit.utils import CoNLL

if __name__ == "__main__":
    nlp = Pipeline("finnish")

    with open("./valtonen.txt", "r", encoding="UTF-8") as file:
        data = file.read()

    processed_data = nlp(data)

    CoNLL.dict2conll(processed_data, "valtonen.conllu")
