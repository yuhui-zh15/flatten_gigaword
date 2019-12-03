import logging
import os
import re

from argparse import ArgumentParser
from bs4 import BeautifulSoup


def flatten_one_gigaword_file(file_path):
    # Parse the text with BeautifulSoup
    print(file_path)
    soup = BeautifulSoup(open(file_path), "html.parser")

    # Iterate over all <p> items and get the text for each.
    all_paragraphs = []
    for paragraph in soup("p"):
        # Turn inter-paragraph newlines into spaces
        paragraph = paragraph.get_text()
        paragraph = re.sub(r"\n+", "\n", paragraph)
        paragraph = paragraph.replace("\n", "")
        all_paragraphs.append(paragraph.strip())
    # Return a list of strings, where each string is a
    # space-tokenized paragraph.
    return all_paragraphs


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    parser = ArgumentParser(description=("Flatten a gigaword data file for "
                                         "use in language modeling."))
    parser.add_argument("--gigaword-path", required=True,
                        metavar="<gigaword_path>", type=str,
                        help=("Path to Gigaword directory, with "
                              "all .gz files unzipped."))
    parser.add_argument("--output-dir", required=True, metavar="<output_dir>",
                        type=str, help=("Directory to write final flattened "
                                        "Gigaword file."))

    A = parser.parse_args()
    all_paragraphs = flatten_one_gigaword_file(A.gigaword_path)
    output_path = os.path.join(A.output_dir,
                               os.path.basename(A.gigaword_path) + ".flat")
    with open(output_path, "w") as output_file:
        for paragraph in all_paragraphs:
            output_file.write("{}\n".format(paragraph))
