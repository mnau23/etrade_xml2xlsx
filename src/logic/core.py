"""
Script core logic.
"""

import csv
import os
import sys
import xml.etree.ElementTree as elemTree  # only for type hints
from pathlib import Path

import pandas as pd
from defusedxml import ElementTree as defusedElemTree


def resource_path(relative_path) -> str:
    """
    Get absolute path to a resource (works for both dev and PyInstaller).

    Parameters:
        relative_path (str): name of file

    Returns:
        str: correct full path of file
    """

    # PyInstaller creates a temp folder and stores path into var _MEIPASS
    base_path: str = getattr(sys, "_MEIPASS", os.path.abspath("./assets/csv/"))

    return os.path.join(base_path, relative_path)


def parse_xml(path: Path) -> tuple[list[elemTree.Element], list[str], str]:
    """
    Retrieve data from input XML file.

    Parameters:
        path (Path): path of file

    Returns:
        list[Element]: list with all elements found in XML file
        list[str]: list with only the article's id (full description = id + description)
        str: name of Excel file to be created
    """

    print("Retrieving data from XML file '" + path.stem + "'...")

    a_id: list[str] = []

    # XML structure
    tree: elemTree.ElementTree = defusedElemTree.parse(path)
    root: elemTree.Element = tree.getroot()

    tmp = root.find(".//DatiGenerali/DatiGeneraliDocumento/Numero")
    invoice_nr: str = tmp.text if tmp is not None and tmp.text is not None else ""

    c_path = ".//CessionarioCommittente/DatiAnagrafici/Anagrafica"
    customer_xml: str
    try:
        tmp = root.find(f"{c_path}/Denominazione")
        customer_xml = tmp.text if tmp is not None and tmp.text is not None else ""
    except AttributeError:
        tmp = root.find(f"{c_path}/Nome")
        first_name: str = tmp.text if tmp is not None and tmp.text is not None else ""
        tmp = root.find(f"{c_path}/Cognome")
        last_name: str = tmp.text if tmp is not None and tmp.text is not None else ""
        customer_xml = f"{last_name} {first_name}"
    customer: str = shorten_customer_name(customer_xml.replace(".", "")).replace(" ", "_")

    name: str = "FATT_NR_" + invoice_nr + "_" + customer

    dbs: elemTree.Element | None = root.find(".//DatiBeniServizi")
    details: list[elemTree.Element] = dbs.findall("DettaglioLinee") if dbs else []

    # Remove last element -useless in this XML file-
    details.pop(len(details) - 1)

    for node in details:
        tmp = node.find("Descrizione")
        description = tmp.text if tmp is not None and tmp.text is not None else ""
        a_id.append(description.partition(" ")[0])

    print("Done!")
    return details, a_id, name


def shorten_customer_name(c_name: str) -> str:
    """
    Get shortened customer name.

    Parameters:
        c_name (str): customer name found in XML file

    Returns:
        str: customer name with improved readability
    """

    with open(resource_path("customers.csv"), "r", encoding="utf-8-sig") as file:
        reader = list(csv.DictReader(file))
        for row in reader:
            if row["original_customer_name"] == c_name:
                return row["shown_customer_name"]
        return "na"


def make_df(detail_list) -> pd.DataFrame:
    """
    Create Pandas DataFrame.

    Parameters:
        detail_list (list[Element]): list of elements from XML file

    Returns:
        DataFrame: contains important rows from XML file with related details
    """

    # Pandas DF structure
    df_cols: list[str] = [
        "barcode",
        "full_description",
        "quantity",
        "unit_price",
        "total_price",
        "VAT",
    ]
    rows = []

    for node in detail_list:
        s_desc = node.find("Descrizione").text
        s_qty = node.find("Quantita").text
        s_unit = node.find("PrezzoUnitario").text
        s_total = node.find("PrezzoTotale").text
        s_vat = node.find("AliquotaIVA").text
        rows.append(
            {
                "full_description": s_desc,
                "quantity": s_qty,
                "unit_price": s_unit,
                "total_price": s_total,
                "VAT": s_vat,
            }
        )

    out_df: pd.DataFrame = pd.DataFrame(rows, columns=df_cols)

    # Some conversions
    out_df["quantity"] = out_df["quantity"].astype(float).astype(int)
    out_df["unit_price"] = out_df["unit_price"].astype(float)
    out_df["total_price"] = out_df["total_price"].astype(float)
    out_df["VAT"] = out_df["VAT"].astype(float) / 100

    return out_df


def get_ean(id_list: list[str]) -> list[str]:
    """
    Search EAN barcodes for each article.

    Parameters:
        id_list (list[str]): list of article IDs

    Returns:
        list[str]: list of EAN barcodes corresponding to each article ID
    """

    ean: list[str] = []

    with open(resource_path("barcodes.csv"), "r", encoding="utf-8-sig") as file:
        reader = list(csv.DictReader(file))
        for i in id_list:
            barcode = ""
            for row in reader:
                # If article_id (row[0]) of ean_file is in id_list and
                # barcode (row[1]) is not empty, get the barcode
                if row["article_id"] == i and row["barcode"]:
                    barcode = row["barcode"]
            # If barcode is found, add it to the list. Otherwise, add "n/a"
            if barcode:
                ean.append(barcode)
            else:
                ean.append("n/a")

    return ean


def make_xlsx(f_name: str, out_xlsx: Path, data_frame: pd.DataFrame) -> pd.ExcelWriter:
    """
    Create Excel file.

    Parameters:
        f_name (str): name of output Excel file to be created
        out_xlsx (Path): path of output Excel file
        data_frame (DataFrame): values to be converted into Excel

    Returns:
        ExcelWriter: object for writing DataFrame into Excel sheets
    """

    print("Creating '" + f_name + ".xlsx'...")
    writer: pd.ExcelWriter = pd.ExcelWriter(out_xlsx, engine="xlsxwriter")
    data_frame.to_excel(writer, index=False, sheet_name="Codici EAN Fattura")
    return writer


def format_xlsx(data_frame: pd.DataFrame, writer):
    """
    Improve Excel file formatting.

    Parameters:
        data_frame (DataFrame): values to be converted into Excel
        writer (ExcelWriter): object for writing DataFrame into Excel sheets
    """

    print("Formatting file...")

    # Define formats for Excel workbook
    workbook = writer.book
    worksheet = writer.sheets["Codici EAN Fattura"]
    format_header = workbook.add_format(
        {"align": "center", "bold": True, "border": 1, "fg_color": "#d9d9d9"}
    )
    format_float = workbook.add_format({"align": "center", "num_format": "€ #,##0.00"})
    format_int = workbook.add_format({"align": "center"})
    format_pct = workbook.add_format({"align": "center", "num_format": "0%"})

    # Auto-adjust columns' width
    for column in data_frame:
        column_width = max(
            data_frame[column].apply(lambda x: len(str(x))).max(), len(str(column))
        )
        column_width = max(column_width, 5)
        col_idx = data_frame.columns.get_loc(column)
        worksheet.set_column(col_idx, col_idx, column_width)

    # Format columns
    for col_num, val in enumerate(data_frame.columns.values):
        worksheet.write(0, col_num, val, format_header)  # header
    worksheet.set_column("C:C", None, format_int)  # quantity
    worksheet.set_column("D:D", None, format_float)  # unit price
    worksheet.set_column("E:E", None, format_float)  # total price
    worksheet.set_column("F:F", None, format_pct)  # VAT

    writer.close()
    print("File Excel created!")
