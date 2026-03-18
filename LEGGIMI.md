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
Cloniamo il repo e installiamo gli hooks. Potrebbe essere necessario dare i permessi di esecuzione agli hooks.
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
## Testare
Questo progetto è dotato di test automatizzati. Si tratta di `unittest` scritti nella cartella `tests/`. Questi sono configurati per essere eseguiti prima di ogni commit e push tramite gli `hooks`. Il materiale utilizzato nei test è descritto in questo [file](./tests/tests_description.md).
## Pubblicare
Un workflow automatico analizza se ci sono dei tag sul main e, in tal caso pubblica la versione corrispondente.

Notare che gli hooks sono configurati per permettere di eseguire un push con tag sul main soltanto se vengono superati tutti gli unittests.

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
PDF_outline_add [file_input.pdf] [file_indice] [file_output.pdf] --start [prima_pagina]
```
dove `file_input` è il pdf che si vuole lavorare, `prima_pagina` è il numero della prima pagina effettiva nella numerazione "sbagliata", `file_indice` è il file dove è scritto l'indice e `file_output` è il nome che si vuole dare al file finito.
il file dell'indice ha la seguente sintassi
```
[pagina inizio] [nome capitolo]
```
E eventuali sezioni/sottosezioni sono indicate anteponendo uno spazio per cambiare il "livello":
```
1 primo capitolo
 2 sezione 1.1
 3 sezione 1.2
  paragrafo
...
```
eventuali pagine antecedenti all'inizio del libro vengono indicate con i numeri romani:
```
i prefazione
v indicie
1 inizio libro
...
```
## Gemini Gem
Per costruire il file dell'indice risulta molto efficace creare un `Agent` personalizzato di Gemini(Gem). Per fare ciò fornire il [prompt](./prompt.txt).