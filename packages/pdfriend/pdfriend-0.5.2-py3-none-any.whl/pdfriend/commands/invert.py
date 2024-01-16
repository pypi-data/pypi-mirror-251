import pdfriend.classes.wrappers as wrappers


def invert(infile: str, outfile: str):
    pdf = wrappers.PDFWrapper.Read(infile)

    pdf.invert()

    pdf.write(outfile)
