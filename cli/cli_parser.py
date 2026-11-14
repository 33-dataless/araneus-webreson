import argparse


import argparse


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Araneus CLI"
        )

        self.parser.add_argument(
            "-d", "--domain",
            help="Domain to scan"
        )

        self.parser.add_argument(
            "--add-tool",
            nargs="+",
            metavar=("NAME", "EXECUTABLE", "ARGS"),
            help="Add custom tool: NAME EXECUTABLE [ARGS...]"
        )

    def parse(self):
        return self.parser.parse_args()
