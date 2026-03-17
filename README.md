# PDF_tools_outline
Un semplice strumento CLI ideato per tutti quegli studenti che nel tentativo di risparmiare un po' di peso nello zaino si convertono al digitale ma "trovano" soltanto pdf senza indice e soprattutto con una numerazione sfalsata a causa di indice, prefazione e quant altro.

## Installazione
### uv
```bash
uv tool install PDF_tools_outline
```

### pipx
```bash
pipx install PDF_tools_outline
```
## Development
Cloniamo il repo e installiamo gli hooks
```bash
git clone https://github.com/aGenius05/PDF_outline.git
cp ./hooks/* .git/hooks
```

### uv
Si consiglia di utilizzare uv in quanto rende tutto molto più semplice
```bash
uv sync
uv pip install -e .
```
### Installazione manuale
In questo caso l'installazioen è più laboriosa, avrai bisogno di `python3`, la libreria `pikepdf`, che si consiglia di installare in un virtual environment tramite `pip3` eseguendo

```bash
python3 -m venv /path/to/venv/
source /path/to/venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```
infatti il file `requirements.txt` contiene la versione utilizzata da me quando ho sviluppato questo script, con quella sicuramente funzionerà.
## Pubblicare
Un workflow automatico analizza se ci sono dei tag sul main e, in tal caso pubblica la versione corrispondente. Notare che gli hooks sono configurati per permettere di eseguire un push con tag sul main soltanto se vengono superati tutti gli unittests.

É possibile anche pubblicare manualmente su PyPi utilizzando il comando
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
L'utilizzo è molto semplice, dopo aver attivato il venv:

```bash
PDF_outline_add [file_input.pdf] [prima_pagina] [file_indice] [file_output.pdf]
```
dove `file_input` è il pdf che si vuole lavorare, `prima_pagina` è il numero della prima pagina effettiva nella numerazione "sbagliata", `file_indice` è il file dove è scritto l'indice e `file_output` è il nome che si vuole dare al file finito.

## Gemini Gem
Per costruire il file dell'indice risulta molto efficace creare un `Agent` personalizzato di Gemini(Gem). Per fare ciò fornire il [prompt](./prompt.txt).

# TODO
- [ ] esporta indice esistente
- [ ] pagine doppie con numerazione giusta
- [ ] readme in più lingue