# PDF-outline-adder
Un semplice strumento CLI ideato per tutti quegli studenti che nel tentativo di risparmiare un po' di peso nello zaino si convertono al digitale ma "trovano" soltanto pdf senza indice e soprattutto con una numerazione sfalsata a causa di indice, prefazione e quant altro.

## Installazione
### pipx


## Development
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
- [ ] implementare unittest
- [ ] scrivere istruzioni per installare con `pipx`
- [ ] documentare meglio
- [ ] implementare CI/CD per creare requirements, testare, buildare e pubblicare
- [ ] informazioni giuste riguardo alla versione
- [ ] controllare che i file esistano