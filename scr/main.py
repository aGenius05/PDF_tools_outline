#!/usr/bin/env python3
import pikepdf
from pikepdf import Name, Dictionary, Array
from .outline_model import OutlineElement, getNumber
from sys import argv
import os
import re

def getArgs():
    if len(argv) != 5:
        print ('Usage: [input_pdf_file] [first_page] [outline_file] [output_pdf_file]\nMore @ https://github.com/agenius05/PDF-outline-adder')
        exit(-1)
        
    # argomenti
    start = int(argv[2])
    file_input = argv[1]
    file_outline = argv[3]
    file_output = argv[4]
    return start, file_input, file_outline, file_output

def parseOutline(file_outline, start=1, out_parsed_index=False):
    r_entry = r"^(\s*)(([ivxlcdm]||\d)+)\s+(.*?)\s*$"          # Outline entry regex 
    outline_items = []
    with open("%s" % file_outline, 'r') as f:
        lines = [line.rstrip() for line in f.readlines() if not (line == '' or line == '\n' or line == '\r')]
        prev = 0
        par = None
        for line in lines:
            parts = re.match(r_entry, line).groups()
            if len(parts) >= 3:
                title = parts[3]
                page_number = getNumber(parts[1], start)
                level = int(parts[0].count(' '))
                if os.environ.get("DEBUG") == "1":
                    print("title: %s, page number: %s, level: %s, prev: %s" % (title, page_number, level, prev))
                if level == 0:
                    outline_items.append(OutlineElement(title, level, page_number))
                    par = outline_items[-1]
                elif prev - level < 2 or level <= prev:
                    while(prev >= level):
                        prev -= 1
                        par = par.parent
                    par.add_child(OutlineElement(title, level, page_number, par))
                    par = par.children[-1]
                else:
                    raise Exception("Error: the difference between the next subsection level and this one must not be bigger than one: page title: %s, page number: %s, level: %s\n%s" % (title, page_number, level, prev))
                prev = level

    # stampo l'indice parsato (debug)
    if out_parsed_index:
        for item in outline_items:
            print(repr(item))

    return outline_items

def addLogicNums(pdf, start):
    # inserisco numerazione logica con numeri romani
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

def writeOutline(pdf, outline_items):
    # scrittura indice da file
    with pdf.open_outline() as outline:
        outline.root = []
        for item in outline_items:
            # Aggiungiamo l'item all'indice del PDF
            outline.root.append(item.returnNode())

def main():
    # prendo gli argomenti
    args = getArgs()
    start, file_input, file_outline, file_output = args # TODO: better way to do this? maybe with argparse?

    # parsing indice
    outline_items = parseOutline(file_outline, start, out_parsed_index=False)

    with pikepdf.open(file_input) as pdf:
        # inserisco numerazione logica con numeri romani
        addLogicNums(pdf, start)

        # scrivo indice da file
        writeOutline(pdf, outline_items)

        # Salva il nuovo file
        pdf.save(file_output)

    print(f"File salvato con successo come: {file_output}")
    exit(0)

if __name__ == "__main__":
    main()