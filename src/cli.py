"""
CLI entrypoint.
"""

from pathlib import Path

from logic.runner import run_xml2xlsx


def cli():
    """
    CLI main function.
    """

    file_path: Path = Path(input("Enter XML file path to convert...\n"))

    # Check if file is an XML
    while file_path.suffix != ".xml":
        file_path = Path(input("Not an XML file. Enter a correct path...\n"))

    run_xml2xlsx(file_path)

    input("Press Enter to exit...")


if __name__ == "__main__":
    cli()
