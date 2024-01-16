
intro = """pdfriend: a command line utility for easily modifying PDF files
    usage: pdfriend [command] [arguments?] [-d|--debug?] (note that options in [] are required and options in [?] are not). Use -d or --debug for more detailed error messages.
    the following commands are available:
    """

outro = """use pdfriend help [command] to get the instructions for particular commands"""

help_blurbs = {
    "version":"""pdfriend version | -v | --version
    prints the current version of pdfriend
    """,
    "help": """pdfriend help [command?]
        display help message. If given a command, it will only display the help message for that command.
    """,
    "merge": """pdfriend merge [filename1] [filename2?] ... [-o|--outfile outfile?=pdfriend_output.pdf] [-q|--quality quality?=100]
        merge the given files into one pdf. It can handle multiple pdfs, as well convert and merge png and jpg images. Glob patterns are also supported. You can specify the output filename using the -o or --outfile flag, otherwise it defaults to pdfriend_output.pdf. You can also specify the quality when images are converted to pdfs via the -q or --quality flag. It's an integer going from 0 to 100, 100 is no lossy compression and 0 is full lossy compression.

    examples:
        pdfriend merge pdf1.pdf img.png pdf2.pdf -o merged.pdf
            merges all of those into merged.pdf, preserving the quality of img.png
        pdfriend merge folder_name/* -o merged.pdf -q 50
            merges all files in directory folder_name into merged.pdf and compresses the images by 50%.
        pdfriend merge pdf1.pdf folder_name/* img.jpg pdf2.pdf -o apricot.pdf
            merges every file given, including all files in folder_name, into apricot.pdf
    """,
    "split": """pdfriend split [filename] [pages] ... [-o|--outfile outfile?=pdfriend_output]
        split the given file at the given points. Every point is included in the part after, not before it.

        examples:
            pdfriend split in.pdf 5 -o parts
                splits in.pdf into one part with pages 1-4 and another with 5-end and puts them in a directory named parts
            pdfriend split input.pdf 4,7
                splits input.pdf into 3 parts, one has pages 1-3, another 4-6 and another 7-end and puts them in a directory named pdfriend_output
            pdfriend split thing.pdf 8-11
                splits thing.pdf into 4 parts, one has pages 1-7, another has page 8, the other page 9, the other page 10, and the other pages 11-end and puts them in a directory named pdfriend_output
            pdfriend split infile.pdf all -o pages
                splits infile.pdf into individual pages and puts them in a directory named pages
    examples:
        pdfriend merge pdf1.pdf img.png pdf2.pdf -o merged.pdf
            merges all of those into merged.pdf, preserving the quality of img.png
        pdfriend merge folder_name/* -o merged.pdf -q 50
            merges all files in directory folder_name into merged.pdf and compresses the images by 50%.
        pdfriend merge pdf1.pdf folder_name/* img.jpg pdf2.pdf -o apricot.pdf
            merges every file given, including all files in folder_name, into apricot.pdf
    """,
    "edit": """pdfriend edit [filename]
        edit the selected file in place, using a set of subcommands. After launching the edit shell, you can type h or help to list the subcommands.
    """,
    "invert": """pdfriend invert [filename] [-o|--outfile outfile?=pdfriend_output.pdf] [-i|--inplace?]
        create a PDF file with the pages of the input file, but in inverted order. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend invert puppy.pdf -o puppy-inv.pdf
                inverts the pages of puppy.pdf and saves to puppy-inv.pdf
            pdfriend invert kitty.pdf -i
                inverts the pages of kitty.pdf
    """,
    "clear": """pdfriend clear
        clears the pdfriend cache.
    """,
    "swap": """pdfriend swap [filename] [page_0] [page_1] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        swaps the specified pages in the PDF file. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend swap notes.pdf 1 3 -i
                swaps pages 1 and 3 in notes.pdf (modifies the file)
            pdfriend swap templ.pdf 6 3 -o new-templ.pdf
                swaps pages 6 and 3 and saves to new-templ.pdf
            pdfriend swap k.pdf 2 9
                swaps pages 2 and 9 and saves to pdfriend_output.pdf
    """,
    "remove": """pdfriend remove [filename] [pages] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        removes specified pages from the PDF file. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend remove input.pdf 6
                removes page 6 and saves to pdfriend_output.pdf
            pdfriend remove input.pdf 5,6,9 -o out.pdf
                removes pages 5,6,9 and saves to out.pdf
            pdfriend remove input.pdf 3-7 -o out
                removes pages 3 through 7 (INCLUDING 7) and saves to out.pdf
            pdfriend remove input.pdf 13,2,4-7,1 -i
                removes pages 1,2,4,5,6,7,13 from input.pdf (modifies the file)
    """,
    "weave": """pdfriend weave [filename_0] [filename_1] [-o|--outfile?=pdfriend_output.pdf]
        combines two PDFs such that the first fills the odd pages and the second the even pages of the output.

        examples:
            pdfriend weave inf0.pdf inf1.pdf
                weaves the two PDFs and saves the output to pdfriend_output.pdf
            pdfriend weave k.pdf l.pdf -o weaved.pdf
                weaves the two PDFs and saves the output to weaved.pdf
    """,
    "encrypt": """pdfriend encrypt [filename] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        creates an encrypted PDF file using a provided password. Adding -i or --inplace will make it so that the file itself is encrypted.

        examples:
            pdfriend encrypt not-sus.pdf -i
                encrypts not-sus.pdf in-place. Make sure you remember the password, as it will be overwritten!
            pdfriend encrypt balance.pdf -o balance-encrypted.pdf
                encrypts balance.pdf and saves to balance-encrypted.pdf.
            pdfriend encrypt acct.pdf
                encrypts acct.pdf and saves to pdfriend_output.pdf.
    """,
    "decrypt": """pdfriend decrypt [filename] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        decrypts an encrypted PDF file using a provided password. Adding -i or --inplace will make it so that the file itself is decrypted. If the file is not encrypted, it will just be copied.

        examples:
            pdfriend decrypt not-sus.pdf -i
                decrypts not-sus.pdf in-place.
            pdfriend decrypt balance.pdf -o balance-decrypted.pdf
                decrypts balance.pdf and saves to balance-decrypted.pdf.
            pdfriend decrypt acct.pdf
                decrypts acct.pdf and saves to pdfriend_output.pdf.
    """,
    "metadata": """pdfriend metadata [filename] [--get key?] [--set key_val_pairs?] [--pop keys?]
        manages PDF metadata. Using no extra flags, it will print the key-value pairs. You can use --get to print the value of a specific key and --set to set values for keys, or --pop to delete them.

        examples:
            pdfriend metadata some.pdf
                prints the metadata of some.pdf.
            pdfriend metadata thing.pdf --get /Author
                prints the name of the author of the PDF, if that field has been set.
            pdfriend metadata stolen.pdf --set /Author=me
                sets the author of stolen.pdf to "me". BEWARE: This will overwrite the PDF, unlike most of the other pdfriend commands.
            pdfriend metadata cnp.pdf --set  "/Title=Crime And Punishment"
                sets the title to that. Note that you need the quotes here, else your shell will interpret the words as different arguments.
            pdfriend metadata phys1.pdf --set "/Title=University Physics with Modern Physics,/Author=H. Young and R. Freedman"
                sets the author of phys1.pdf to "H. Young and R. Freedman" and its title to you-know-what.
            pdfriend metadata embarassing_fanfic.pdf --pop /Author
                removes (!) the PDF's author field.
            pdfriend metadata mystery.pdf --pop /Author,/Producer
                removes the PDF's author and producer fields.
    """
}


def help(command: str):
    try:
        print(help_blurbs[command])
    except KeyError:
        print(intro)
        print("\n".join([f"    {blurb}" for blurb in help_blurbs]), "\n")
        print(outro)
