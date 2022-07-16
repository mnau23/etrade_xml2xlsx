#!/usr/bin/env python3

import os.path
import ntpath
import xml.etree.ElementTree as ElTree
import csv
import pandas as pd
# import openpyxl

ean_file = 'barcodes.csv'
customer_file = 'customers.csv'


# Get XML data
def parse_xml(fp):
    print("Retrieving data from XML file '" + ntpath.basename(fp).partition(".")[0] + "'...")

    # List with only the article's id (full description = id + description)
    a_id = list()

    # XML structure
    tree = ElTree.parse(fp)
    root = tree.getroot()

    invoice_nr = root.find('.//DatiGenerali/DatiGeneraliDocumento/Numero').text
    customer_name_from_xml = root.find('.//CessionarioCommittente/DatiAnagrafici/Anagrafica/Denominazione')\
        .text.replace(".", "")
    customer_name = shorten_customer_name(customer_name_from_xml).replace(" ", "_")
    name = "FATT_NR_" + invoice_nr + "_" + customer_name

    dbs = root.find('.//DatiBeniServizi')
    dl = dbs.findall('DettaglioLinee')

    # Remove last element -useless in this XML file-
    dl.pop(len(dl) - 1)

    for node in dl:
        a_id.append(node.find('Descrizione').text.partition(' ')[0])

    print("Done!")
    return dl, a_id, name


# Find shortened customer name in file
def shorten_customer_name(c_name):
    with open(customer_file, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        for row in reader:
            if row['original_customer_name'] == c_name:
                return row['shown_customer_name']
        return "na"


# Create Pandas DF
def make_df(dl):
    # Pandas DF structure
    df_cols = ['barcode', 'full_description', 'quantity', 'unit_price', 'total_price', 'VAT']
    rows = []

    for node in dl:
        s_desc = node.find('Descrizione').text
        s_qty = node.find('Quantita').text
        s_unit = node.find('PrezzoUnitario').text
        s_total = node.find('PrezzoTotale').text
        s_vat = node.find('AliquotaIVA').text
        rows.append({'full_description': s_desc, 'quantity': s_qty, 'unit_price': s_unit,
                     'total_price': s_total, 'VAT': s_vat})

    out_df = pd.DataFrame(rows, columns=df_cols)

    # Some conversions
    out_df['quantity'] = out_df['quantity'].astype(float).astype(int)
    out_df['unit_price'] = out_df['unit_price'].astype(float)
    out_df['total_price'] = out_df['total_price'].astype(float)
    out_df['VAT'] = out_df['VAT'].astype(float)/100

    return out_df


# Search EAN for each item
def get_ean(id_list):
    ean = list()
    with open(ean_file, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        for i in id_list:
            barcode = ''
            for row in reader:
                # If article_id (row[0]) of ean_file is in id_list and
                # barcode (row[1]) is not empty, get the barcode
                if row['article_id'] == i and row['barcode']:
                    barcode = row['barcode']
            # If barcode is found, add it to the list. Otherwise add "n/a"
            if barcode:
                ean.append(barcode)
            else:
                ean.append("n/a")
    return ean


# Convert CSV to Excel using OpenPyXL
# def create_xlsx(csv_path):
#    wb = openpyxl.Workbook()
#    ws = wb.active
#    out_xlsx = os.path.dirname(csv_path) + "\\" + ntpath.basename(csv_path).partition(".")[0] + ".xlsx"
#    print("Writing data on XLSX file...")
#    with open(ntpath.basename(csv_path), 'r') as f:
#        for row in csv.reader(f):
#            ws.append(row)
#    wb.save(out_xlsx)
#    print("Done!")


# Create XLSX file
def make_xlsx(fname, out_xlsx, df):
    # --- OR using OpenPyXL: create_xlsx(os.path.abspath(output_csv))
    print("Creating '" + fname + ".xlsx'...")
    writer = pd.ExcelWriter(out_xlsx, engine='xlsxwriter')
    df.to_excel(writer, index=False, encoding='utf-8', sheet_name='Codici EAN Fattura')
    return writer


# Format XLSX file
def format_xlsx(df, wr):
    print('Formatting file...')

    # Cell formats
    workbook = wr.book
    worksheet = wr.sheets['Codici EAN Fattura']
    format_header = workbook.add_format({
        'align': 'center',
        'bold': True,
        'border': 1,
        'fg_color': '#d9d9d9'
    })
    format_float = workbook.add_format({
        'align': 'center',
        'num_format': '#0.00'
    })
    format_int = workbook.add_format({
        'align': 'center'
    })
    format_pct = workbook.add_format({
        'align': 'center',
        'num_format': '0%'
    })
    for col_num, val in enumerate(df.columns.values):
        worksheet.write(0, col_num, val, format_header)  # header
    worksheet.set_column('C:C', None, format_int)  # quantity
    worksheet.set_column('D:D', None, format_float)  # unit price
    worksheet.set_column('E:E', None, format_float)  # total price
    worksheet.set_column('F:F', None, format_pct)  # VAT

    # Auto-adjust columns' width
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        if column_width < 5:
            column_width = 5
        col_idx = df.columns.get_loc(column)
        worksheet.set_column(col_idx, col_idx, column_width)

    wr.save()
    print("File Excel created!")


def main():
    file_path = input("Enter XML file path to convert...\n")

    # Check if file is an XML
    while ntpath.basename(file_path).partition(".")[2] != 'xml':
        file_path = input("Not an XML file. Enter a correct path...\n")

    # Get XML data
    details, art_ids, file_name = parse_xml(file_path)

    # Create Pandas DF
    data_frame = make_df(details)

    # Search EAN for each item
    art_barcodes = get_ean(art_ids)

    # Add it to the DF
    data_frame['barcode'] = art_barcodes

    # Create CSV file, if needed
    # output_csv = file_name + ".csv"
    # print("Creating '" + output_csv + "'...")
    # data_frame.to_csv(output_csv, index=False, encoding='utf-8')
    # print("File CSV created!")

    # Create XLSX file
    output_xlsx = os.path.dirname(file_path) + "\\" + file_name + ".xlsx"
    writer = make_xlsx(file_name, output_xlsx, data_frame)

    # Format XLSX file
    format_xlsx(data_frame, writer)


if __name__ == '__main__':
    main()
