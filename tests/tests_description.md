# sample1
### input.pdf
It's a sample input file of **40 pages** with an **outline made only of chapters**
### index.txt
**empty** sample outline file
### pdf_ref.pdf
sample **output expected** from `input.pdf` and `index.txt`
### index_ref.txt
It's the outline file corresponding to **input.pdf's outline**
# sample2
### input.pdf
It's a sample input file of **40 pages** with an **outline made of chapters and paragraphs**
### index.txt
Sample outline file with **wrong syntax**
### index2.txt
Sample outline file with **word in place of chapter page number**
### index3.txt
Sample outline file with **decreasing page order**
### index_ref.txt
It's the outline file corresponding to **input.pdf's outline**
# sample3
### input.pdf
It's a sample input file of **25 pages** with an **outline made of everything**
### index.txt
**Only chapters** sample outline file
### index_ref.txt
It's the outline file corresponding to **input.pdf's outline**
### pdf_ref.pdf
sample **output expected** from `input.pdf` and `index.txt`
# sample4
### input.pdf
It's a sample input file of **36 pages** with an **outline made of everything and shifted(real start at page 9)**
### index.txt
**Chapters and paragraphs** sample outline file
### index_ref.txt
It's the outline file corresponding to **input.pdf's outline**
### pdf_ref.txt
sample **output expected** from `input.pdf` and `index.txt`
# sample5
### input.pdf
It's a sample input file of **35 pages** with **no outline**
### index.txt
**Complete** sample outline file
### pdf_ref.pdf
sample **output expected** from `input.pdf` and `index.txt`
### index_shifted.txt
**Complete** sample outline shifted with **start at page 2**
### index_ref_shifted.txt
Expected output of parsing stage with `index_shifted.txt` with **start at page 2**
### pdf_shifted_ref.pdf
sample **output expected** from `input.pdf` and `index_shifted.txt` with **start at page 2**
# sample6
### index.txt
sample outline file with **double forward indent**
# sample7
### input.pdf
It's a sample input file of **15 pages** with **no outline**
### index.txt
sample outline file with **double backward indent** and a section starting in a **non existing page**