# PDF_tools_outline
A simple CLI tool made for all the students who started using PDFs instead of paper book in order to save some weight in their backpack but stumbled into the problem of missing outline and shifted page numbering cause by preface, index and other additions.

GUIDA IN ITALIANO [QUI](./LEGGIMI.md)
## How to install
### uv
```bash
uv tool install PDF_tools_outline
```

### pipx
```bash
pipx install PDF_tools_outline
```
## Development
Clone the repo and install the hooks. It may be necessary to give execution privileges to hooks files
```bash
git clone https://github.com/aGenius05/PDF_outline.git
cp ./hooks/* .git/hooks
```

### uv
It's recommended that you use uv cause it makes everything much simpler
```bash
uv sync
uv pip install -e .
```
### manual install
Manual installation is a bit trickier, you'll need `python3` and `pikepdf` module. You should install it in a virtual environment through `pip3`:

```bash
python3 -m venv /path/to/venv/
source /path/to/venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```
Indeed `requirements.txt` contains the version I used and it's guaranteed that it will work on you're computer too.
## Testing
This project has some automated tests written in the `tests/` dir. They are `unittest` tests and are configured to run before commits and pushes via the `hooks`. The material used in the tests is described in this [file](./tests/tests_description.md).
## Publishing
A Github Action is configured to look for commits on the main branch which also have a tag, build the package for those and publish them automatically on PyPi

Note that the hooks make it impossible to push to main tagged commit that haven't passed unittests first.

It's also possible to manually send a package version to PyPi using the command:
```bash
uv build
uv publish
```
oppure con pip
```bash
python3 -m build
python3 -m twine dist/*
```
## Utilizzo
The usage is very simple:
```bash
PDF_outline_add [file_input.pdf] [file_index] [file_output.pdf] --start [first_page]
```
where `file_input` is the inpput pdf, `first_page` is the number of the first page in the "wrong" ordering, `file_index` is the file where the outline lays and `file_output` is the output's file name.
The outline file has the following syntax
```
[starting page number] [section's name]
```
Subsections/paragraphs, if present, are written adding one additional space in front of their line:
```
1 first chapter
 2 section 1.1
 3 section 1.2
  paragraph
...
```
Pages befor the start of the "real" book, if present, are written using roman numeration:
```
i prefazione
v indicie
1 inizio libro
...
```
## Gemini Gem
To generate index file it's very useful having a custom `Agent` for Gemini(Gem). To do so give it the [prompt](./prompt.txt).

# TODO
- [ ] export index from existing pdf
- [ ] right numeration on pages with double pages
- [ ] --dry flag instead of --verbose
- [ ] --version flag