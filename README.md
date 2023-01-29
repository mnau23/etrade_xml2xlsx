# Xml2Xlsx

> Small project to convert an XML file
> (Fattura Elettronica, <a href="https://www.agid.gov.it/it/piattaforme/fatturazione-elettronica" target="_blank">more info</a>)
> into an Excel file.


## Installation

1. Clone the repository
1. Install requirements
```bash
pip install -r requirements/requirements.txt
```


## Usage

Run `python src/main.py`


### Build executable with PyInstaller on Windows

In order to build and create an executable for this project, you have to run the following command.\
**NB**: Option `--add-data` loads some required non-binary files into the executable
(they must be saved under the root of the project).
```bash
cd src
python -m PyInstaller --add-data 'files/;.' --onefile main.py
```
Finally, the `.exe` file will be available in `src/dist/` folder.


## License

**[GPL v3](https://www.gnu.org/licenses/gpl-3.0)** - Copyright 2021 © 
<a href="https://mnau23.github.io/" target="_blank">mnau23</a>
