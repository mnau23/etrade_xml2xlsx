"""
GUI entrypoint.
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from logic.runner import run_xml2xlsx

# Colors
DEFAULT = "#707070"  # #6F9A84
ERROR_COLOR = "#F00"
# Fonts
FONT = "Helvetica"
HEADER = (FONT, 18, "bold")
CONTENT = (FONT, 14)
FOOTER = (FONT, 12)
ERROR_FONT = (FONT, 14, "bold")
# Geometry
WIDTH = 700
HEIGHT = 260


# pylint: disable=too-many-instance-attributes
class Xml2XlsxGUI:
    """
    GUI main class.
    """

    def __init__(self):
        self.root = tk.Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - WIDTH) / 2
        y = (screen_height - HEIGHT) / 2
        self.root.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x, y))  # pylint: disable=C0209
        # self.root.resizable(False, False)
        self.root.title("Xml2Xlsx")
        self.file_path = None

        # Header
        self.header = tk.Frame(self.root, height=50, bg=DEFAULT)
        self.header.pack(fill=tk.X)
        self.header_label = tk.Label(
            self.header, text="Invoice Converter", font=HEADER, bg=DEFAULT
        )
        self.header_label.pack(pady=10)

        # Content
        self.content = tk.Frame(self.root)
        self.content.pack(fill=tk.X)
        self.open_button = tk.Button(
            self.content, text="Open File", cursor="hand2", command=self.open_file
        )
        self.open_button.pack(pady=20)
        self.file_path_label = tk.Label(self.content, text="")
        self.file_path_label.pack(pady=5)
        self.process_button = tk.Button(
            self.content, text="Start Process", cursor="hand2", command=self.start_process
        )
        self.process_button.pack(pady=20)

        # Footer
        self.footer = tk.Frame(self.root, height=50, bg=DEFAULT)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.footer_label = tk.Label(
            self.footer,
            text="Copyright © mnau23. All Rights Reserved.",
            font=FOOTER,
            bg=DEFAULT,
        )
        self.footer_label.pack(pady=10)

        # Loop
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # pylint: disable=missing-function-docstring
    def open_file(self):
        selected_file = filedialog.askopenfilename(
            initialdir="~", title="Choose XML", filetypes=(("XML Files", "*.xml"),)
        )
        if selected_file != "":
            self.file_path_label.config(
                text=f'Ready to convert: "{selected_file}"', font=CONTENT
            )
            self.file_path = selected_file
        else:
            self.file_path_label.config(
                text="No file selected!", font=ERROR_FONT, foreground=ERROR_COLOR
            )

    # pylint: disable=missing-function-docstring
    def start_process(self):
        if self.file_path is not None:
            run_xml2xlsx(file_path=Path(self.file_path))
            self.file_path = None  # reset file_path after the process is completed
            self.file_path_label.config(text="File path cleared.", font=CONTENT)
        else:
            # self.file_path_label.config(
            #     text="Please select a file first!",
            #     font=ERROR_FONT,
            #     foreground=ERROR_COLOR,
            # )
            messagebox.showerror(title="No File!", message="You didn't select any file!")

    # pylint: disable=missing-function-docstring
    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    Xml2XlsxGUI()
