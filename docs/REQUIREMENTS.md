# Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/) installed globally

Optional (only for building & running the GUI):

- Tcl/Tk 8.6

## Troubleshooting

- Tcl/Tk: as of Dec 2024, v9 is not supported yet
- `pandas`: using the next version, the generated app crashes with `ModuleNotFoundError: No module named 'cmath'`
- `setuptools`: using the next version, the Py2App build crashes with `error: [Errno 17] File exists: [file path]`
