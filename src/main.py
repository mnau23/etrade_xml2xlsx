"""
Main entrypoint.
"""

from pathlib import Path

import pandas as pd

from xml2xlsx.xml2xlsx import format_xlsx, get_ean, make_df, make_xlsx, parse_xml


def main():
    file_path: Path = Path(input("Enter XML file path to convert...\n"))

    # Check if file is an XML
    while file_path.suffix != ".xml":
        file_path = Path(input("Not an XML file. Enter a correct path...\n"))

    details, art_ids, file_name = parse_xml(file_path)

    data_frame: pd.DataFrame = make_df(details)

    art_barcodes: list[str] = get_ean(art_ids)

    # Add barcodes to the DF
    data_frame["barcode"] = art_barcodes

    output_xlsx: Path = file_path.parent / (file_name + ".xlsx")
    writer: pd.ExcelWriter = make_xlsx(file_name, output_xlsx, data_frame)

    format_xlsx(data_frame, writer)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
