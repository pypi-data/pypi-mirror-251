import pdfriend.classes.wrappers as wrappers


def remove(infile: str, slice_str: str, outfile: str):
    pdf = wrappers.PDFWrapper.Read(infile)

    for page in pdf.slice(slice_str):
        pdf.pop_page(page)

    pdf.write(outfile)
