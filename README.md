# Xml2Xlsx

[![code style: black](https://img.shields.io/badge/code%20style-black-39f)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-39f)](https://github.com/pylint-dev/pylint)
[![security: bandit](https://img.shields.io/badge/security-bandit-39f)](https://github.com/PyCQA/bandit)

> Small project to convert an XML file
> ([Fattura Elettronica](https://www.agid.gov.it/it/piattaforme/fatturazione-elettronica))
> into an Excel file.

## Usage

The app is available both as CLI and as GUI, respectively run:

- `python src/cli.py`
- `python src/gui.py`

### Build executable with PyInstaller on Windows

In order to build and create an executable for this project, you have to run the following command.\
**NB**: Option `--add-data` loads some required non-binary files into the executable.

```bash
python -m PyInstaller --add-data 'files/;.' --onefile src/cli.py
```

Finally, the `.exe` file will be available in `dist/` folder.

## License

**[GPL v3](https://www.gnu.org/licenses/gpl-3.0)** - Copyright 2021 &copy; [mnau23](https://mnau23.github.io/)
