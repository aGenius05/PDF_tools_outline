#!./.venv/bin/python3
import pikepdf
from pikepdf import Name, Dictionary, Array
from sys import argv

if len(argv) != 5:
	print ('Arguments: input_pdf_file first_page outline_file output_pdf_file')
	exit(-1)
      
# argomenti
start = int(argv[2])
file_input = argv[1]
file_outline = argv[3]
file_output = argv[4]

# inserisco numerazione logica con numeri romani
with pikepdf.open(file_input) as pdf:
    # Creiamo la struttura dei numeri di pagina (PageLabels)
    # /Nums è un array dove ogni coppia è: [indice_pagina_inizio, dizionario_stile]
    # L'indice parte da 0 (0 = prima pagina del PDF)
    
    page_labels = Dictionary({
        "/Nums": Array([
            0, Dictionary({
                "/S": Name("/r"),  # Romano minuscolo
                "/St": 1
            }),
            (start-1), Dictionary({
                "/S": Name("/D"),  # Decimale (arabo)
                "/St": 1
            })
        ])
    	})

    # Inseriamo il dizionario nel 'Catalog' (la radice del PDF)
    pdf.Root.PageLabels = page_labels

	# scrittura indice da file

    # Salva il nuovo file
    pdf.save(file_output)

print(f"File salvato con successo come: {file_output}")