import pdfriend.classes.wrappers as wrappers
import pdfriend.classes.exceptions as exceptions
import pdfriend.classes.cmdparsers as cmdparsers
import pdfriend.classes.info as info
from pdfriend.classes.platforms import Platform
from pdfriend.classes.config import Config
import pdfriend.utils as utils
import pathlib
import re


whitespace_pattern = re.compile(r"\s+")

def parse_command_string(command_string: str) -> list[str]:
    return re.split(whitespace_pattern, command_string)

command_info = {
    "help": info.CommandInfo("help", "h", """[command?]
    display help message. If given a command, it will only display the help message for that command.

    examples:
        help rotate
            displays the help blurb for the rotate command
        help exit
            displays the help blurb for the exit command
    """),
    "exit": info.CommandInfo("exit", "e", """
    exits the edit mode
    """),
    "rotate": info.CommandInfo("rotate", "r", """[page_numbers] [angle]
    rotates page clockwise with the given numbers (starting from 1) by the given angle (in degrees). Can use negative angles to rotate counter-clockwise. DO NOT put extra spaces between the page numbers!

    examples:
        r 34 1.2
            rotates page 34 clockwise by 1.2 degrees
        r 1,3,8 -4
            rotates pages 1,3 and 8 counter-clockwise by 4 degrees
        r 3-18 90
            rotates pages 3 through 18 (INCLUDING 18) clockwise by 90 degrees
        r 1,13,5-7,2 54
            rotates pages 1,2,5,6,7,13 clockwise by 54 degrees
        r all -90
            rotates all pages counter-clockwise by 90 degrees
    """),
    "delete": info.CommandInfo("delete", "d", """[page_numbers]
    deletes all specified pages. DO NOT put extra spaces between the page numbers!

    examples:
        d 7
            deletes page 7
        d 4,8,1
            deletes pages 1, 4 and 8
        d 6-66
            deletes pages 6 through 66 (INCLUDING 66)
        d 4,17,3-6
            deletes pages 3,4,5,6 and 17
    """),
    "swap": info.CommandInfo("swap", "s", """[page_0] [page_1]
    swaps page_0 and page_1.
    """),
    "move": info.CommandInfo("move", "m", """[source] [destination]
    move source to BEFORE destination, taking its place.

    examples:
        m 3 17
            moves page 3 to page 17, pushing back the pages from 17 onward
        m 83 1
            moves page 83 to the beginning of the document
    """),
    "push": info.CommandInfo("push", "p", """[pages] [offset]
    pushes the specified pages by offset pages (offset can be negative).

    examples:
        p 3 7
            moves page 3 to 7 pages down, i.e. to page 10.
        p 4,9,2 1
            moves pages 2,4,9 by 1 page.
        p 5-8 -3
            moves pages 5,6,7,8 to 3 pages BACK.
        p 5,6,90-94 5
            moves pages 5,6,90,91,92,93,94 to be 5 pages down.
        p -5 4
            moves pages 1,2,3,4,5 to be 4 pages down.
        p 67- -7
            move pages from 67 to the end of the PDF to be 7 pages back.
        p 70- 5
            FAILS. 70- includes the end of the PDF, and you can't move that further down.
    """),
    "undo": info.CommandInfo("undo", "u", """[number?]
    undo the previous [number] commands.

    examples:
        u
            undoes the previous command
        u 3
            undoes the previous 3 commands
        u all
            undoes all commands issued this session (reverts document fully)
    """),
}

command_info_by_shorts = {cmd.short: cmd for name, cmd in command_info.items()}

def print_help(subcommand: str | None = None):
    if subcommand is None:
         print("pdfriend edit shell for quick changes. Commands:")
         for command, info in command_info.items():
             print(f"{command} (short: {info.short})")

         print("use h [command] to learn more about a specific command")
         return

    sub_info = None
    if subcommand in command_info_by_shorts:
        sub_info = command_info_by_shorts[subcommand]
    elif subcommand in command_info:
        sub_info = command_info[subcommand]
    else:
        raise exceptions.ExpectedError(f"command \"{subcommand}\" does not exist")

    print(f"{sub_info.name}|{sub_info.short} {sub_info.descr}")



