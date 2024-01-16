import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.platforms as platforms
import pathlib

def split(infile: str, slice_str: str, outdir: str):
    pdf = wrappers.PDFWrapper.Read(infile)

    split_indices = pdf.slice(slice_str)
    if 1 not in split_indices:
        split_indices = [1] + split_indices
    if pdf.len() not in split_indices:
        split_indices.append(pdf.len())

    outdir_path = pathlib.Path(outdir)
    platforms.ensuredir(outdir_path)
    outfile = outdir_path.joinpath(pathlib.Path(infile).stem)

    ndigits = len(str(len(split_indices) - 1))

    for i, (lower, upper) in enumerate(zip(
        split_indices[:-1], split_indices[1:]
    )):
        pdf_slice = wrappers.PDFWrapper(pdf.pages[(lower-1):(upper-1)])
        pdf_slice.write(f"{outfile}-{i:0{ndigits}}.pdf")
