
### Example 1: Convert PySide6 app to exe with Pyinstaller 

<img width="371" alt="multimedia" src="https://github.com/ip-repo/guides/assets/123945379/4a05bb2a-0e03-4134-977e-319b724b6778">

First lets download the examples and install the modules we need.
Its important to use a virtual environment when using pyinstaller and also make sure to use a pyside6 version that come from the venv
and not from the system main python it might create some bugs.

```console
git clone
python -m venv convert_venv
pip install PySide6
pip install pyinstaller
cd guides/example-pyinstaller/pyside6_example_1
```
So you are inside the pyside6 example directory and we can use pyinstaller to create a exe from the project.<br>
The structure of the project directory look something like this:

```console
assets
main.py
```
The `assets` directory holds the app images so we will need a way to inform pyinstaller to inculde that directory when creating the exe.<br>
In the script we will create a function that handles paths so that the porgram will able to find to paths to app assets either when runed 
as a script or as an exe.

When the exe bootloader start his work he create a temporary folder and assign it as his base path and when the the script is runed as script
we just use the script base path joined with the relative path of a resource if needed.

```python
def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        print("error", Exception)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
....
image_path = resource_path(relative_path="assets\\mic.png")
````
Now we can use pyinstaller make sure you in the same directory as `media_devices.py`.
```cosnole
pyinstaller --onefile -w --clean --add-data "assets:assets" --icon=app.ico  media_devices.py
```
You will be able to find the exe version in the directory `dist` andit will be named `media_devices.exe`

<a href="https://pyinstaller.org/" >If you want to learn more about pyinstaller your can click here</a>
