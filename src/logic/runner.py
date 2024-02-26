"""
Script execution logic.
"""

from pathlib import Path

import pandas as pd

from .core import format_xlsx, get_ean, make_df, make_xlsx, parse_xml


def run_xml2xlsx(file_path: Path):
    details, art_ids, file_name = parse_xml(file_path)

    data_frame: pd.DataFrame = make_df(details)

    art_barcodes: list[str] = get_ean(art_ids)

    # Add barcodes to the DF
    data_frame["barcode"] = art_barcodes

    output_xlsx: Path = file_path.parent / (file_name + ".xlsx")
    writer: pd.ExcelWriter = make_xlsx(file_name, output_xlsx, data_frame)

    format_xlsx(data_frame, writer)
