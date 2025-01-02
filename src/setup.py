"""
MacOS builder.
"""

from setuptools import setup

APP_NAME = "Xml2Xlsx"
VERSION = "0.1.0"
DATA_FILES = [("assets/csv", ["assets/csv/barcodes.csv", "assets/csv/customers.csv"])]
OPTIONS = {
    "argv_emulation": False,
    "iconfile": "assets/icon_512x512@2x@2x.icns",
    "plist": {
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleVersion": VERSION,
        "CFBundleShortVersionString": VERSION,
        "NSHumanReadableCopyright": "GPL v3",
    },
}

setup(
    name=APP_NAME,
    app=["src/gui.py"],
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