def run_edit_command(pdf: wrappers.PDFWrapper, args: list[str]):
    no_command_msg = "No command specified! Type h or help for a list of the available commands"
    if len(args) == 0:
        raise exceptions.ExpectedError(no_command_msg)

    command = args[0]
    if command == "":
        raise exceptions.ExpectedError(no_command_msg)

    short = ""; long = ""
    if command in command_info_by_shorts:
        short = command
        long = command_info_by_shorts[command].name
    elif command in command_info:
        long = command
        short = command_info[command].short
    else:
        raise exceptions.ExpectedError(f"command \"{command}\" does not exist")

    cmd_parser = cmdparsers.CmdParser(long, args[1:])

    if short == "h":
        subcommand = cmd_parser.next_str_or(None)
        print_help(subcommand)

        # this is to prevent rewriting the file and appending
        # the command to the command stack
        raise exceptions.ShellContinue()
    if short == "e":
        raise exceptions.ShellExit()
    if short == "r":
        pages = cmd_parser.next_typed("PDF slice", lambda s: pdf.slice(s), "pages")
        angle = cmd_parser.next_float("angle")

        if len(pages) == 0:
            return
        # the slice is sorted, so if any pages are out of range, it'll
        # either be the first or the last one, probably the last
        pdf.raise_if_out_of_range(pages[-1])
        pdf.raise_if_out_of_range(pages[0])

        for page in pages:
            pdf.rotate_page(page, angle)
    if short == "d":
        pages = cmd_parser.next_typed("PDF slice", lambda s: pdf.slice(s))

        for page in pages:
            pdf.pop_page(page)
    if short == "s":
        page_0 = cmd_parser.next_int("page_0")
        pdf.raise_if_out_of_range(page_0)
        page_1 = cmd_parser.next_int("page_1")
        pdf.raise_if_out_of_range(page_1)

        pdf.swap_pages(page_0, page_1)
    if short == "m":
        source = cmd_parser.next_int("source")
        pdf.raise_if_out_of_range(source)
        destination = cmd_parser.next_int("destination")
        pdf.raise_if_out_of_range(destination)

        page = pdf.pages.pop(source - 1)
        pdf.pages.insert(destination - 1, page)
    if short == "p":
        pages = cmd_parser.next_typed("PDF slice", lambda s: pdf.slice(s), "pages")
        offset = cmd_parser.next_int("offset")

        last_page_before = pages[-1]
        last_page_after = last_page_before + offset

        if last_page_after > pdf.len(): # only check last page, as the slice is sorted
            raise exceptions.ExpectedError(
                f"can't move page {last_page_before} to {last_page_after}, as it's outside the PDF (number of pages: {pdf.len()})"
            )

        if offset > 0:
            pages = pages[::-1]

        for page in pages:
            p = pdf.pages.pop(page - 1)
            pdf.pages.insert(page + offset - 1, p)
    if short == "u":
        # arg will be converted to int, unless it's "all". Defaults to 1
        num_of_commands = cmd_parser.next_typed_or(
            "int or \"all\"", lambda s: s if s == "all" else int(s),
            1 # default value
        )

        raise exceptions.ShellUndo(num_of_commands)


def edit(infile: str):
    pdf = wrappers.PDFWrapper.Read(infile)
    command_stack = []

    # backup the file, because it will be overwritten
    backup_path = pdf.backup(infile)
    print(f"editing {infile}\nbackup created in {backup_path}")

    while True:
        try:
            args = parse_command_string(input(""))
            run_edit_command(pdf, args)
            command_stack.append(args)

            pdf.write(infile) # overwrites the file!
        except (KeyboardInterrupt, exceptions.ShellExit):
            return
        except exceptions.ShellContinue:
            continue
        except exceptions.ShellUndo as undo:
            if undo.num == "all":
                command_stack = []
            else:
                command_stack = command_stack[:-undo.num]

            pdf = wrappers.PDFWrapper.Read(backup_path)
            for args in command_stack:
                run_edit_command(pdf, args)

            pdf.write(infile)
        except exceptions.ExpectedError as e:
            print(e)
        except Exception as e:
            utils.print_unexpected_exception(e, Config.Debug)

