
import argparse


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="araneus",
            description="Araneus domain scanner"
        )

        action = self.parser.add_mutually_exclusive_group(required=True)

        action.add_argument(
            "-d", "--domain",
            help="Domain to scan"
        )
        action.add_argument(
            "--add-tool",
            nargs=argparse.REMAINDER,
            metavar="ARGS",
            help="Add tool: NAME EXECUTABLE [ARGS...]"
        )
        action.add_argument(
            "--list-tools",
            action="store_true"
        )
        action.add_argument(
            "--delete-tool",
            metavar="ID"
        )
        action.add_argument(
            "--edit-tool",
            metavar="ID"
        )

        # Дополнительный флаг, совместимый с -d
        self.parser.add_argument(
            "--sudo",
            action="store_true",
            help="Run Araneus with root privileges"
        )

    def parse(self):
        return self.parser.parse_args()
