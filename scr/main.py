#!/usr/bin/env python3
import pikepdf
from pikepdf import Name, Dictionary, Array
from outline_model import OutlineElement, getNumber, getExistingStart
from importlib.metadata import version
import argparse
import re

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not greater than 0")
    return ivalue

def getArgs(args_input=None):
    # general attributes
    parser = argparse.ArgumentParser(
        prog="PDF_outline_add",
        description="Manipulate PDF outline and logical page labels"
        )
    subparsers = parser.add_subparsers(dest="mode", help="Mode of operation: write, extract")
    parser.add_argument('-v', '--version', action='version', version=version('PDF_tools_outline'))
    
    # writer attributes
    writer_parser = subparsers.add_parser("write", help="Write mode: write the outline from a text file to a PDF")
    writer_parser.add_argument("outline_file", help="Path to outline text file")
    writer_parser.add_argument(dest="input_pdf_file", help="Path to input PDF", nargs='?')
    writer_parser.add_argument("-o", "--output", metavar="<path>", dest="output_file", help="Path to output PDF, default: overwrite file", required=False, default=None)
    writer_parser.add_argument("-s", "--start", action="store", dest="first_page", metavar="<number>", type=check_positive, help="First real page number (1-based). Defaults to first arab number page number in the outline file.", required=False, default=None)
    writer_parser.add_argument("-d", "--dry", action="store_true", help="Print the parsed index")
    writer_parser.add_argument("--debug", action="store_true", help="Enable debug output")
    writer_parser.add_argument("--input-tabsize", "-it", dest="input_tabsize", metavar="<number>", type=check_positive, help="Number of spaces corresponding to a tab in the outline file, default: 1", required=False, default=1)
    writer_parser.add_argument("--output-tabsize", "-ot", dest="output_tabsize", metavar="<number>", type=check_positive, help="Number of spaces corresponding to a tab in the parsed output, default: 1", required=False, default=1)


    # extractor attributes
    extractor_parser = subparsers.add_parser("extract", help="Extract mode: extract the outline from a PDF and save it in a text file")
    extractor_parser.add_argument("input_pdf_file", help="Path to input PDF")
    extractor_parser.add_argument("-o", "--output", metavar="<path>", dest="output_file", help="Path to extracted outline file, default: outline.txt", required=False, default="outline.txt")
    extractor_parser.add_argument("--debug", action="store_true", help="Enable debug output")
    extractor_parser.add_argument("-s", "--start", help="specify book start page different from the one in the pdf. If not specified defaults to PDF's one", default=None, dest="start", type=check_positive, required=False)
    extractor_parser.add_argument("--tabsize", "-t", dest="tabsize", metavar="<number>", type=check_positive, help="Number of spaces corresponding to a tab in the outline file, default: 1", required=False, default=1)

    args = parser.parse_args(args_input)
    if args.mode == "write":
        if not args.dry and not args.input_pdf_file:
            raise SystemExit("PDF_outline_add write: error: the following arguments are required: input_pdf_file")
    return args

def parseOutline(file_outline, start=1, args=None):
    r_entry = r"^(\s*)(([ivxlcdmIVXLCDM]||\d)+)\s+(.*?)\s*$"          # Outline entry regex 
    outline_items = []
    with open(file_outline, 'r') as f:
        lines = [line.rstrip() for line in f.readlines() if not (line == '' or line == '\n' or line == '\r')]
        prev = 0
        par = None
        syntax = re.compile(r_entry)
        for line in lines:
            parts = syntax.match(line).groups()
            if len(parts) >= 3 and parts[1] != '' and parts[3] != '' :
                title = parts[3]
                if start is None:   # start hasn't been specified
                    try:
                        _ = int(parts[1])+1 # if the page number is the first arab number use prev page+1 as start page number
                        start = outline_items[-1].page_number+1 if len(outline_items) > 0 else 1 # if there are no previous items start from 1
                    except ValueError:
                        pass
                page_number = getNumber(parts[1], start or 1)   # get page number with start fallback to 1
                level = int(parts[0].count(' '*args.input_tabsize))   # get level from indentation
                if args and args.debug:
                    print("title: %s, page number: %s, level: %s, prev: %s" % (title, page_number, level, prev))
                if level == 0:
                    outline_items.append(OutlineElement(title, level, page_number))
                    if start == None:
                        outline_items[-1].set_preface()
                    par = outline_items[-1]
                elif level - prev < 2 or level <= prev:
                    while(prev >= level):
                        prev -= 1
                        par = par.parent
                    par.add_child(OutlineElement(title, level, page_number, par))
                    if start == None:
                        par.children[-1].set_preface()
                    par = par.children[-1]
                else:
                    raise Exception("Error: the difference between the next subsection level and this one must not be bigger than one: page title: %s, page number: %s, level: %s\n%s" % (title, page_number, level, prev))
                prev = level
            else:
                raise Exception("Error: line does not match the expected format: %s" % line)

    # stampo l'indice parsato (debug)
    if args and args.dry:
        for item in outline_items:
            if args.output_tabsize is not None:
                item.set_tabsize(args.output_tabsize)
            print(repr(item))

    return outline_items

def addLogicNums(pdf, start):
    if start is None:
        start = 1
    # inserisco numerazione logica con numeri romani
    # Creiamo la struttura dei numeri di pagina (PageLabels)
    # /Nums è un array dove ogni coppia è: [indice_pagina_inizio, dizionario_stile]
    # L'indice parte da 0 (0 = prima pagina del PDF)
    if start > len(pdf.pages):
        raise IndexError("Error: the first real page number is bigger than the total number of pages in the PDF: %s > %s" % (start, len(pdf.pages)))
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
    if args.mode == "write":
        if not args.dry:
            file_input = args.input_pdf_file
        start = args.first_page
        file_outline = args.outline_file
        file_output = args.output_file or args.input_pdf_file

        # parsing indice
        outline_items = parseOutline(file_outline, start, args)

        if not args.dry:
            with pikepdf.open(file_input, allow_overwriting_input=bool(file_input == file_output)) as pdf:
                # inserisco numerazione logica con numeri romani
                addLogicNums(pdf, start)
                # scrivo indice da file
                writeOutline(pdf, outline_items)
                # Salva il nuovo file
                pdf.save(file_output)

            print(f"File salvato con successo come: {file_output}")
        exit(0)

    elif args.mode == "extract":
        file_input = args.input_pdf_file
        file_output = args.output_file

        outline_items = []
        with pikepdf.open(file_input) as pdf:
            start = getExistingStart(pdf, args.start)
            with pdf.open_outline() as outline:
                for item in outline.root:
                    outline_items.append(OutlineElement.from_OutlineItem(item, pdf, start=start))
                    outline_items[-1].set_tabsize(args.tabsize)
        if not args.debug:
            with open(file_output, 'w') as f:
                for item in outline_items:
                    f.write(repr(item) + "\n")
            print(f"Outline estratto con successo in: {file_output}")
        else:
            for item in outline_items:
                print(repr(item))
            print("Outline estratto con successo")
    else:
        raise SystemExit("Error: invalid mode, must be 'write' or 'extract'", 2)

if __name__ == "__main__":
    main()