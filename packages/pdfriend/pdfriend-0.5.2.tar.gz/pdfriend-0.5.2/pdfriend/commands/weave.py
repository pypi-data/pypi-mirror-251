import pdfriend.classes.wrappers as wrappers

def weave(infile_0: str, infile_1: str, outfile: str):
    pdf_0 = wrappers.PDFWrapper.Read(infile_0)
    pdf_1 = wrappers.PDFWrapper.Read(infile_1)

    weaved_pdf = pdf_0.weave_with(pdf_1)

    weaved_pdf.write(outfile)
