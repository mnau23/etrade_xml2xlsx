import csv
import os
import sys
import xml.etree.ElementTree as elemTree
from pathlib import Path

import pandas as pd


def resource_path(relative_path) -> str:
    """
    Get absolute path to a resource (works for both dev and PyInstaller).

    Parameters:
        relative_path (str): name of file

    Returns:
        str: correct full path of file
    """

    try:
        # PyInstaller creates a temp folder and stores path into var _MEIPASS
        base_path: str = sys._MEIPASS
    except Exception:
        base_path: str = os.path.abspath("./src/files/")

    return os.path.join(base_path, relative_path)


def parse_xml(fp: Path) -> tuple[list[elemTree.Element], list[str], str]:
    """
    Retrieve data from input XML file.

    Parameters:
        fp (Path): path of file

    Returns:
        list[Element]: list with all elements found in XML file
        list[str]: list with only the article's id (full description = id + description)
        str: name of Excel file to be created
    """

    print("Retrieving data from XML file '" + fp.stem + "'...")

    a_id: list[str] = list()

    # XML structure
    tree: elemTree = elemTree.parse(fp)
    root: elemTree.Element = tree.getroot()

    invoice_nr: str = root.find(".//DatiGenerali/DatiGeneraliDocumento/Numero").text
    customer_name_from_xml: str = root.find(
        ".//CessionarioCommittente/DatiAnagrafici/Anagrafica/Denominazione"
    ).text.replace(".", "")
    customer_name: str = shorten_customer_name(customer_name_from_xml).replace(" ", "_")
    name: str = "FATT_NR_" + invoice_nr + "_" + customer_name

    dbs: elemTree.Element | None = root.find(".//DatiBeniServizi")
    dl: list[elemTree.Element] = dbs.findall("DettaglioLinee")

    # Remove last element -useless in this XML file-
    dl.pop(len(dl) - 1)

    for node in dl:
        a_id.append(node.find("Descrizione").text.partition(" ")[0])

    print("Done!")
    return dl, a_id, name


def shorten_customer_name(c_name: str) -> str:
    """
    Get shortened customer name.

    Parameters:
        c_name (str): customer name found in XML file

    Returns:
        str: customer name with improved readability
    """

    with open(resource_path("customers.csv"), "r", encoding="utf-8-sig") as f:
        reader = list(csv.DictReader(f))
        for row in reader:
            if row["original_customer_name"] == c_name:
                return row["shown_customer_name"]
        return "na"


def make_df(dl) -> pd.DataFrame:
    """
    Create Pandas DataFrame.

    Parameters:
        dl (list[Element]): list of elements from XML file

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

    for node in dl:
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

    ean: list[str] = list()
    with open(resource_path("barcodes.csv"), "r", encoding="utf-8-sig") as f:
        reader = list(csv.DictReader(f))
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


def make_xlsx(f_name: str, out_xlsx: Path, df: pd.DataFrame) -> pd.ExcelWriter:
    """
    Create Excel file.

    Parameters:
        f_name (str): name of output Excel file to be created
        out_xlsx (Path): path of output Excel file
        df (DataFrame): values to be converted into Excel

    Returns:
        ExcelWriter: object for writing DataFrame into Excel sheets
    """

    print("Creating '" + f_name + ".xlsx'...")
    writer: pd.ExcelWriter = pd.ExcelWriter(out_xlsx, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Codici EAN Fattura")
    return writer


def format_xlsx(df: pd.DataFrame, wr):
    """
    Improve Excel file formatting.

    Parameters:
        df (DataFrame): values to be converted into Excel
        wr (ExcelWriter): object for writing DataFrame into Excel sheets
    """

    print("Formatting file...")

    # Define formats for Excel workbook
    workbook = wr.book
    worksheet = wr.sheets["Codici EAN Fattura"]
    format_header = workbook.add_format(
        {"align": "center", "bold": True, "border": 1, "fg_color": "#d9d9d9"}
    )
    format_float = workbook.add_format({"align": "center", "num_format": "€ #,##0.00"})
    format_int = workbook.add_format({"align": "center"})
    format_pct = workbook.add_format({"align": "center", "num_format": "0%"})

    # Auto-adjust columns' width
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        if column_width < 5:
            column_width = 5
        col_idx = df.columns.get_loc(column)
        worksheet.set_column(col_idx, col_idx, column_width)

    # Format columns
    for col_num, val in enumerate(df.columns.values):
        worksheet.write(0, col_num, val, format_header)  # header
    worksheet.set_column("C:C", None, format_int)  # quantity
    worksheet.set_column("D:D", None, format_float)  # unit price
    worksheet.set_column("E:E", None, format_float)  # total price
    worksheet.set_column("F:F", None, format_pct)  # VAT

    wr.close()
    print("File Excel created!")
