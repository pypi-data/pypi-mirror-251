import pdfriend.classes.wrappers as wrappers


def swap(infile: str, page_num_0: int, page_num_1: int, outfile: str):
    pdf = wrappers.PDFWrapper.Read(infile)

    pdf.swap_pages(page_num_0, page_num_1)

    pdf.write(outfile)
