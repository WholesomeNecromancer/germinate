# germinate

`germinate` is a lightweight packaging tool that leverages [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/index.html) to create OS-dependent executable binaries from Python code. This makes Python code even more portable by encasing your code in an OS-native application with the Python interpreter used to run `germinate.py`.

>PyInstaller has many features; germinate is currently a convenient wrapper for a very small subset of PyInstaller's potential.

>***NOTE*** germinate creates intermediary files and folders in the working directory which it deletes upon completion.

## Usage
germinate is a python file and must be used with a python3 interpreter.
*Originally tested with v3.7.x*
`python germinate.py myapp.py`

>TODO: coming soon:
`python -m germinate myapp.py`

Only the Python file that serves as your app's main entrypoint need be specified.

>**A note on hidden dependencies** - some Python modules, even in public packages, do not express all of their import directives in a way that PyInstaller can understand. It is imperative that you test your app after building to ensure all necessary Python dependencies were included. The missing dependencies should be easy to diagnose based on error output from the interpreter.

## Confyg files
germinate's behavior is defined in a `-confyg.json` file defined alongside your app's entrypoint Python module. germinate detects this file automatically - just name it after your app.

e.g. `foo.py` is germinated into `foo.exe` by behavior defined in `foo-confyg.json`

>**NOTE:** you may specify an alternative confyg json file via `-c=` or `--confyg=` which does not need to conform to the naming convention.

### app-name
`string`
The desired name of your final app; does not need to match the Python entrypoint's module name.

### create-dirs
`list` of `string`
Any directories that `germinate` should create alongside the finished binary.

### copy-dirs
`list` of `string`
Any directories that `germinate` should copy alongside the finished binary.

### copy-files
`list` of `string` any files that `germinate` should copy alongside the finished binary. *global-config.json* is commonly copied.

### one-file
`boolean`
Whether to create a single executable binary (.exe on Windows) or keep resources for the binary unpacked in the same directory. `True` provides the simplest, most straightforward output.

### confyg
`string`; file path
An alternative confyg file (i.e. other than `yourapp-confyg.json`) to use to `germinate` your app.

### output-dir
`string`
A top-level directory in which to place `germinate`'s final output. `foo/foo.exe` by default.

Apps are placed in nested directories with the app's name: `foo.exe` with an `output-dir` of `built` is placed in `./built/foo/`

e.g.
`python germinate.py foo.py --output-dir=built` yields:
```
foo.py                  # App's Python source code
foo-confyg.json         # App's germinate confyg file
built/                  # Specified as output-dir
built/foo
built/foo/foo.exe       # Windows binary
```

### Confyg Example: `hello-world`

```
# hello_world-confyg.json
{
    "app-name": "hello-world",
    "onefile": "true",
    "create-dirs": [],
    "copy-dirs": [],
    "copy-files": [],
    "output-dir": "."
}
```

`./hello-world/hello-world.exe`
