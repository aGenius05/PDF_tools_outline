#!/usr/bin/env python3
import pikepdf
from pikepdf import Name, Dictionary, Array
from .outline_model import OutlineElement, getNumber
import argparse
import re

def getArgs():
    parser = argparse.ArgumentParser(
        prog="PDF_outline_add",
        description="Add PDF outline and logical page labels"
    )

    parser.add_argument("input_pdf_file", help="Path to input PDF")
    parser.add_argument("first_page", type=int, help="First real page number (1-based)")
    parser.add_argument("outline_file", help="Path to outline text file")
    parser.add_argument("output_pdf_file", help="Path to output PDF")

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print the parsed index"
    )

    return parser

def parseOutline(file_outline, start=1, args=None):
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
                if args and args.debug:
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
    if args and args.verbose:
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
    args = getArgs().parse_args()
    file_input = args.input_pdf_file
    start = args.first_page
    file_outline = args.outline_file
    file_output = args.output_pdf_file

    # parsing indice
    outline_items = parseOutline(file_outline, start, args)

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