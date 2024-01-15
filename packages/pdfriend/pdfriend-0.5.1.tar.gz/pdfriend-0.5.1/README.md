# Simple command line PDF editor

`pdfriend` is a simple command line program for editing PDF files at the page level (meaning it's able to manipulate pages, but not the content of said pages). It can, among other things:

- merge many PDFs, PNGs and JPGs into a single PDF
- split a PDF into different parts
- rotate PDF pages
- delete PDF pages
- change the order of pages in a PDF
- encrypt and decrypt PDFs
- see and edit PDF metadata

## Installation
The recommended way to install `pdfriend` is through [pipx](https://github.com/pypa/pipx). Simply run:
```sh
pipx install pdfriend
```
You need a working python 3.11 or newer installation.

Alternatively, you can install it as you would any other PyPI package, for example using pip:
```sh
pip install pdfriend
```

## Usage
To access instructions for the usage of `pdfriend`:
```sh
pdfriend help
```
As a quick overview:
### Merging PDFs and images
PDFs:
```sh
pdfriend merge doc0.pdf doc1.pdf -o output.pdf
```
Images:
```sh
pdfriend merge img0.png img1.jpg img2.png img3.png -o output.pdf
```
PDFs and images:
```sh
pdfriend merge doc0.pdf img0.png doc32.pdf -o comb.pdf
```
Glob patterns are also supported:
```sh
pdfriend merge input_dir/*.png -o output.pdf
```

### Editing PDFs
To edit a PDF file in place, enter the edit shell:
```sh
pdfriend edit doc.pdf
```
You can then use the edit subcommands, for example
```
rotate 12 90
```
To rotate page 12 by 90 degrees, or
```
delete 6
```
To delete page 6, or
```
swap 3 7
```
To swap pages 3 and 7, or
```
undo
```
To undo the previous command, etc. Use
```
help
```
To see all the available subcommands
