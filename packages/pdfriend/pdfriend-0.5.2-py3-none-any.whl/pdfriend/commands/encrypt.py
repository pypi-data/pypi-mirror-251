import getpass
import pdfriend.classes.wrappers as wrappers

def encrypt(infile: str, outfile: str):
    password = getpass.getpass("password: ")
    # if the input doesn't get overwritten, there's no need to
    # double check the password
    if infile == outfile:
        confirmation = getpass.getpass("repeat the password: ")
        if password != confirmation:
            print("the passwords don't match!")
            return

    pdf = wrappers.PDFWrapper.Read(infile)

    writer = pdf.to_writer()
    writer.encrypt(password)
    writer.write(pathlib.Path(outfile).with_suffix(".pdf"))

