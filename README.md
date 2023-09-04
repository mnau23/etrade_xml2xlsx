# Xml2Xlsx

[![code style: black](https://img.shields.io/badge/code%20style-black-39f)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-39f)](https://github.com/pylint-dev/pylint)
[![security: bandit](https://img.shields.io/badge/security-bandit-39f)](https://github.com/PyCQA/bandit)

> Small project to convert an XML file
> ([Fattura Elettronica](https://www.agid.gov.it/it/piattaforme/fatturazione-elettronica))
> into an Excel file.

## Usage

Run `python src/main.py`

### Build executable with PyInstaller on Windows

In order to build and create an executable for this project, you have to run the following command.\
**NB**: Option `--add-data` loads some required non-binary files into the executable.

```bash
cd src
python -m PyInstaller --add-data 'files/;.' --onefile main.py
```

Finally, the `.exe` file will be available in `src/dist/` folder.

## License

**[GPL v3](https://www.gnu.org/licenses/gpl-3.0)** - Copyright 2021 &copy; [mnau23](https://mnau23.github.io/)
