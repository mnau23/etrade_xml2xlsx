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

## Build

### MacOS

_py2app_ was used in order to build and create a MacOS app for this project.

**Debug**: `python src/setup.py py2app -A` \
**Release**: `python src/setup.py py2app`

In both cases, the app will be available in `dist/` folder.

**Create DMG**

Once the release version is ready:
- install `brew install create-dmg`
- run
  ```sh
  mkdir -p dist/dmg
  cp -r "dist/Xml2Xlsx.app" dist/dmg
  create-dmg --volname "Xml2Xlsx" --volicon "assets/icon_512x512@2x@2x.icns" --window-pos 200 120 \
    --window-size 600 300 --icon-size 100 --icon "Xml2lsx.app" 175 120 \
    --hide-extension "Xml2Xlsx.app" --app-drop-link 425 120 "dist/Xml2Xlsx.dmg" "dist/dmg/"
  ```

### Windows

(Currently disabled)

_PyInstaller_ was used in order to build and create an executable for this project. \
**NB**: Option `--add-data` loads some required non-binary files into the executable.

```bash
python -m PyInstaller --add-data 'files/;.' --onefile src/cli.py
```

Finally, the `.exe` file will be available in `dist/` folder.

## License

**[GPL v3](https://www.gnu.org/licenses/gpl-3.0)** - Copyright 2021 &copy; [mnau23](https://mnau23.github.io/)
